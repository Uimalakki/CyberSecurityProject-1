from django.urls import path

from .views import index, results, detail, vote, add, flaw_one_delete, flaw_three_add_injection, add_new_user

app_name = 'polls'
urlpatterns = [
  path('', index, name='index'),
  path('add/', add, name='add'),
  path('flaw_three_injection/', flaw_three_add_injection, name='flaw_three'),
  path('<int:question_id>/', detail, name='detail'),
  path('<int:question_id>/results/', results, name='results'),
  path('<int:question_id>/vote/', vote, name='vote'),
  path('<int:question_id>/delete/', flaw_one_delete, name='delete'),
  path('register/', add_new_user, name='register'),
]