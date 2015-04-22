from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Convention(models.Model):
    ID = models.AutoField(primary_key = True)
    name = models.TextField()
    date = models.DateField()
    numAttenders = models.PositiveIntegerField()
    location = models.TextField()

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.TextField(primary_key = True)
    password = models.TextField()
    email = models.EmailField(unique = True, max_length = 254)
    cookieID = models.BigIntegerField(unique = True)
    startYear = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.username

    def setEmail(self, newEmail):
        self.email = newEmail
        self.full_clean()
        self.save()

    def setPassword(self, newPass):
        self.password = newPass
        self.full_clean()
        self.save()

    def setUsername(self, newUsername):
        self.username = newUsername
        self.full_clean()
        self.save()

class Item(models.Model):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "items")
    convention = models.ForeignKey(Convention, related_name = "items")
    name = models.TextField()
    fandom = models.ForeignKey(Fandom, related_name = "items")
    kind = models.ForeignKey(Kind, related_name = "items")
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    cost = models.DecimalField(max_digits = 10, decimal_places = 2)
    num = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Writeup(models.Model):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "writeups")
    convention = models.ForeignKey(Convention, related_name = "writeups")
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    review = models.TextField()
    miscCosts = models.DecimalField(max_digits = 10, decimal_places = 2)

class Fandom(models.Model):
    name = models.TextField(primary_key = True)

class Kind(models.Model):
    name = models.TextField(primary_key = True)
