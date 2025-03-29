from django.db import models
from django.contrib.auth.models import AbstractUser

# Model uživatele
class Uzivatel(AbstractUser): # Model získává základní autentizační funkce
    username = models.CharField(unique=True, max_length=100) # Uživatelské jméno (zadává se při přihlášení)
    email = models.EmailField(unique=False) # E-mail (zadává se při přihlášení)
    # Věk, váha a výška uživatele
    vek = models.IntegerField(null=True, blank=True)
    vaha = models.FloatField(null=True, blank=True)
    vyska = models.FloatField(null=True, blank=True)
    id = models.AutoField(primary_key=True) # Identifikátor uživatele (genruje se po přihlášení)
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

    # Typy tréninků na výběr
    TRENINK_TYPES = [
        ('Gym', 'Gym/Posilovna'),
        ('Workout', 'Workout'),
        ('Běh', 'Běh'),
        ('Cyklo', 'Kolo'),
        ('Míčovky', 'Míčovky'),
        ('Plavání', 'Plavání'),
        ('Běžky', 'Běžky'),
    ]

    user = models.ForeignKey(Uzivatel, on_delete=models.CASCADE) # Uživatel přihlášení v Trenink Deniku
    nazev = models.CharField(max_length=100) # Název tréninku
    datum = models.DateField() # Datum (neměnitelné textové pole)
    type = models.CharField(max_length=20, choices=TRENINK_TYPES) # Rozbalovací buńka s nabýzenými typy tréninků
    doba = models.PositiveIntegerField() # Doba tréninku v minutách
    pozn = models.TextField(max_length=100, blank=True, null=True) # Dodatečné poznámky
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"

