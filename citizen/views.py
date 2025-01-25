from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from citizen.models import Abakandida, Citizens, Events, Family, Post, Votes
from core.models import Stories
from .forms import *
from django.db.models import Count
from collections import defaultdict

# def index(request):
#     if not request.user.is_authenticated:
#         return redirect('/')
    
#     grouped_by_gender = Family.objects.get(user=request.user).members.values('gender').annotate(count=Count('gender'))
#     recent_events = Events.objects.all().order_by('-created')[:3]
#     messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]
#     context = {
#         'grouped_by_gender': grouped_by_gender,
#         'recent_events': recent_events,
#         'messages_all': messages_all
#     }
#     return render(request, 'citizen/pages/index.html', context)

def index(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    # Attempt to get the Family object associated with the logged-in user
    try:
        family = Family.objects.get(user=request.user)
        grouped_by_gender = family.members.values('gender').annotate(count=Count('gender'))
    except Family.DoesNotExist:
        # Handle the case where no Family object exists for the user
        grouped_by_gender = []

    # Fetch recent events
    recent_events = Events.objects.all().order_by('-created')[:3]
    
    # Fetch the most recent messages sent by the user
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]
    
    # Prepare the context to pass to the template
    context = {
        'grouped_by_gender': grouped_by_gender,
        'recent_events': recent_events,
        'messages_all': messages_all, 
    }
    
    # Render the index page with the context
    return render(request, 'citizen/pages/index.html', context)

def family(request):
    
    family_members = Family.objects.filter(user=request.user).first()
    print(family_members)
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]

    

    context = {
        'family_members': family_members,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/family.html', context)

def family_single(request, id):
    member = Family.objects.get(user=request.user).members.filter(id=id).first()
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]

    context = {
        'member': member,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/family-single.html', context)

def family_member_delete(request, id):
    member_object = Family.objects.get(user=request.user).members.filter(id=id).first()
    member_object.delete()
    messages.success(request, 'Byagenze neza!')
    return redirect('citizen-family')

def family_member_add(request):
    family_object = Family.objects.filter(user=request.user).first()
    form = NewMemberForm(request.POST or None, request.FILES or None)
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        family_object.members.add(instance)
        family_object.save()
        messages.success(request, 'Umunyamuryango yongewemo!')
        return redirect('citizen-family')

    context = {
        'form': form,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/family-member-add.html', context)

def family_member_edit(request, id):
    family_member_object = Family.objects.get(user=request.user).members.filter(id=id).first()
    form = NewMemberForm(request.POST or None, request.FILES or None, instance=family_member_object)
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Umunyamuryango yahinduwe neza!')
        return redirect('citizen-family')

    context = {
        'form': form,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/family-member-edit.html', context)


######### Messaging ############

def all_messages(request):
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')
    context = {
        'messages_all': messages_all,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/messages-all.html', context)

def new_message(request):
    form = MessageForm(request.POST or None)
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]

    if form.is_valid():
        message_obj = form.save(commit=False)
        message_obj.sender = request.user
        message_obj.save()
        messages.success(request, 'Ubutumwa bwagiye!')
        return redirect('messages-all')
    context = {
        'form': form,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/new_message.html', context)



######### Events ############

def events(request):    
    available_events = Events.objects.all()
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]

    context = {
        'available_events': available_events,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/events.html', context)

def event_single(request, id):
    event = Events.objects.get(id=id)
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]

    context = {
        'event': event,
        'messages_all': messages_all

    }
    return render(request, 'citizen/pages/event-single.html', context)


######### Ikuru z'amateka ###############

def historyView(request):
    stories = Stories.objects.all()
    context = {
        'stories': stories
    }
    return render(request, 'citizen/pages/stories.html', context)

# Profile

def profile(request):
    profileform = ProfileForm(instance=request.user)
    messages_all = Messages.objects.filter(sender=request.user).order_by('-created')[:5]

    context = {}
    if request.method == 'POST':
        formdata = ProfileForm(request.POST)
        if formdata.is_valid():
            print(formdata)
            # request.user.first_name = formdata['first_name']
            # request.user.gender = formdata['gender']
            # request.user.save()
            # return redirect(request.path_info)
    context['profileform'] = profileform
    context['messages_all'] = messages_all
    return render(request, 'citizen/pages/profile.html', context)

######### Amatora ###############
def voting_all(request):
    posts_all = Abakandida.objects.select_related('post')
    print(posts_all)
    categorized_posts = defaultdict(list)
    for item in posts_all:
        categorized_posts[item.post].append(item)

    context = {
        'categorized_posts': dict(categorized_posts)
    }

    return render(request, 'citizen/pages/voting-all.html', context)

def voting_single(request, id):
    post = get_object_or_404(Post, id=id)
    members = Abakandida.objects.filter(post=post)
    try:
        already_vote_object = get_object_or_404(Votes, user=request.user, post=post)
    except:
        already_vote_object = None

    context = {
        'post': post,
        'members': members,
        'already_vote_object': already_vote_object
    }
    return render(request, 'citizen/pages/voting-single.html', context)

def vote_increase(request):
    member = get_object_or_404(Abakandida, id=request.POST['member_id'])
    member.votes+=1
    member.save()

    Votes.objects.create(
        user=request.user,
        post=Post.objects.get(id=request.POST['post_id'])
    )
    messages.success(request, 'Gutora byagenze neza')
    return redirect("voting-all")

def kwimuka(request):
    form = KwimukaForm(request.POST or None)
    kwimuka_objects = Kwimuka.objects.filter(user=request.user).order_by('-created')
    try:
        current_kwimuka_obj = Kwimuka.get_latest_for_user(request.user)
    except:
        current_kwimuka_obj = None
        
    if current_kwimuka_obj is not None and not current_kwimuka_obj.approve and not current_kwimuka_obj.cancelled:
        form = None

    if form is not None and form.is_valid():
        kwimuka_obj = form.save(commit=False)
        kwimuka_obj.user = request.user
        kwimuka_obj.save()
        messages.success(request, 'Request sent!')
        return redirect(request.path_info)

    context = {
        'form': form,
        'current_kwimuka_obj': current_kwimuka_obj,
        'kwimuka_objects': kwimuka_objects
    }
    return render(request, "citizen/pages/kwimuka.html", context)

def cancelKwimuka(request, id):
    kwimuka_object = get_object_or_404(Kwimuka, id=id)
    kwimuka_object.cancelled = True
    kwimuka_object.save()
    messages.success(request, 'Success!')
    return redirect('kwimuka')