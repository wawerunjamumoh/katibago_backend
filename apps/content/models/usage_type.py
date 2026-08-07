from django.db import models

class UsageType(models.TextChoices):
    INTRODUCTION = "INTRODUCTION", "introduction"
    PRIMARY = "PRIMARY", "Primary"
    SUPPLEMENTARY = "SUPPLEMENTARY", "Supplementary"