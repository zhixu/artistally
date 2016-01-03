from django.db import models
from django.db.models import Avg, Sum, F, ExpressionWrapper
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ValidationError, ImproperlyConfigured, AppRegistryNotReady
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail

from artistally.settings import EMAIL_HOST_USER

import datetime, random, statistics, collections, operator, uuid

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
        app_label = "aa_app"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(args, kwargs)


class User(AbstractBaseUser):
    username = models.SlugField(primary_key = True, max_length = 50)
    email = models.EmailField(unique = True, max_length = 254)
    superuser = models.BooleanField(default = False)
    startYear = models.PositiveSmallIntegerField(null = True, blank = True, default = None)
    image = models.URLField(max_length = 200, blank = True, default = "")
    description = models.TextField(blank = True, default = "")
    website1 = models.URLField(max_length = 200, blank = True, default = "")
    website2 = models.URLField(max_length = 200, blank = True, default = "")
    website3 = models.URLField(max_length = 200, blank = True, default = "")
    confirmToken = models.UUIDField(blank = True, null = True, default = None)
    resetToken = models.UUIDField(blank = True, null = True, default = None)

    @property
    def profit(self):    # does NOT include cost of items that weren't so
        profit = -(self.miscCosts.aggregate(Sum("amount"))["amount__sum"] or 0)
        for item in self.items.all():
            profit += item.price * item.numSold
            profit -= item.cost * item.numSold
        return profit

    # SETTERS
    def setPassword(self, newPassword):
        self.set_password(newPassword)
        self.save()

    def setEmail(self, newEmail):
        self.email = newEmail
        self.save()

    def setSuperuser(self, newSuperuser):
        self.superuser = newSuperuser
        self.save()

    def setStartYear(self, newStartYear):
        self.startYear = newStartYear
        self.save()

    def setImage(self, newImage):
        self.image = newImage
        self.save()

    def setDescription(self, newDescription):
        self.description = newDescription
        self.save()

    def setWebsite1(self, newWebsite1):
        self.website1 = newWebsite1
        self.save()

    def setWebsite2(self, newWebsite2):
        self.website2 = newWebsite2
        self.save()

    def setWebsite3(self, newWebsite3):
        self.website3 = newWebsite3
        self.save()

    def setConfirmToken(self, newConfirmToken):
        self.confirmToken = newConfirmToken
        self.save()

    def setResetToken(self, newResetToken):
        self.resetToken = newResetToken
        self.save()
    
    # METHODS
    def sendConfirmEmail(self):
        if not self.confirmToken:
            self.setConfirmToken(uuid.uuid4())
        msg = "You just created your Artistally account.\n" + \
            "Here is your username and confirmation token. Enter it to continue.\n\n" + \
            "Username: " + self.username + "\n" + \
            "Token: " + str(self.confirmToken) + "\n\n" + \
            "If you did not submit such a request, feel free to ignore this email."
        send_mail("ArtistAlly Confirmation Request", msg, EMAIL_HOST_USER, [self.email])
        
    def sendResetEmail(self):
        if not self.resetToken:
            self.setResetToken(uuid.uuid4())
        msg = "Your account reset request was received.\n" + \
            "Here is your username and reset token. Enter it to continue.\n\n" + \
            "Username: " + self.username + "\n" + \
            "Token: " + str(self.resetToken) + "\n\n" + \
            "If you did not submit such a request, feel free to ignore this email."
        send_mail("ArtistAlly Reset Request", msg, EMAIL_HOST_USER, [self.email])
        
    def sendFeedback(self, subject, body):
        send_mail(subject + "\n\n Sent by " + self.username, body, EMAIL_HOST_USER, [EMAIL_HOST_USER])

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
        return True
    
    def has_perm(self, perm, obj = None):
        return self.superuser
    
    def has_module_perms(self, app_label):
        return self.superuser

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(args, kwargs)
        
    class Meta(ValidatedModel.Meta):
        pass
    
    def __str__(self):
        return self.username

