from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meetup, Participant, myUser, Speaker
from django.db.models import Q
from django.views.generic import UpdateView, CreateView, DeleteView
from .forms import ParticipantForm, UserMeetupForm, MyUserRegistrationForm, SpeakerForm, ProfileForm
from django.urls import reverse_lazy
from string import punctuation
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.



def loginPage(request):
    page='Login'
    if request.user.is_authenticated:
        return redirect('home')
    #when submit botti=on is pressed 
    if request.method=='POST':  
        email = request.POST.get('email')
        email.lower()
        password = request.POST.get('password')
        try:
            user=myUser.objects.get(email=email)  
        except:
            messages.error(request, 'User does not exist')
        user=authenticate(request, email=email, password=password)
        if user is not None:
          login(request, user)
          return redirect ('home')
        else:
          messages.error(request, 'Invalid credential')
    context={'page':page}

    return render(request, 'meetup/login.html', context)

def index(request):
    # q=request.GET.get('q')
    # if(q!=None):
    #     return q
    # else:
    #     ''  
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    meetups=Meetup.objects.filter(activate=True)
    meetups=meetups.filter(
        Q(title__icontains=q)
    )
    count=meetups.count
    return render(request, 'meetup/home.html', {'meetups':meetups, "count":count})

def contact(request):
    return HttpResponse('<h1>This is my contact in django</h1>')



def register(request):
    page='Register'
    form=MyUserRegistrationForm()
    context={'form':form,  'page':page}

    if request.method == 'POST':
        form = MyUserRegistrationForm(request.POST,  request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            #email=user.email
            user.save()
            #send_mail('Thanks for registering','Thanks For Registering, we will get i touch with you soon..', settings.EMAIL_HOST_USER, [ email,])
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
           
    return render(request, 'meetup/register.html',context )


def meetup_details(request, meetup_slug):
   # selected_meetup=Meetup.objects.get(slug=meetup_slug)
    try:
        selected_meetup=Meetup.objects.get(slug=meetup_slug)
        speakers=selected_meetup.meetup_speakers.all
        if request.method=='GET':
            registration_form=ParticipantForm()
        else:
            registration_form= ParticipantForm(request.POST)
            if registration_form.is_valid():
                participant=registration_form.save()
                selected_meetup.participant.add(participant)
                return redirect('confirm-registration')
                
        return render(request, 'meetup/meetup_details.html', {
         'meet_found':True,
         'meetup':selected_meetup,
         'form': registration_form ,
         'speakers':speakers, 

          })    
   
    except Exception as exc:
        return render(request, 'meetup/meetup_details.html', {
         'meet_found':False,
         
     })


class MeetupUpdate(UpdateView):
    model=Meetup
    form_class=UserMeetupForm
    template_name='meetup/meetup_form.html'
    success_url=reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(MeetupUpdate, self).form_valid(form)



#Creating meetup
class MeetupsCreate(CreateView):
    model=Meetup
    form_class = UserMeetupForm
    #exclude=[]
    success_url=reverse_lazy('home')
    template_name='meetup/meetup_form.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        for i in punctuation:
            title=form.instance.title.replace(i, ' ')
        form.instance.slug=title.replace(' ', '-')
        return super(MeetupsCreate, self).form_valid(form)
    
def confirmReg(request):
    return render(request, 'meetup/confirmReg.html')
    


def user_meetups(request, pk):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    
    user_meetups=Meetup.objects.order_by('-create')
    user_meetups=Meetup.objects.filter(user=pk)
    meetups=user_meetups.filter(
        Q(title__icontains=q)
    )
    count=meetups.count
    return render(request, 'meetup/user_meetups.html', {'meetups':meetups, 'count':count} )


#Delete Meetups
class MeetupDelete(DeleteView):
    model=Meetup
    context_object_name='meetup'
    template_name='meetup/delete_meetup.html'
    success_url=reverse_lazy('home')
    
    
def participants(request, meetupId):
    meetup=Meetup.objects.get(id=meetupId)
    participants=meetup.participant.all()
    participants=participants.order_by('-id')
    count=participants.count()
    
    return render(request, 'meetup/participants.html', {'participants':participants, 'count':count} )


def speakers(request, meetupId):
    meetup=Meetup.objects.get(id=meetupId)
    speakers=meetup. meetup_speakers.all()
    speakers=speakers.order_by('-id')
    count=speakers.count()
    
    return render(request, 'meetup/speakers.html', {'speakers':speakers, 'count':count} )
# Add speakers to meetup
# @login_required(login_url='login')
def add_speakers(request, meetup_slug):
   # selected_meetup=Meetup.objects.get(slug=meetup_slug)
    try:
        selected_meetup=Meetup.objects.get(slug=meetup_slug)
        
        if request.method=='GET':
            add_speaker_form=SpeakerForm()
        else:
           
            add_speaker_form= SpeakerForm(request.POST, request.FILES)
            if add_speaker_form.is_valid():
                add_speaker_form.instance.user=request.user
                
                speaker=add_speaker_form.save(commit=False)
                add_speaker_form.instance.meetup_name=selected_meetup.title
                speaker=add_speaker_form.save()
                selected_meetup.meetup_speakers.add(speaker)
                return redirect('home')
              
        return render(request, 'meetup/add_speaker.html', {
         'meet_found':True,
         'meetup':selected_meetup,
         'page':False, 
         'form': add_speaker_form ,
         

          })    
   
    except Exception as exc:
        return render(request, 'meetups/add_speakers.html', {
         'meet_found':False,
         
     })


# #speakers update
# LoginRequiredMixin, 
class SpeakerUpdate(UpdateView):
    model=Speaker
    form_class = SpeakerForm
    template_name='meetup/add_speaker.html'
    success_url=reverse_lazy('home')
    
    
#     def form_valid(self, form):
#         form.instance.user=self.request.user
#         return super(SpeakerUpdate, self).form_valid(form)
    
# #Delete Speakers
class SpeakerDelete(DeleteView):
    model=Speaker
    context_object_name='speaker'
    template_name='meetup/delete_speaker.html'
    success_url=reverse_lazy('home')
    
# @login_required(login_url='login')
def profile(request, pk):
    page="Profile"
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context={'form':form, 'page':page}
    return render(request, 'meetup/profile_form.html', context)
#contact
