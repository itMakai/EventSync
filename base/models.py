from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Organizer(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='organizers/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    about = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()  # Add start time
    end_time = models.TimeField()    # Add end time
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/')
    organizers = models.ManyToManyField(Organizer, related_name='events')

    def __str__(self):
        return self.title


    

    def save(self, *args, **kwargs):
        # Automatically generate a slug when saving the product
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"slug": self.slug})
    

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Attendee(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.event.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events_attending = models.ManyToManyField(Event, through='Attendee', related_name='attendees', blank=True)
    notifications = models.ManyToManyField(Notification, related_name='user_notifications', blank=True)

    def __str__(self):
        return self.user.username


class KeyTheme(models.Model):
    name = models.CharField(max_length=100)
    events = models.ManyToManyField(Event, related_name='key_themes')

    def __str__(self):
        return self.name
    
