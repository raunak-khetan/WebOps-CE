from django.contrib import admin
from .models import City, Event, Head, Team, TeamMember
from .models import CFARegistration
from .models import AboutImage

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1  # Number of extra empty forms to show by default
    raw_id_fields = ('head',)  # Use raw_id fields for large databases


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'time', 'state')
    search_fields = ('name', 'venue', 'state')
    list_filter = ('state', 'time')
    filter_horizontal = ('events',)
    fieldsets = (
        (None, {
            'fields': ('name', 'venue', 'state', 'time', 'image')
        }),
        ('Details', {
            'fields': ('guidelines', 'events'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'min_participants', 'max_participants', 'deadline', 'event_date')
    list_filter = ('event_type', 'deadline', 'event_date')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'event_type', 'description')
        }),
        ('Participants', {
            'fields': ('min_participants', 'max_participants')
        }),
        ('Important Dates', {
            'fields': ('deadline', 'event_date')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.event_type == 'solo':
            return ['min_participants', 'max_participants']
        return []


@admin.register(Head)
class HeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'city', 'email', 'phone_no', 'institute_name', 'year_of_passing', 'solo')
    list_filter = ('gender', 'city', 'event', 'year_of_passing', 'is_disabled', 'solo')
    search_fields = ('name', 'email', 'phone_no', 'institute_name')
    raw_id_fields = ('event', 'city')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_no', 'gender', 'is_disabled')
        }),
        ('Academic Information', {
            'fields': ('institute_name', 'year_of_passing', 'program_enrolled')
        }),
        ('Event Information', {
            'fields': ('event', 'city', 'solo')
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'head', 'created_at')
    search_fields = ('team_name', 'head__name')
    list_filter = ('created_at',)
    raw_id_fields = ('head',)
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'team', 'phone_no', 'email', 'gender', 'institute_name', 'year_of_passing', 'program_enrolled', 'is_disabled')
    list_filter = ('gender', 'year_of_passing', 'is_disabled')
    search_fields = ('name', 'phone_no', 'email', 'head__name', 'team__team_name', 'institute_name')
    raw_id_fields = ('head', 'team')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_no', 'gender', 'is_disabled')
        }),
        ('Academic Information', {
            'fields': ('institute_name', 'year_of_passing', 'program_enrolled')
        }),
        ('Team Information', {
            'fields': ('head', 'team')
        }),
    )


@admin.register(CFARegistration)
class CFARegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'college_name', 'fest_name', 'submitted_at')
    search_fields = ('full_name', 'email', 'college_name', 'fest_name')
    list_filter = ('college_designation', 'accommodation_required', 'submitted_at')
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'age', 'email', 'phone_number', 'alternate_phone', 'college_id_card_link')
        }),
        ('College Information', {
            'fields': ('college_name', 'college_designation')
        }),
        ('Fest Information', {
            'fields': ('fest_name', 'fest_address', 'fest_dates', 'number_of_days', 'expected_footfall', 'social_links')
        }),
        ('Additional Details', {
            'fields': ('accommodation_required', 'event_preferences')
        }),
        ('Timestamps', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )

#bug fixes...
@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'image']
    ordering = ['order']