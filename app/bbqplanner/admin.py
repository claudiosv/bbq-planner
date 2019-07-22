from django.contrib import admin
from django.contrib.admin import site
# Register your models here.
from .models import Event, MeatType, Visitor, VisitorMeatChoice


class MeatInline(admin.StackedInline):
    """Inline adding meats to event admin"""
    model = MeatType
    extra = 3


class EventAdmin(admin.ModelAdmin):
    """Allow admin to change event name and date, and meats offered"""
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': [
         'event_date'], 'classes': ['collapse']}),
    ]
    inlines = [MeatInline]
    list_display = ('name', 'event_date')
    list_filter = ['event_date']
    search_fields = ['name']


site.site_header = "BBQ Planner"

admin.site.register(Event, EventAdmin)
admin.site.register(MeatType)
admin.site.register(Visitor)
admin.site.register(VisitorMeatChoice)
