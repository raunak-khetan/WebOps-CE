from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Event, Head, TeamMember, Team
from .forms import RegistrationForm, TeamName, MemberForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from .forms import CFARegistrationStep1Form
from .models import CFARegistration
from .models import City, Event
from django.http import HttpResponse



def city_list(request):
    cities = City.objects.all().values('name')  # Query to get city names
    return JsonResponse(list(cities), safe=False)


def get_city_events(request, city_name):
    # Retrieve the City instance based on the slug or name
    # If using slug:
    # city = get_object_or_404(City, slug=city_name)
    # If using name:
    city = get_object_or_404(City, name=city_name)

    # Access the related events
    events = city.events.all()

    # Serialize events data
    data = {
        'time': city.time.strftime('%d %b %Y'),  # Format the date as desired
        'events': [
            {
                'name': event.name,
            }
            for event in events
        ]
    }

    return JsonResponse(data)


def prelimspage(request):
    cities = City.objects.all().prefetch_related('events')
    first_reg_url = None
    for c in cities:
        first_event = c.events.first()
        if first_event:
            try:
                first_reg_url = reverse('registrationpage', args=[
                                        c.name, first_event.name])
            except Exception:
                first_reg_url = None
            break
    return render(request, 'core/home.html', {'cities': cities, 'first_reg_url': first_reg_url})


def citypage(request, city_name):
    city = get_object_or_404(City, name=city_name)
    cities = City.objects.all()
    events = city.events.all()
    return render(request, 'core/compitition.html', {'events': events, 'curr_city': city, 'cities': cities})


def has_registered(email, event):
    """ Helper function to check if a user has already registered for the event. """
    return Head.objects.filter(email=email, event=event).exists()


def detailspage(request, city_name, event_name):
    city = get_object_or_404(City, name=city_name)
    event = get_object_or_404(Event, name=event_name)

    return render(request, 'core/register.html', {
        'event': event,
        'city': city,
    })


def registrationpage(request, city_name, event_name):
    city = get_object_or_404(City, name=city_name)
    event = get_object_or_404(Event, name=event_name)

    # Create a formset for multiple team members
    MemberFormSet = modelformset_factory(
        TeamMember,
        form=MemberForm,
        extra=0
    )  # Use custom form to ensure radio gender without blank option

    if request.method == 'POST':
        if event.event_type == 'team':
            team_name_form = TeamName(request.POST)
            team_form = RegistrationForm(request.POST)
            member_formset = MemberFormSet(request.POST, prefix='members')
            print(member_formset)

            if team_name_form.is_valid() and team_form.is_valid() and member_formset.is_valid():
                # Check if the team has already registered for this event
                # Save the team registration
                team_head = team_form.save(commit=False)
                team_head.event = event
                team_head.city = city
                team_head.save()

                team_name = team_name_form.save(commit=False)
                team_name.head = team_head
                team_name.save()

                # Save each team member
                for form in member_formset:
                    if form.cleaned_data:  # Save only if the form has data
                        member = form.save(commit=False)
                        member.head = team_head
                        member.team = team_name
                        member.save()

                send_mail(
                    subject='Team Registration Successful',
                    message=f'Hello {team_head.name},\n\nYou have successfully registered your team for the event "{event.name}" in {city.name}.\n\nThank you for registering!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[team_head.email],
                    fail_silently=False,
                 )

                return render(request, 'core/thank_you.html')

        else:  # Handle solo registration
            form = RegistrationForm(request.POST)
            if form.is_valid():
    
                # Save the solo registration
                registration = form.save(commit=False)
                registration.event = event
                registration.city = city
                registration.save()

                send_mail(
                    subject='Registration Successful',
                    message=f'Hello {registration.name},\n\nYou have successfully registered for the event "{event.name}" in {city.name}.\n\nThank you for registering!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[registration.email],
                    fail_silently=False,
                )
                
                return render(request, 'core/thank_you.html')

    else:
        if event.event_type == 'team':
            team_name_form = TeamName()
            team_form = RegistrationForm()
            member_formset = MemberFormSet(queryset=TeamMember.objects.none(), prefix='members')
        else:
            form = RegistrationForm()
            team_name_form = None
            team_form = None
            member_formset = None

    return render(request, 'core/register_form.html', {
        'form': form if event.event_type == 'solo' else team_form,
        'team_name_form': team_name_form,
        'event': event,
        'city': city,
        'member_formset': member_formset,
        'min_participants': event.min_participants,
        'max_participants': event.max_participants,
    })

def cfa_register_step1(request):
    if request.method == 'POST':
        form = CFARegistrationStep1Form(request.POST)
        if form.is_valid():
            cfa = form.save(commit=False)
            cfa.save()
            # Save the ID to session for next step
            request.session['cfa_id'] = cfa.id
            return redirect('cfa_step2')
    else:
        form = CFARegistrationStep1Form()

    return render(request, 'core/cfa_step1.html', {'form': form})


def cfa_step2_view(request):
    if request.method == 'POST':
        college_name = request.POST.get('college_name')

        # Get existing CFA object
        cfa_id = request.session.get('cfa_id')
        if cfa_id:
            cfa = CFARegistration.objects.get(id=cfa_id)
            cfa.college_name = college_name
            cfa.save()

        # Redirect to step 3
        return redirect('cfa_step3')

    return render(request, 'core/cfa_step2.html')


def cfa_step3(request):
    if request.method == 'POST':
        # Handle form submission here
        # You can access fields using request.POST.get('field_name')
        team_size = request.POST.get('team_size')
        fest_address = request.POST.get('fest_address')
        expectations = request.POST.get('expectations')
        competitions = request.POST.get('competitions')

        # Optionally, save the data or process it...

        # For now, redirect to a thank you or confirmation page
        return render(request, 'core/thank_you.html')  # or use redirect()

    return render(request, 'core/cfa_step3.html')



def comp_page(request):
    print("comp_page view called")  # DEBUG

    competitions = []

    cities = City.objects.prefetch_related('events').all()
    print(f"Fetched {cities.count()} cities")  # DEBUG

    for city in cities:
        print(f"City: {city.name}, Events: {city.events.count()}")  # DEBUG
        for event in city.events.all():
            competitions.append({
                "city": city.name,
                "title": event.name,
                "subtitle": event.description,
                "date": city.time.strftime("%a, %d.%m.") if city.time else "No date",
                "venue": city.venue,
                "image": city.image.url if city.image else '',
                "type": event.event_type.capitalize() if event.event_type else "N/A"
            })

    print(f"Competitions list length: {len(competitions)}")  # DEBUG
    return render(request, 'core/comp_page.html', {"cities": cities})


