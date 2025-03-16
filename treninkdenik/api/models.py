from django.db import models
from django.contrib.auth.models import AbstractUser

# Model uživatele
class Uzivatel(AbstractUser):
    jmeno = models.CharField(unique=False, max_length=100)
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
        return self.jmeno

# Model tréninku    
class Trenink(models.Model):
    TRENINK_TYPES = [
        ('gym', 'Posilovna'),
        ('outdoor', 'Outdoor'),
    ]

    user = models.ForeignKey(Uzivatel, on_delete=models.CASCADE)
    datum = models.DateField()
    type = models.CharField(max_length=20, choices=TRENINK_TYPES) # Typ tréninku
    doba = models.PositiveIntegerField() # Uplynulá doba tréninku v minutách
    pozn = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"

