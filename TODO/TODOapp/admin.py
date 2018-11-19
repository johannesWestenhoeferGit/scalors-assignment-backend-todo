from django.contrib import admin
from .models import Todo, Board, Reminder

# Making TODOs boards and reminders accessible to the admin panel.

admin.site.register( Todo )
admin.site.register( Board )
admin.site.register( Reminder )