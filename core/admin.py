from django.contrib import admin
from .models import City, Event, Head, Team, TeamMember

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1  # Number of extra empty forms to show by default
    raw_id_fields = ('head',)  # Use raw_id fields for large databases

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('events',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'min_participants', 'max_participants', 'description')
    list_filter = ('event_type',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'event_type', 'min_participants', 'max_participants', 'description')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.event_type == 'solo':
            return ['min_participants', 'max_participants']
        return []

@admin.register(Head)
class HeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'city', 'email', 'phone_no', 'solo')
    list_filter = ('gender', 'city', 'event')
    search_fields = ('name', 'email', 'phone_no')
    raw_id_fields = ('event', 'city')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'head', 'created_at')
    search_fields = ('team_name', 'head__name')
    raw_id_fields = ('head',)
    inlines = [TeamMemberInline]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'phone_no', 'email', 'gender', 'institute_name', 'year_of_passing')
    list_filter = ('gender', 'year_of_passing')
    search_fields = ('name', 'phone_no', 'email', 'head__name')
    raw_id_fields = ('head',)
