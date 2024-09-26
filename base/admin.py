from django.contrib import admin
from .models import Event,KeyTheme, Ticket, Attendee, Notification, UserProfile, Category, Organizer

class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'price', 'quantity_available')

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'event', 'ticket', 'registration_date')

class KeyThemeInline(admin.TabularInline):
    model = KeyTheme.events.through  # Create an inline display for KeyThemes related to Event
    extra = 1

class OrganizerInline(admin.TabularInline):
    model = Event.organizers.through  # This allows you to manage organizers in the event admin
    extra = 1  # Number of empty rows to display for adding new organizers

class EventAdmin(admin.ModelAdmin):
    inlines = [KeyThemeInline]
    inlines = [OrganizerInline]  # Add inline for organizers
    list_display = ('title', 'description', 'about', 'date', 'location')
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('organizers',)  # Exclude direct Many-to-Many field management

class KeyThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')


admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(KeyTheme, KeyThemeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
