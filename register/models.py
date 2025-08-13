
from django.db import models
from django.utils import timezone

class Player(models.Model):
	GAME_LEVELS = [
		("beginner", "Beginner"),
		("intermediate", "Intermediate"),
		("advanced", "Advanced"),
	]
	PREFERRED_TIME_CHOICES = [
		("after_10_am", "After 10 AM"),
		("after_1_pm", "After 1 PM"),
		("after_4_pm", "After 4 PM"),
		("after_8_pm", "After 8 PM"),
	]
	STATUS_CHOICES = [
		("pending", "Pending"),
		("accepted", "Accepted"),
		("rejected", "Rejected"),
	]
	name = models.CharField(max_length=100)
	contact = models.CharField(max_length=20)
	age = models.PositiveIntegerField()
	city = models.CharField(max_length=100, null=True, blank=True)
	game_level = models.CharField(max_length=20, choices=GAME_LEVELS, null=True, blank=True)
	preferred_time = models.CharField(max_length=20, choices=PREFERRED_TIME_CHOICES, null=True, blank=True)
	payment_status = models.BooleanField(default=False)
	payment_screenshot = models.ImageField(upload_to="payments/", blank=True, null=True)
	date_registered = models.DateTimeField(default=timezone.now)
	amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

	def __str__(self):
		return f"{self.name} ({self.contact})"
