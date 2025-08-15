from django.shortcuts import render, redirect
from .forms import CFARegistrationStep1Form
from .models import CFARegistration

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
    competitions = [
        {
            "title": "Electric Heels",
            "subtitle": "Solo dance comp",
            "date": "Tues, 15.08.",
            "venue": "Mini Audi, IIT Guwahati",
            "image": "core/landing/frame.png",
            "type": "Solo"
        },
        {
            "title": "This is Pop",
            "subtitle": "Pop dance",
            "date": "Wed, 16.08.",
            "venue": "Audi, IIT Guwahati",
            "image": "core/landing/frame.png",
            "type": "Solo"
        },
        {
            "title": "SA RE GA MA",
            "subtitle": "Singing competition",
            "date": "Wed, 16.08.",
            "venue": "Audi, IIT Guwahati",
            "image": "core/landing/frame.png",
            "type": "Group"
        },
        {
            "title": "Footloose",
            "subtitle": "Group dance",
            "date": "Thu, 17.08.",
            "venue": "Main Stage, IIT Guwahati",
            "image": "core/landing/frame.png",
            "type": "Group"
        },
    ]

    return render(request, 'core/comp_page.html', {"competitions": competitions})
