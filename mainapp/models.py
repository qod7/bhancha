from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Media(models.Model):
    '''
    Represents the image file as media
    It processes and saves the media file in fixed
    size upon saving.
    '''
    image = models.ImageField()
    description = models.CharField(max_length=1000, default=' ')

    def save(self, size=(200, 200)):
        """
        Save Photo after ensuring it is not blank.  Resize as needed.
        """
        from bhancha import settings

        if not self.image:
            return

        super(Media, self).save()

        filename = settings.MEDIA_ROOT+"/"+self.image.name
        image = Image.open(filename)
        width, height = image.size
        if height > width:
            ratio = height/width

            image.thumbnail((200, 200*ratio), Image.ANTIALIAS)
        else:
            ratio = width/height
            image.thumbnail((200*ratio, 200), Image.ANTIALIAS)
        image.save(filename)

    def showimage(self):
        return '<img src="/media/'+self.image.name+'"/>'
    showimage.allow_tags = True

    def geturl(self):
        '''
        Returns the URL of the media file
        '''
        pass

    def __str__(self):
        return self.description


class Food(models.Model):
    '''
    This model represents the food
    '''
    name = models.CharField(max_length=30)
    image = models.ForeignKey(Media)

    def __str__(self):
        return self.name


class Dish(models.Model):
    '''
    This represent certain dish that is cooked by certain cook
    '''
    cook = models.ForeignKey(User)
    food = models.ForeignKey(Food)
    enabled = models.BooleanField(default=False)
    price = models.IntegerField(default=100)

    def __str__(self):
        return self.food.name+" by "+self.cook.first_name+" "+self.cook.last_name


class CookInfo(models.Model):
    '''
    This class stores any extra information for the cook
    '''

    cook = models.ForeignKey(User)
    rating = models.FloatField(default=0.0)

    BUSY = "BUSY"
    FREE = "FREE"

    STATUS_CHOICES = (
        (BUSY, "Busy"),
        (FREE, "Free")
    )

    status = models.CharField(max_length=4,
                              choices=STATUS_CHOICES,
                              default=BUSY)

    def __str__(self):
        return "Cook info for "+self.cook.first_name+" "+self.cook.last_name


class Order(models.Model):
    ORDERED = "ORD"
    COOKING = "CKN"
    DELIVERING = "DLI"
    DELIVERED = "DLV"

    ORDER_STATUS = (
        (ORDERED, "Ordered"),
        (COOKING, "Cooking"),
        (DELIVERING, "Delivering"),
        (DELIVERED, "Delivered")
    )

    customer = models.ForeignKey(User)
    dish = models.ForeignKey(Dish)
    quantity = models.IntegerField(default=1)

    status = models.CharField(max_length=4,
                              choices=ORDER_STATUS,
                              default=ORDERED)

    accepted = models.NullBooleanField(blank=True)
    order_placed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order by "+self.customer.first_name+" "+self.customer.last_name+" for "+self.dish.__str__()


class Session(models.Model):
    user = models.ForeignKey(User)
    sessionid = models.CharField(max_length=20, default='', unique=True)

    def generateRandom(self):
        from django.db import IntegrityError
        from django.utils.crypto import get_random_string

        self.sessionid = get_random_string(length=20)
        success = False
        while not success:
            try:
                self.save()
            except IntegrityError:
                self.sessionid = get_random_string(length=16)
            else:
                success = True

    def __str__(self):
        return "Session for "+self.user.first_name+" "+self.user.last_name
