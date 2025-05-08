from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.db.models import Q
from .models import Profile, Group, Event, HousingListing, Message, Job
from .forms import UserRegistrationForm, EventForm, HousingSearchForm, MessageForm
from .models import Project
from .forms import ProjectForm



def landing_page(request):
    return render(request, 'base/landing_page.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optional auto-login after registration
            return redirect('landing_page')  # change to your homepage if needed
    else:
        form = UserCreationForm()
    
    return render(request, 'base/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('landing_page')  # or dashboard
    
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing_page')  # or wherever you want

    return render(request, 'base/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    events = Event.objects.filter(attendees=profile)
    groups = profile.group_set.all()
    return render(request, 'base/home.html', {'profile': profile, 'events': events, 'groups': groups})

@login_required
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user.profile
            event.save()
            return redirect('dashboard')
    return render(request, 'base/create_event.html', {'form': form})

@login_required
def leave_event(request, event_id):
    event = Event.objects.get(id=event_id)
    profile = request.user.profile
    event.attendees.remove(profile)
    return redirect('events')  # or to a specific event page


def events_list(request):
    events = Event.objects.all()
    return render(request, 'base/events_list.html', {'events': events})

def about_us(request):
    return render(request, 'base/about_us.html')

def contact_us(request):
    return render(request, 'base/contact_us.html')

def layout(request):
    return render(request, 'base/layout.html')

def group_discovery(request):
    query = request.GET.get('q')
    groups = Group.objects.all()
    if query:
        groups = groups.filter(Q(name__icontains=query) | Q(country__icontains=query))
    return render(request, 'base/groups.html', {'groups': groups})


def group_list(request):
    return render(request, 'base/groups.html')

@login_required(login_url='/login/')
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    profile = request.user.profile
    if profile not in group.members.all():
        group.members.add(profile)
    return redirect('group_discovery')

def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    profile = request.user.profile
    group.members.remove(profile)
    return redirect('group_discovery')

def housing_search(request):
    listings = HousingListing.objects.all()
    form = HousingSearchForm(request.GET or None)
    if form.is_valid():
        listings = listings.filter(
            location__icontains=form.cleaned_data['location']
        )
    return render(request, 'base/housing.html', {'form': form, 'listings': listings})

@login_required
def group_chat(request, group_id):
    group = Group.objects.get(id=group_id)
    messages_list = Message.objects.filter(group=group)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = group
            message.sender = request.user.profile
            message.save()
            return redirect('group-chat', group_id=group.id)
    return render(request, 'base/chat.html', {'group': group, 'messages': messages_list, 'form': form})

def home(request):
    return render(request, 'base/home.html', {'room_count': 5})

def create_room(request):
    return render(request, 'base/create_room.html')

def events_page(request):
    return render(request, 'base/events.html')

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'base/projects_list.html', {'projects': projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user.profile
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'base/add_project.html', {'form': form})

@login_required
def add_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            ProjectComment.objects.create(project=project, user=request.user, text=text)
    return redirect('projects')

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user == project.user:
        project.delete()
        return redirect('projects_list')  # or 'projects' if that's your named URL
    else:
        return redirect('projects_list')  # prevent others from deleting


def user_profile(request, pk):
    return render(request, 'base/user_profile.html', {'pk': pk})

# ============== Jobs ==============
def job_search(request):
    jobs = Job.objects.all()
    title = request.POST.get('title', '')
    location = request.POST.get('location', '')
    if title or location:
        jobs = jobs.filter(jobtitle__icontains=title, location__icontains=location)
    return render(request, 'base/job_search.html', {'jobs': jobs})

from django.shortcuts import render, get_object_or_404
from .models import Job

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'base/job_detail.html', {'job': job})


def events_page(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'base/events.html', {'events': events})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = request.user.profile
    event.attendees.add(profile)
    return redirect('events')



