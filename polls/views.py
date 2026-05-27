from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.db import connection
import sqlite3

from .models import Question, Choice

# Create your views here.

@login_required
def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {
    'latest_question_list': latest_question_list
  }
  return render(request, 'polls/index.html', context)

def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'polls/detail.html', {'question': question})

def add(request):
  if(request.method == 'POST'):
    print(request.POST)
    question = request.POST.get('question')
    new_question = Question.objects.create(question_text=question, pub_date=timezone.now(), user=request.user)
    new_question.save()

  return redirect('/')

def flaw_three_add_injection(request):
  if request.method == 'POST':
    question = request.POST.get("question")
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM polls_question")
    question_id = int(cursor.fetchone()[0]) + 1
    new_date = '2026-05-27'
    user_id = request.user.id

    cursor.execute(f"INSERT INTO polls_question VALUES ({question_id}, '{question}', '{new_date}', {user_id})")
    
    conn.commit()
    conn.close()

  return redirect('/')


def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', {'question': question})

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

    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
  
def flaw_one_delete(request, question_id):
  Question.objects.get(id=question_id).delete()
  return redirect('polls:index')

def flaw_one_delete_fix(request, question_id):

  deleted_question = get_object_or_404(Question, pk=question_id)

  if deleted_question.user == request.user:
    deleted_question.delete()
    return redirect('polls:index')
  else:
    return HttpResponseForbidden("You don't have permission to delete this question")
  