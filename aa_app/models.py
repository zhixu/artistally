from django.db import models
from django.db.models import Avg, Q, Sum
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import datetime, random


INV_CON = None      # initialized in artistally/urls.py

class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        u = User(username = username, email = self.normalize_email(email))
        u.setPassword(password)
        return u
        
    def create_superuser(self, username, email, password):
        u = self.create_user(username, email, password)
        u.setSuperuser(True)
        return u

class ValidatedModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(args, kwargs)

        
class User(AbstractBaseUser):
    username = models.SlugField(primary_key = True, max_length = 50)
    email = models.EmailField(unique = True, max_length = 254)
    startYear = models.PositiveSmallIntegerField(null = True, blank = True, default = None)
    image = models.URLField(max_length = 200, blank = True, null = True, default = None)
    superuser = models.BooleanField(default = False)

    @property
    def conventions(self):
        return Convention.objects.filter(Q(items__user = self) | Q(writeups__user = self)).exclude(ID = INV_CON.ID).distinct()
    
    @property
    def profit(self):
        profit = -(self.miscCosts.aggregate(Sum("amount"))["amount__sum"] or 0)
        for item in self.items.all():
            profit += item.price * item.numSold
            profit -= item.cost * item.numSold  # numSold or numLeft?
        return profit

    # SETTERS
    def setEmail(self, newEmail):
        self.email = newEmail
        self.save()

    def setPassword(self, newPass):
        self.password = newPass
        self.save()

    def setStartYear(self, newStartYear):
        self.startYear = newStartYear
        self.save()

    def setImage(self, newImage):
        self.image = newImage
        self.save()
        
    def setSuperuser(self, newSuperuser):
        self.superuser = newSuperuser
        self.save()
        
    def setPassword(self, newPassword):
        self.set_password(newPassword)
        self.save()
        
    # UTIL
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def is_staff(self):
        return self.superuser
    
    def is_active(self):
        return self.is_active
    
    def has_perm(self, perm, obj = None):
        return self.superuser
    
    def has_module_perms(self, app_label):
        return self.superuser

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(args, kwargs)
    
    def __str__(self):
        return self.username

class Convention(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    name = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()
    numAttenders = models.PositiveIntegerField()
    location = models.TextField()
    website = models.URLField(max_length = 200)
    image = models.URLField(max_length = 200, blank = True, null = True, default = None)
    
    @property
    def avgRating(self):
        return self.writeups.aggregate(Avg("rating"))["rating__avg"]
    
    @property
    def avgUserProfit(self):
        profit = -(self.miscCosts.aggregate(Sum("amount"))["amount__sum"] or 0)
        for item in self.items.all():
            profit += item.price * item.numSold
            profit -= item.cost * item.numSold  # numSold or numLeft?
        return profit / self.users().count()
    
    @property
    def users(self):
        return User.objects.filter(Q(items__convention = self) | Q(writeups__convention = self)).distinct()

    # SETTERS
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

    def setImage(self, newImage):
        self.image = newImage
        self.save()

    # UTIL
    def clean(self):
        super().clean()
        if (self.endDate - self.startDate).days < 0:
            raise ValidationError("endDate cannot be before startDate")

    def __str__(self):
        return self.name

class Writeup(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "writeups")
    convention = models.ForeignKey(Convention, related_name = "writeups")
    rating = models.PositiveSmallIntegerField(validators = [MaxValueValidator(5)])
    review = models.TextField()
    writeTime = models.DateTimeField(auto_now_add = True)
    editTime = models.DateTimeField(auto_now = True)

    # SETTERS
    def setRating(self, newRating):
        self.rating = newRating
        self.save()

    def setReview(self, newReview):
        self.review = newReview
        self.save()
    
    # UTIL
    def clean(self):
        super().clean()
        if self.convention is INV_CON:
            raise ValidationError("you can't make a writeup for the INV_CON")
        filtered = self.user.writeups.filter(convention = self.convention)
        if filtered.exists() and filtered.get().ID is not self.ID:
            raise ValidationError("user already has a writeup for that convention")

    def __str__(self):
        return self.user.__str__() + " writeup for " + self.convention.__str__()

class Fandom(ValidatedModel):
    name = models.TextField(primary_key = True)

    # SETTERS
    def setName(self, name):
        self.name = name
        self.save()
        
    # UTIL
    def __str__(self):
        return self.name

class Kind(ValidatedModel):
    name = models.TextField(primary_key = True)

    # SETTERS
    def setName(self, name):
        self.name = name
        self.save()

    # UTIL
    def __str__(self):
        return self.name

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
    image = models.URLField(max_length = 200, blank = True, null = True, default = None)

    # SETTERS
    def setNumSold(self, newNumSold):
        self.numSold = newNumSold
        self.save()

    def setNumLeft(self, newNumLeft):
        self.numLeft = newNumLeft
        self.save()

    def setName(self, newName):
        self.name = Name
        self.save()

    def setImage(self, newImage):
        self.image = newImage
        self.save()
    
    # UTIL
    def clean(self):
        super().clean()
        if self.convention is INV_CON and self.numSold != 0:
            raise ValidationError("you can't have a nonzero numSold for the INV_CON")
        if self.price < 0 or self.cost < 0:
            raise ValidationError("you can't have negative price or cost")

    def __str__(self):
        return self.name
        
class MiscCost(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "miscCosts")
    convention = models.ForeignKey(Convention, related_name = "miscCosts")
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    # SETTERS    
    def setAmount(self, newAmount):
        self.amount = newAmount
        self.save()

    # UTIL
    def clean(self):
        super().clean()
        if self.amount < 0:
            raise ValidationError("you can't have negative miscCost amount")
    
    def __str__(self):
        return str(self.amount)

def newUser(username, password, email):
    return User.objects.create_user(username = username, password = password, email = email)

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