class Convention(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    name = models.CharField(unique = True, max_length = 50)
    website = models.URLField(max_length = 200)
    image = models.URLField(max_length = 200, blank = True, default = "")

    def userProfit(self, u):
        return sum(e.userProfit(u) for e in self.events.all())

    @property
    def itemUsers(self):
        return User.objects.filter(items__event__in = self.events.all()).distinct()

    @property
    def avgRating(self):
        avgs = tuple(e.avgRating for e in self.events.all() if e.avgRating != 0)
        if len(avgs) > 0:
            return statistics.mean(avgs)
        else:
            return 0

    @property
    def avgUserProfit(self):
        avgs = tuple(e.avgUserProfit for e in self.events.all() if e.avgRating != 0)
        if len(avgs):
            return statistics.mean(avgs)
        else:
            return 0

    @property
    def itemsSoldTotal(self):
        return sum(e.itemsSoldTotal for e in self.events.all())
    
    @property
    def topKinds(self):
        kindsCounter = collections.Counter()
        for e in self.events.all():
            for k in e.items.all():
                if k.numSold:
                    kindsCounter[k.kind] += k.numSold
        if len(kindsCounter):
            for k in kindsCounter:
                kindsCounter[k] /= self.itemsSoldTotal
        return sorted(kindsCounter.items(), key = operator.itemgetter(1), reverse = True)
    
    @property
    def topFandoms(self):
        fandomsCounter = collections.Counter()
        for e in self.events.all():
            for k in e.items.all():
                if k.numSold:
                    fandomsCounter[k.fandom] += k.numSold
        if len(fandomsCounter):
            for k in fandomsCounter:
                fandomsCounter[k] /= self.itemsSoldTotal
        return sorted(fandomsCounter.items(), key = operator.itemgetter(1), reverse = True)

    # SETTERS
    def setName(self, newName):
        self.name = newName
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
        if INV_CON is not None and self == INV_CON:
            if self.events.exists():
                if self.events.count() > 1:
                    raise ValidationError({"events": ["badly attached extra events in the INV_CON"]})
                elif self.events.first() != INV_EVENT:
                    raise ValidationError({"events": ["event attached to the INV_CON is not INV_EVENT"]})

    def __str__(self):
        return self.name
    
class Event(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    convention = models.ForeignKey(Convention, related_name = "events")
    name = models.CharField(max_length = 50)
    startDate = models.DateField()
    endDate = models.DateField()
    numAttenders = models.PositiveIntegerField(blank = True, null = True, default = None)
    users = models.ManyToManyField(User, related_name = "events", blank = True)
    location = models.CharField(max_length = 50)
    
    def userProfit(self, u):
        expr = ExpressionWrapper((F("price") - F("cost")) * F("numSold"), output_field = models.DecimalField())
        agg = self.items.filter(user = u).annotate(profit = expr).aggregate(Sum("profit"))
        return agg["profit__sum"]or 0

    @property
    def itemUsers(self):
        return User.objects.filter(items__event = self).distinct()

    @property
    def avgRating(self):
        return self.writeups.aggregate(Avg("rating"))["rating__avg"] or 0

    @property
    def avgUserProfit(self):    # does NOT include cost of items that weren't sold
        profit = -(self.miscCosts.aggregate(Sum("amount"))["amount__sum"] or 0)
        for item in self.items.all():
            profit += item.price * item.numSold
            profit -= item.cost * item.numSold
        if self.itemUsers.count() > 0:
            return profit / self.itemUsers.count()
        else:
            return 0

    @property
    def itemsSoldTotal(self):
        return self.items.aggregate(Sum("numSold"))["numSold__sum"] or 0

    @property
    def kindValueSold(self):
        kindPrices = collections.Counter()
        for item in self.items.all():
            kindPrices[item.kind] += item.price * item.numSold
        return kindPrices

    @property
    def kindNumSold(self):
        kindNumSolds = collections.Counter()
        for item in self.items.all():
            kindNumSolds[item.kind] += item.numSold
        return kindNumSolds
    
    @property
    def avgKindPrice(self):
        result = self.kindValueSold
        for k in result:
            if self.kindNumSold[k] == 0:
                result[k] = None
            else:
                result[k] /= self.kindNumSold[k]
        return result
    
    @property
    def kindUserVotes(self):
        kindUsers = collections.Counter()
        for item in self.items.all():
            if item.kind not in kindUsers:
                kindUsers[item.kind] = set()
            kindUsers[item.kind].add(item.user)
        for kind in kindUsers:
            kindUsers[kind] = len(kindUsers[kind])
        return kindUsers
    
    @property
    def topKinds(self):
        kindsCounter = collections.Counter()
        for k in self.items.all():
            if k.numSold:
                kindsCounter[k.kind] += k.numSold
        if len(kindsCounter):
            for k in kindsCounter:
                kindsCounter[k] /= self.itemsSoldTotal
        return sorted(kindsCounter.items(), key = operator.itemgetter(1), reverse = True)
    
    @property
    def topFandoms(self):
        fandomsCounter = collections.Counter()
        for k in self.items.all():
            if k.numSold:
                fandomsCounter[k.fandom] += k.numSold
        if len(fandomsCounter):
            for k in fandomsCounter:
                fandomsCounter[k] /= self.itemsSoldTotal
        return sorted(fandomsCounter.items(), key = operator.itemgetter(1), reverse = True)
    
    # SETTERS
    def setName(self, newName):
        self.name = newName
        self.save()

    def setStartDate(self, newStartDate):
        self.startDate = newStartDate
        self.save()

    def setEndDate(self, newEndDate):
        self.endDate = newEndDate
        self.save()

    def setNumAttenders(self, newNumAttenders):
        self.numAttenders = newNumAttenders
        self.save()
        
    def setLocation(self, newLocation):
        self.location = newLocation
        self.save()
        
    def setUser(self, newUser):
        self.users.add(newUser)
        self.save()
            
    def unsetUser(self, newUser):
        self.users.remove(newUser)
        self.save()
    
    # UTIL
    class Meta(ValidatedModel.Meta):
        ordering = ["startDate"]

    def clean(self):
        super().clean()
        if (self.endDate - self.startDate).days < 0:
            raise ValidationError("endDate cannot be before startDate")
        try:
            if INV_EVENT is not None and self == INV_EVENT and self.users.exists():
                raise ValidationError({"users": ["you can't have a user favorite the INV_EVENT"]})
        except ValueError:  # can't access .users before instance gets saved
            pass
        #filtered = self.convention.events.filter(name = self.name)
        #if filtered.exists() and filtered.get().ID is not self.ID:
        #    raise ValidationError({"name": ["there is already an event in this convention with that name"]})
            
    def __str__(self):
        return self.name

class Writeup(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "writeups")
    event = models.ForeignKey(Event, related_name = "writeups")
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
        if self.event == INV_EVENT:
            raise ValidationError({"convention": ["you can't make a writeup for the INV_EVENT"]})
        filtered = self.user.writeups.filter(event = self.event)
        if filtered.exists() and filtered.get().ID is not self.ID:
            raise ValidationError("user already has a writeup for that event")

    def __str__(self):
        return "%s writeup for %s %s" % (self.user, self.event.convention, self.event)

class Fandom(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    name = models.CharField(unique = True, max_length = 50)

    # SETTERS
    def setName(self, name):
        self.name = name
        self.save()
        
    # UTIL
    def __str__(self):
        return self.name

class Kind(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    name = models.CharField(unique = True, max_length = 50)

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
    event = models.ForeignKey(Event, related_name = "items")
    name = models.CharField(max_length = 50)
    fandom = models.ForeignKey(Fandom, related_name = "items")
    kind = models.ForeignKey(Kind, related_name = "items")
    price = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    cost = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    numSold = models.PositiveIntegerField()
    numLeft = models.PositiveIntegerField()
    image = models.URLField(max_length = 200, blank = True, default = "")
    tag = models.UUIDField(blank = True, null = True, default = None)

    # SETTERS
    def setNumSold(self, newNumSold):
        self.numSold = newNumSold
        self.save()

    def setNumLeft(self, newNumLeft):
        self.numLeft = newNumLeft
        self.save()

    def setName(self, newName):
        self.name = newName
        self.save()

    def setImage(self, newImage):
        self.image = newImage
        self.save()
        
    def setPrice(self, newPrice):
        self.price = newPrice
        self.save()
    
    def setCost(self, newCost):
        self.cost = newCost
        self.save()
    
    def setFandom(self, newFandom):
        self.fandom = newFandom
        self.save()
    
    def setKind(self, newKind):
        self.kind = newKind
        self.save()
        
    def setTag(self, newTag):
        self.tag = newTag
        self.save()
    
    # UTIL
    def clean(self):
        super().clean()
        if self.event == INV_EVENT and self.numSold != 0:
            raise ValidationError({"numSold": ["you can't have a nonzero numSold for the INV_EVENT"]})

    def __str__(self):
        return self.name
        
class MiscCost(ValidatedModel):
    ID = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, related_name = "miscCosts")
    event = models.ForeignKey(Event, related_name = "miscCosts")
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    name = models.CharField(max_length = 50)
    
    # SETTERS
    def setAmount(self, newAmount):
        self.amount = newAmount
        self.save()
        
    def setName(self, newName):
        self.name = newName
        self.save()

    # UTIL
    def clean(self):
        super().clean()
        if self.event == INV_EVENT:
            raise ValidationError({"convention": ["you can't make a miscCost for the INV_EVENT"]})
    
    def __str__(self):
        return "%s spent %s for %s at %s %s" % (self.user, self.amount, self.name, self.event.convention, self.event)

def newUser(username, password, email):
    return User.objects.create_user(username = username, password = password, email = email)

def newWriteup(user, event, rating, review):
    k = Writeup(user = user, event = event, rating = rating, review = review)
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

def newMiscCost(user, event, amount, name):
    k = MiscCost(user = user, event = event, amount = amount, name = name)
    k.save()
    return k

def newItem(user, event, name, fandom, kind, price, cost, numSold, numLeft):
    k = Item(user = user, event = event, name = name, fandom = fandom, kind = kind, price = price, cost = cost, numSold = numSold, numLeft = numLeft)
    k.save()
    return k

def newConvention(name, website):
    k = Convention(name = name, website = website)
    k.save()
    return k

def newEvent(convention, name, startDate, endDate, location):
    k = Event(convention = convention, name = name, startDate = startDate, endDate = endDate, location = location)
    k.save()
    return k


INV_CON = None
INV_EVENT = None
try:
    if Convention.objects.filter(name = "INV_CON").exists():
        INV_CON = Convention.objects.get(name = "INV_CON")
    else:
        INV_CON = newConvention("INV_CON", "https://artistal.ly")
    try:
        INV_EVENT = Event.objects.get(ID = 1)
    except Event.DoesNotExist:
        INV_EVENT = newEvent(INV_CON, "INV_EVENT", datetime.datetime(1, 1, 1), datetime.datetime(1, 1, 1), "artistally")
        assert INV_EVENT.ID == 1
except (OperationalError, ProgrammingError, ImproperlyConfigured):   # django currently migrating
    pass
