from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import sqlite3
from django.core.cache import cache

from .models import Question, Choice

# Create your views here.

def rate_limiter(key, limit=5, period=60):
  count = cache.get(key, 0)

  if count >= limit:
    return False
  
  cache.set(key, count + 1, period)
  return True

def user_exists(username):
  if User.objects.filter(username=username).exists():
    return True
  else:
    return False

@login_required
def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {
    'latest_question_list': latest_question_list
  }
  return render(request, 'polls/index.html', context)

def flaw_one_delete(request, question_id):

  # =============================
  # Fix to the flaw 2 2/2
  # ============================= 
  # uncomment lines 47 and 48

  #if request.method != "POST":
  # return HttpResponseForbidden()

  # =============================
  # Fix to the flaw 1:
  # ============================= 
  # uncomment lines 55 - 60 and comment lines 62 and 63

  # deleted_question = get_object_or_404(Question, pk=question_id)
  # if deleted_question.user == request.user:
  #   deleted_question.delete()
  #   return redirect('polls:index')
  # else:
  #   return HttpResponseForbidden("You don't have permission to delete this question")

  Question.objects.get(id=question_id).delete() # comment this line when fix to flaw 1 is impelemented
  return redirect('polls:index') # comment this line when fix to flaw 1 is impelemented

@login_required
def add_question(request):
  if request.method == 'POST':

    question = request.POST.get("question")
    # =============================
    # Fix to the flaw 3: SQL Injection
    # ============================= 
    # Comment lines from 75 to 86 when fix to the flaw 3 is implemented

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM polls_question")
    question_id = int(cursor.fetchone()[0] or 0) + 1
    new_date = '2026-05-27'
    user_id = request.user.id

    cursor.execute(f"INSERT INTO polls_question VALUES ({question_id}, '{question}', '{new_date}', {user_id})")
    
    conn.commit()
    conn.close()

    # =============================
    # Fix to flaw 3
    # ============================= 
    # uncomment the lines 93 and 94

    # new_question = Question.objects.create(question_text=question, pub_date=timezone.now(), user=request.user)
    # new_question.save()

  return redirect('/')

def add_new_user(request):
  if request.method == 'POST':
    username = request.POST.get("username")
    password = request.POST.get('password')

    if user_exists(username):
      return HttpResponseForbidden("Username already exists")
    # =============================
    # Fix to the flaw 4: Identification and Authentication Failures
    # ============================= 

    # uncomment the lines 111 - 114

    # try:
    #  validate_password(password)
    # except ValidationError as e:
    #  return HttpResponseForbidden(", ".join(e.messages))

    User.objects.create_user(username=username, password=password)
    return redirect('polls:index')

  return render(request, 'polls/register.html')

@login_required
def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'polls/detail.html', {'question': question})

@login_required
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice']) # type: ignore
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
  

def login_user(request):

  if request.method == 'POST':
    username = request.POST.get("username")
    key = f"login-{username}"

    # =============================
    # Fix to flaw 5
    # ============================= 
    # uncomment the lines 159 - 162

    # if not rate_limiter(key):
    #   return HttpResponseForbidden(
    #     "Too many login attempts. Try again later."
    #   )
    
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      cache.delete(key)

      return redirect('polls:index')
    
    return render(
      request,
      "polls/login.html",
      {"error": "Invalid username or password"}
    )
  return render(request, 'polls/login.html')

@login_required
def add_choice(request, question_id):

  if request.method == 'POST':

    question = get_object_or_404(Question, pk=question_id)
    choice = request.POST.get('new_choice')
    
    question.choice_set.create(choice_text=choice, votes=0) # type: ignore
    
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

  return render(request, 'polls:results')

  