from django.db import models
from django.contrib.auth.models import AbstractUser

# Model uživatele
class Uzivatel(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=False)
    vek = models.IntegerField(null=True, blank=True)
    vaha = models.FloatField(null=True, blank=True)
    vyska = models.FloatField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="uzivatele_skupiny",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="uzivatele_opravneni",
        blank=True,
    )

    def __str__(self):
        return self.username

# Model tréninku    
class Trenink(models.Model):
    TRENINK_TYPES = [
        ('gym', 'Gym/Posilovna'),
        ('workout', 'Workout'),
        ('běh', 'Běh'),
        ('cyklo', 'Kolo'),
    ]

    user = models.ForeignKey(Uzivatel, on_delete=models.CASCADE)
    nazev = models.CharField(max_length=100)
    datum = models.DateField()
    type = models.CharField(max_length=20, choices=TRENINK_TYPES) # Typ tréninku
    doba = models.PositiveIntegerField() # Uplynulá doba tréninku v minutách
    pozn = models.TextField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"

