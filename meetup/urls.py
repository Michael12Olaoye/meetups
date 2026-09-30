from . import views
from .views import MeetupUpdate, MeetupsCreate, MeetupDelete, SpeakerUpdate, SpeakerDelete
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('',  views.index, name='home'),
      path('user-meetups/<str:pk>',  views.user_meetups, name='user-meetups'),
    path('meetups/<slug:meetup_slug>', views.meetup_details, name="meetup-details"),   
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/',  views.loginPage, name='login'),
    path('register/',  views.register, name='register'),
    
    path('user-profile/<int:pk>', views.profile, name="user-profile"),
    path('meetup/confirm',  views.confirmReg, name='confirm-registration'),
    path('meetup-update/<int:pk>', MeetupUpdate.as_view(), name="meetup-update"),
    path('meetup-delete/<int:pk>', MeetupDelete.as_view(), name="meetup-delete"),
    path('create-meetup/', MeetupsCreate.as_view(), name="meetup-create"),
    path('meetup-participants/<int:meetupId>',  views.participants, name='meetup-participants'),
    path('add-speaker/<slug:meetup_slug>',  views.add_speakers, name='add-speaker'),
     path('meetup-speakers/<int:meetupId>',  views.speakers, name='meetup-speakers'),
    path('speaker-update/<int:pk>', SpeakerUpdate.as_view(), name="speaker-update"),
       path('speaker-delete/<int:pk>', SpeakerDelete.as_view(), name="speaker-delete"),
    path("contact/", views.contact)
    
    
]

