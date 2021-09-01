from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup

import sqlite3

@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

#@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
@login_required
def new_poll(request):
    if request.method == "GET":
        return render(request, 'polls/new.html')
    
    description = request.POST.get("description")
    
    poll = Question.objects.create(title=request.POST.get("title"), description=description)
    
    #if has_risky_html(description):
        #return redirect('/polls')
    
    choice_1 = Choice.objects.create(question=poll, choice_text=request.POST.get("choice1"))
    choice_2 = Choice.objects.create(question=poll, choice_text=request.POST.get("choice2"))
    choice_3 = Choice.objects.create(question=poll, choice_text=request.POST.get("choice3"))
    
    poll.save()
    choice_1.save()
    choice_2.save()
    choice_3.save()
    
    return redirect('/polls')

def has_risky_html(text):
    safe_tags = ["strong", "h1", "h2", "h3", "ul", "li", "br", "p"]
    
    soup = BeautifulSoup(text)
    for tag in soup.findAll(True):
        if tag.name not in safe_tags:
            return True
        
    return False

def search(request):
    searched_title = request.GET.get("title")
    
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    
    res = ("SELECT * FROM polls_tasks WHERE title = ")