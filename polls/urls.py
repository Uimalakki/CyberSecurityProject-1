from django.urls import path

from .views import index, results, detail, vote, add


app_name = 'polls'
urlpatterns = [
  path('', index, name='index'),
  path('add/', add, name='add'),
  path('<int:question_id>/', detail, name='detail'),
  path('<int:question_id>/results/', results, name='results'),
  path('<int:question_id>/vote/', vote, name='vote'),
]