from django.urls import path

from .views import index, results, detail, vote, add, flaw_one_delete, flaw_one_delete_fix


app_name = 'polls'
urlpatterns = [
  path('', index, name='index'),
  path('add/', add, name='add'),
  path('<int:question_id>/', detail, name='detail'),
  path('<int:question_id>/results/', results, name='results'),
  path('<int:question_id>/vote/', vote, name='vote'),
  path('<int:question_id>/flaw_one_delete/', flaw_one_delete, name='flaw_one_delete'),
  path('<int:question_id>/flaw_one_delete_fix/', flaw_one_delete_fix, name='flaw_one_delete_fix')
]