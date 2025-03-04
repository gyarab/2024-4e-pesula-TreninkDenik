from django.db import models

# Model uživatele
class Uzivatel(models.Model):
    jmeno = models.CharField(max_length=100)
    vek = models.IntegerField()
    vyska = models.FloatField()
    vaha = models.FloatField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.jmeno

# Model tréninku    
class Trenink(models.Model):
    TRENINK_TYPES = [
        ('gym', 'Posilovna'),
        ('outdoor', 'Outdoor'),
    ]

    user = models.ForeignKey(Uzivatel, on_delete=models.CASCADE)
    datum = models.DateField() # Datum konání tréninku
    type = models.CharField(max_length=20, choices=TRENINK_TYPES) # Typ tréninku
    doba = models.PositiveIntegerField() # Uplynulá doba tréninku v minutách
    pozn = models.TextField(blank=True) # Poznámky z tréninku
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"

