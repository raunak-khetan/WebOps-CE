from django.shortcuts import render, redirect
from .forms import CFARegistrationStep1Form
from .models import CFARegistration
from .models import City, Event
from django.http import HttpResponse


def landing_page(request):
    return render(request, 'core/landing.html')

def about_alcher(request):
    return render(request, 'core/about.html')

def cfa_register_page(request):
    return render(request, 'core/cfa_register.html')

def cfa_register_step1(request):
    if request.method == 'POST':
        form = CFARegistrationStep1Form(request.POST)
        if form.is_valid():
            cfa = form.save(commit=False)
            cfa.save()
            request.session['cfa_id'] = cfa.id  # Save the ID to session for next step
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


