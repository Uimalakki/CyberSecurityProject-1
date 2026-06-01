from django.urls import path

from .views import index, results, detail, vote, add, flaw_one_delete, flaw_one_delete_fix, flaw_three_add_injection, flaw_four_add_new_user, flaw_four_fix_add_new_user


app_name = 'polls'
urlpatterns = [
  path('', index, name='index'),
  path('add/', add, name='add'),
  path('flaw_three_injection/', flaw_three_add_injection, name='flaw_three'),
  path('<int:question_id>/', detail, name='detail'),
  path('<int:question_id>/results/', results, name='results'),
  path('<int:question_id>/vote/', vote, name='vote'),
  path('<int:question_id>/flaw_one_delete/', flaw_one_delete, name='flaw_one_delete'),
  path('<int:question_id>/flaw_one_delete_fix/', flaw_one_delete_fix, name='flaw_one_delete_fix'),
  path('flaw_four_register/', flaw_four_add_new_user, name='register_flaw'),
  path('flaw_four_register_fixed/', flaw_four_fix_add_new_user, name='register_fixed')
]