from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

import random

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

    def clean(self):
        super().clean()
        if (self.endDate - self.startDate).days < 0:
            raise ValidationError("endDate cannot be before startDate")

    def __str__(self):
        return self.name
    
    def avgRating(self):
        ratings = list(map(lambda x: x.rating, self.writeups.all()))
        if len(ratings) == 0:
            return None
        else:
            return sum(ratings) / (0.0 + len(ratings))

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

class User(ValidatedModel):
    username = models.SlugField(primary_key = True, max_length = 50)
    password = models.TextField()
    email = models.EmailField(unique = True, max_length = 254)
    cookieID = models.BigIntegerField(unique = True)
    startYear = models.PositiveSmallIntegerField(null = True, blank = True, default = None)

    def __str__(self):
        return self.username

    def setEmail(self, newEmail):
        self.email = newEmail
        self.save()

    def setPassword(self, newPass):
        self.password = newPass
        self.save()

#    def setUsername(self, newUsername):
#        self.username = newUsername
#        self.save()

    def setStartYear(self, newStartYear):
        self.startYear = newStartYear
        self.save()

#    def regenerateCookieID(self):
#        self.cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
#        while User.objects.filter(cookieID = self.cookieID):
#            self.cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
#        self.save()

class Writeup(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "writeups")
    convention = models.ForeignKey(Convention, related_name = "writeups")
    rating = models.PositiveSmallIntegerField(validators = [MaxValueValidator(5)])
    review = models.TextField()
    miscCosts = models.DecimalField(max_digits = 10, decimal_places = 2)
    writeTime = models.DateTimeField(auto_now_add = True)
    editTime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user.__str__() + " writeup for " + self.convention.__str__()

    def setRating(self, newRating):
        self.rating = newRating
        self.save()

    def setReview(self, newReview):
        self.review = newReview
        self.save()

    def setMiscCosts(self, newMiscCosts):
        self.miscCosts = newMiscCosts
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

    def __str__(self):
        return self.name

    def setNumSold(self, newNumSold):
        self.numSold = newNumSold
        self.save()

    def setNumLeft(self, newNumLeft):
        self.numLeft = newNumLeft
        self.save()

    def setName(self, name):
        self.name = name
        self.save()

def newUser(username, password, email):
    cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    while User.objects.filter(cookieID = cookieID):
        cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    k = User(username = username, password = password, email = email, cookieID = cookieID)
    k.save()
    return k

def newWriteup(user, convention, rating, review, miscCosts):
    k = Writeup(user = user, convention = convention, rating = rating, review = review, miscCosts = miscCosts)
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

def newItem(user, convention, name, fandom, kind, price, cost, numSold, numLeft):
    k = Item(user = user, convention = convention, name = name, fandom = fandom, kind = kind, price = price, cost = cost, numSold = numSold, numLeft = numLeft)
    k.save()
    return k

def newConvention(name, startDate, endDate, numAttenders, location):
    k = Convention(name = name, startDate = startDate, endDate = endDate, numAttenders = numAttenders, location = location)
    k.save()
    return k
