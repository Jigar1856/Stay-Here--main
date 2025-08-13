from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = ("name", "contact", "age", "city", "game_level", "payment_status", "date_registered", "amount_paid")
	list_filter = ("payment_status", "game_level", "date_registered", "city")
	search_fields = ("name", "contact", "city")
