from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Convention(models.Model):
    ID = models.AutoField(primary_key = True)
    name = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()
    numAttenders = models.PositiveIntegerField()
    location = models.TextField()

    def __str__(self):
        return self.name

    def setName(self, newName):
        self.name = newName
        self.full_clean()
        self.save()

    def setNumAttenders(self, newNumAttenders):
        self.numAttenders = newNumAttenders
        self.full_clean()
        self.save()

    def setLocation(self, newLocation):
        self.location = newLocation
        self.full_clean()
        self.save()

    def setStartDate(self, newStartDate):
        self.startDate = newStartDate
        self.full_clean()
        self.save()

    def setEndDate(self, newEndDate):
        self.endDate = newEndDate
        self.full_clean()
        self.save()

class User(models.Model):
    username = models.SlugField(primary_key = True, max_length = 50)
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

    def regenerateCookieID(self):
        self.cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
        self.full_clean()
        self.save()

class Writeup(models.Model):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "writeups")
    convention = models.ForeignKey(Convention, related_name = "writeups")
    rating = models.PositiveSmallIntegerField(validators = [MaxValueValidator(5)])
    review = models.TextField()
    miscCosts = models.DecimalField(max_digits = 10, decimal_places = 2)
    writeTime = models.DateTimeField(auto_now_add = True)
    editTime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user + " " + self.convention

    def setRating(self, newRating):
        self.rating = newRating
        self.full_clean()
        self.save()

    def setReview(self, newReview):
        self.review = newReview
        self.full_clean()
        self.save()

    def setMiscCosts(self, newMiscCosts):
        self.miscCosts = newMiscCosts
        self.full_clean()
        self.save()

class Fandom(models.Model):
    name = models.TextField(primary_key = True)

    def __str__(self):
        return self.name

    def setName(self, name):
        self.name = name
        self.full_clean()
        self.save()

class Kind(models.Model):
    name = models.TextField(primary_key = True)

    def __str__(self):
        return self.name

    def setName(self, name):
        self.name = name
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
    numSold = models.PositiveIntegerField()
    numLeft = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def setNumSold(self, newNumSold):
        self.numSold = newNumSold
        self.full_clean()
        self.save()

    def setNumLeft(self, newNumLeft):
        self.numLeft = newNumLeft
        self.full_clean()
        self.save()

    def setName(self, name):
        self.name = name
        self.full_clean()
        self.save()

def newUser(username, password, email, startYear):
    cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    k = User(username = username, password = password, email = email, cookieID = cookieID, startYear = startYear)
    k.full_clean()
    k.save()
    return k

def newWriteup(user, convention, rating, review, miscCosts):
    k = Writeup(user = user, convention = convention, rating = rating, review = review, miscCosts = miscCosts)
    k.full_clean()
    k.save()
    return k

def newFandom(name):
    k = Fandom(name = name)
    k.full_clean()
    k.save()
    return k

def newKind(name):
    k = Kind(name = name)
    k.full_clean()
    k.save()
    return k

def newItem(user, convention, name, fandom, kind, price, cost, numSold, numLeft):
    k = Item(user = user, convention = convention, fandom = fandom, kind = kind, price = price, cost = cost, numSold = numSold, numLeft = numLeft)
    k.full_clean()
    k.save()
    return k

def newConvention(name, startDate, endDate, numAttenders, location):
    k = Convention(name = name, startDate = startDate, endDate = endDate, numAttenders = numAttenders, location = location)
    k.full_clean()
    k.save()
    return k
