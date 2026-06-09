from django.urls import path

from .views import index, login_user, results, detail, vote, flaw_one_delete, add_question, add_new_user

app_name = 'polls'
urlpatterns = [
  path('', index, name='index'),
  path('login/', login_user, name='login'),
  path('add_question/', add_question, name='add_question'),
  path('<int:question_id>/', detail, name='detail'),
  path('<int:question_id>/results/', results, name='results'),
  path('<int:question_id>/vote/', vote, name='vote'),
  path('<int:question_id>/delete/', flaw_one_delete, name='delete'),
  path('register/', add_new_user, name='register'),
]