from django import forms
from .models import Participant, Meetup, Speaker
from django.contrib.auth.forms import UserCreationForm
from .models import myUser


class ParticipantForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['name', 'email']
        

class UserMeetupForm(forms.ModelForm):
    class Meta:
        model =Meetup
        fields=['title', 'from_date',  'to_date', 'meetup_time', 'description', 'organizer_email',  'location_name', 'location_address', 'activate','image',]


class MyUserRegistrationForm(UserCreationForm):
    class Meta:
        model=myUser
        fields= ['name', 'username', 'email', 'password1', 'password2','image' ]


class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields =['name', 'email','phone', 'bio', 'image']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = [ 'name', 'username', 'email', 'bio', 'image', 'phone', 'dod',]