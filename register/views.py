from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Player
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import decimal
from django.http import HttpResponse, Http404
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.parse

def register(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		contact = request.POST.get('contact')
		age = request.POST.get('age')
		city = request.POST.get('city')
		game_level = request.POST.get('game_level')
		preferred_time = request.POST.get('preferred_time')
		amount_paid = request.POST.get('amount_paid', '0')
		payment_status = False
		payment_screenshot = None
		if request.FILES.get('payment_screenshot'):
			payment_screenshot = request.FILES['payment_screenshot']
			payment_status = True  # Assume manual verification for demo
		player = Player.objects.create(
			name=name,
			contact=contact,
			age=age,
			city=city,
			game_level=game_level,
			preferred_time=preferred_time,
			payment_status=payment_status,
			amount_paid=decimal.Decimal(amount_paid),
			date_registered=timezone.now(),
			payment_screenshot=payment_screenshot
		)
		return redirect('payment_success')
	return render(request, 'register/register.html')

def payment_success(request):
	return render(request, 'register/payment_success.html')

def owner_login(request):
	if request.user.is_authenticated:
		return redirect('owner_dashboard')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None and user.is_staff:
			login(request, user)
			return redirect('owner_dashboard')
		else:
			messages.error(request, 'Invalid credentials or not an owner.')
	return render(request, 'register/owner_login.html')


@login_required(login_url='owner_login')
def owner_dashboard(request):
	try:
		players = Player.objects.all().order_by('-date_registered')
		total_players = players.count()
		total_amount = sum([p.amount_paid for p in players if p.payment_status])
		accepted_players = Player.objects.filter(status='accepted').order_by('-date_registered')
		accepted_players_count = accepted_players.count()
		accepted_players_total = sum([p.amount_paid for p in accepted_players])
		rejected_players = Player.objects.filter(status='rejected').order_by('-date_registered')
		rejected_players_count = rejected_players.count()
		rejected_players_total = sum([p.amount_paid for p in rejected_players])
		return render(request, 'register/owner_dashboard.html', {
			'players': players,
			'accepted_players': accepted_players,
			'rejected_players': rejected_players,
			'total_players': total_players,
			'total_amount': total_amount,
			'accepted_players_count': accepted_players_count,
			'accepted_players_total': accepted_players_total,
			'rejected_players_count': rejected_players_count,
			'rejected_players_total': rejected_players_total,
		})
	except Exception as e:
		# Log the error for debugging
		print(f"Error in owner_dashboard: {e}")
		# Return a simple error page or redirect
		return render(request, 'register/owner_dashboard.html', {
			'players': [],
			'accepted_players': [],
			'rejected_players': [],
			'total_players': 0,
			'total_amount': 0,
			'accepted_players_count': 0,
			'accepted_players_total': 0,
			'rejected_players_count': 0,
			'rejected_players_total': 0,
		})

@login_required(login_url='owner_login')
@csrf_exempt
def player_decision(request, player_id):
	from django.shortcuts import get_object_or_404
	player = get_object_or_404(Player, id=player_id)
	if request.method == 'POST':
		decision = request.POST.get('decision')
		if decision == 'accept':
			player.status = 'accepted'
		elif decision == 'reject':
			player.status = 'rejected'
		player.save()
		# WhatsApp message
		receipt = (
			"Stay Here Snooker Club\n\nTournament Selection Letter\n\n"
		)
		receipt += f"Name: {player.name}\nContact: {player.contact}\nAge: {player.age}\nCity: {player.city or ''}\nGame Level: {player.game_level or ''}\nAmount Paid: ₹{player.amount_paid}\nDate Registered: {player.date_registered.strftime('%Y-%m-%d %H:%M')}\n\n"
		if decision == 'accept':
			receipt += "Congratulations! You have been ACCEPTED for the tournament."
		else:
			receipt += "We regret to inform you that you have NOT been selected for the tournament."
		# WhatsApp API link (using wa.me)
		phone = player.contact.strip().replace('+', '').replace(' ', '')
		if phone.startswith('0'):
			phone = phone[1:]
		wa_url = f"https://wa.me/{phone}?text={urllib.parse.quote(receipt)}"
		return HttpResponseRedirect(wa_url)
	return redirect('owner_dashboard')

def owner_logout(request):
	logout(request)
	return redirect('owner_login')


def logo_page(request):
	return render(request, 'register/logo.html')

def serve_media_file(request, file_path):
    """
    Serve media files securely, specifically for payment screenshots
    """
    # Only allow access to payment screenshots
    if not file_path.startswith('payments/'):
        raise Http404("File not found")
    
    # Construct the full file path
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # Check if file exists and is within media directory
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise Http404("File not found")
    
    # Check if the path is within the media directory (security check)
    if not os.path.abspath(full_path).startswith(os.path.abspath(settings.MEDIA_ROOT)):
        raise Http404("File not found")
    
    # Get file extension to determine content type
    file_extension = os.path.splitext(file_path)[1].lower()
    content_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.pdf': 'application/pdf',
    }
    content_type = content_type_map.get(file_extension, 'application/octet-stream')
    
    # Read and serve the file
    try:
        with open(full_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
            return response
    except Exception:
        raise Http404("File not found")
