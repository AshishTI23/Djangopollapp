from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', admin.site.urls),
    # path('',include('regLogin.urls')),
    # path('',include('pollapp.urls')),
    path('poll-list/',views.PollList,name = "PollList"),
    path('delete/<int:poll_id>/',views.DeletePoll,name = "DeletePoll"),
    path('<int:poll_id>/',views.VotePoll,name = "VotePoll"),
    path('view/<int:question_id>/',views.viewVote,name = "ViewVotes"),
    path('newpoll/',views.Newpoll,name = 'newpoll')

]
