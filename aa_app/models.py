from django.db import models
from django.db.models import Avg, Q, Sum
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime, random

class ValidatedModel(models.Model):
    class Meta:
        abstract = True

    def save(self):
        self.full_clean()
        super().save()

class Convention(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    name = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()
    numAttenders = models.PositiveIntegerField()
    location = models.TextField()
    website = models.URLField(max_length=200)
    
    def avgRating(self):
        return self.writeups.aggregate(Avg("rating"))["rating__avg"]
    
    def avgUserProfit(self):
        profit = -self.miscCosts.aggregate(Sum("amount"))["amount__sum"]
        for item in self.items.all():
            profit += item.price * item.numSold
            profit -= item.cost * item.numSold  # numSold or numLeft?
        return profit / self.users().count()
    
    def users(self):
        return User.objects.filter(Q(items__convention = self) | Q(writeups__convention = self)).distinct()

    def clean(self):
        super().clean()
        if (self.endDate - self.startDate).days < 0:
            raise ValidationError("endDate cannot be before startDate")

    def __str__(self):
        return self.name

    def setName(self, newName):
        self.name = newName
        self.save()

    def setNumAttenders(self, newNumAttenders):
        self.numAttenders = newNumAttenders
        self.save()

    def setLocation(self, newLocation):
        self.location = newLocation
        self.save()

    def setStartDate(self, newStartDate):
        self.startDate = newStartDate
        self.save()

    def setEndDate(self, newEndDate):
        self.endDate = newEndDate
        self.save()

    def setWebsite(self, newWebsite):
        self.website = newWebsite
        self.save()

class User(ValidatedModel):
    username = models.SlugField(primary_key = True, max_length = 50)
    password = models.TextField()
    email = models.EmailField(unique = True, max_length = 254)
    cookieID = models.BigIntegerField(unique = True)
    startYear = models.PositiveSmallIntegerField(null = True, blank = True, default = None)

    def conventions(self):
        return Convention.objects.filter(Q(items__user = self) | Q(writeups__user = self)).exclude(ID = INV_CON.ID).distinct()
    
    def profit(self):
        profit = -self.miscCosts.aggregate(Sum("amount"))["amount__sum"]
        for item in self.items.all():
            profit += item.price * item.numSold
            profit -= item.cost * item.numSold  # numSold or numLeft?
        return profit
    
    def __str__(self):
        return self.username

    def setEmail(self, newEmail):
        self.email = newEmail
        self.save()

    def setPassword(self, newPass):
        self.password = newPass
        self.save()

    def setStartYear(self, newStartYear):
        self.startYear = newStartYear
        self.save()

#    def regenerateCookieID(self):
#        self.cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
#        while User.objects.filter(cookieID = self.cookieID).exists():
#            self.cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
#        self.save()

class Writeup(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "writeups")
    convention = models.ForeignKey(Convention, related_name = "writeups")
    rating = models.PositiveSmallIntegerField(validators = [MaxValueValidator(5)])
    review = models.TextField()
    writeTime = models.DateTimeField(auto_now_add = True)
    editTime = models.DateTimeField(auto_now = True)

    def clean(self):
        super().clean()
        if self.convention is INV_CON:
            raise ValidationError("you can't make a writeup for the INV_CON")
        filtered = self.user.writeups.filter(convention = self.convention)
        if filtered.exists() and filtered.get().ID is not self.ID:
            raise ValidationError("user already has a writeup for that convention")

    def __str__(self):
        return self.user.__str__() + " writeup for " + self.convention.__str__()

    def setRating(self, newRating):
        self.rating = newRating
        self.save()

    def setReview(self, newReview):
        self.review = newReview
        self.save()

class Fandom(ValidatedModel):
    name = models.TextField(primary_key = True)

    def __str__(self):
        return self.name

    def setName(self, name):
        self.name = name
        self.save()

class Kind(ValidatedModel):
    name = models.TextField(primary_key = True)

    def __str__(self):
        return self.name

    def setName(self, name):
        self.name = name
        self.save()

class Item(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "items")
    convention = models.ForeignKey(Convention, related_name = "items")
    name = models.TextField()
    fandom = models.ForeignKey(Fandom, related_name = "items")
    kind = models.ForeignKey(Kind, related_name = "items")
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    cost = models.DecimalField(max_digits = 10, decimal_places = 2)
    numSold = models.PositiveIntegerField()
    numLeft = models.PositiveIntegerField()
    
    def clean(self):
        super().clean()
        if self.convention is INV_CON and self.numSold != 0:
            raise ValidationError("you can't have a nonzero numSold for the INV_CON")
        if self.price < 0 or self.cost < 0:
            raise ValidationError("you can't have negative price or cost")

    def __str__(self):
        return self.name

    def setNumSold(self, newNumSold):
        self.numSold = newNumSold
        self.save()

    def setNumLeft(self, newNumLeft):
        self.numLeft = newNumLeft
        self.save()

    def setName(self, newName):
        self.name = Name
        self.save()
        
class MiscCost(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "miscCosts")
    convention = models.ForeignKey(Convention, related_name = "miscCosts")
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    def clean(self):
        super().clean()
        if self.amount < 0:
            raise ValidationError("you can't have negative miscCost amount")
    
    def __str__(self):
        return str(self.amount)
    
    def setAmount(self, newAmount):
        self.amount = newAmount
        self.save()

def newUser(username, password, email):
    cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    while User.objects.filter(cookieID = cookieID).exists():
        cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    k = User(username = username, password = password, email = email, cookieID = cookieID)
    k.save()
    return k

def newWriteup(user, convention, rating, review):
    k = Writeup(user = user, convention = convention, rating = rating, review = review)
    k.save()
    return k

def newFandom(name):
    k = Fandom(name = name)
    k.save()
    return k

def newKind(name):
    k = Kind(name = name)
    k.save()
    return k

def newMiscCost(user, convention, amount):
    k = MiscCost(user = user, convention = convention, amount = amount)
    k.save()
    return k

def newItem(user, convention, name, fandom, kind, price, cost, numSold, numLeft):
    k = Item(user = user, convention = convention, name = name, fandom = fandom, kind = kind, price = price, cost = cost, numSold = numSold, numLeft = numLeft)
    k.save()
    return k

def newConvention(name, startDate, endDate, numAttenders, location, website):
    k = Convention(name = name, startDate = startDate, endDate = endDate, numAttenders = numAttenders, location = location, website = website)
    k.save()
    return k

INV_CON = None
if Convention.objects.filter(name = "INV_CON").exists():
    INV_CON = Convention.objects.get(name = "INV_CON")
else:
    INV_CON = newConvention("INV_CON", datetime.datetime(1, 1, 1), datetime.datetime(1, 1, 1), 1, "artistally", "https://artistal.ly")
