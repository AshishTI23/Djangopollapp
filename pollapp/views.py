from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . models import MakePoll, Vote
from django.contrib import messages
# Create your views here.
def PollList(request):
    polls = MakePoll.objects.all()
    return render(request,'pollapp/listpoll.html',{'polls':polls})

def VotePoll(request,poll_id):
    if request.method == "POST":
        data = MakePoll.objects.get(id = poll_id)
        selected_Question = data.question
        selected_Choice = request.POST['vote']
        Vote.objects.create(poll = data,vote = selected_Choice).save()
        return redirect('PollList')
    else:
        requested_poll = MakePoll.objects.get(id = poll_id)
        return render(request,'pollapp/votepoll.html',{'poll':requested_poll})

def viewVote(request,question_id):
    if request.user.is_authenticated:
        question = MakePoll.objects.get(id = question_id)
        all_votes = Vote.objects.filter(poll = question)
        voteForOption1 = Vote.objects.filter(poll = question,vote = question.optionone).count()
        voteForOption2 = Vote.objects.filter(poll = question,vote = question.optiontwo).count()
        voteForOption3 = Vote.objects.filter(poll = question,vote = question.optionthree).count()
        voteForOption4 = Vote.objects.filter(poll = question,vote = question.optionfour).count()
        total = voteForOption1 + voteForOption2 + voteForOption3 + voteForOption4
        if total == 0:
            total = 100
        else:
            total = total
        context = {
            'total': total,
            'question':question,
            'all_votes':all_votes,
            'voteForOption1':voteForOption1,'percentage1': round((voteForOption1*100)/total, 2),
            'voteForOption2':voteForOption2,'percentage2': round((voteForOption2*100)/total, 2),
            'voteForOption3':voteForOption3,'percentage3': round((voteForOption3*100)/total, 2),
            'voteForOption4':voteForOption4,'percentage4': round((voteForOption4*100)/total, 2),
        }
        return render(request,'pollapp/viewVotes.html',context)

def DeletePoll(request,poll_id):
    if request.user.is_authenticated:
        pollobject = MakePoll.objects.filter(id=poll_id)
        MakePoll.objects.get(id = poll_id).delete()
        return redirect('signedIn')


def Newpoll(request):
    if request.method == "POST":
        owner = request.user.username
        question = request.POST.get('Question')
        optionone = request.POST.get('first_option')
        optiontwo = request.POST.get('second_option')
        optionthree = request.POST.get('third_option')
        optionfour = request.POST.get('fourth_option')
        owner = User.objects.get(username = owner)
        MakePoll.objects.create(owner=owner,question=question,optionone=optionone,optiontwo=optiontwo,optionthree=optionthree,optionfour=optionfour).save()
        return redirect('signedIn')
    else:
        return render(request,'pollapp/makepoll.html')
