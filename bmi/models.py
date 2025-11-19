from django.conf import settings
from django.db import models


class BMIRecord(models.Model):
    

    SEX_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    WEIGHT_UNIT_CHOICES = [
        ("kg", "Kilograms"),
        ("lb", "Pounds"),
    ]

    HEIGHT_UNIT_CHOICES = [
        ("m", "Metres"),
        ("cm", "Centimetres"),
        ("ft_in", "Feet/Inches"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="bmi_records",
    )

    sex = models.CharField(max_length=10, choices=SEX_CHOICES)

    # stored in metric for consistency
    weight_kg = models.FloatField(help_text="Weight in kilograms")
    height_m = models.FloatField(help_text="Height in metres")

    bmi_value = models.FloatField()
    category = models.CharField(max_length=20)  # e.g. "underweight", "healthy", "overweight"

    # what the user originally selected/entered
    original_weight_unit = models.CharField(
        max_length=5,
        choices=WEIGHT_UNIT_CHOICES,
    )
    original_height_unit = models.CharField(
        max_length=10,
        choices=HEIGHT_UNIT_CHOICES,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        who = self.user.username if self.user else "Guest"
        return f"{who} - BMI {self.bmi_value:.1f} ({self.category})"



