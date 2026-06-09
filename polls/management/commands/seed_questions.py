from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from polls.models import Question

class Command(BaseCommand):
  help = "Create demo questions"

  def handle(self, *args, **kwargs):
    maureen = User.objects.get(username="maureen")
    john = User.objects.get(username="john")

    Question.objects.all().delete()

    Question.objects.create(
      question_text="Favorite movie?",
      pub_date=timezone.now(),
      user=john
    )
    Question.objects.create(
      question_text="Best pizza in town?",
      pub_date=timezone.now(),
      user=john
    )

    Question.objects.create(
      question_text="Worst band in history?",
      pub_date=timezone.now(),
      user=maureen
    )

    Question.objects.create(
      question_text="My favorite mistake?",
      pub_date=timezone.now(),
      user=maureen
    )

    self.stdout.write(self.style.SUCCESS("Demo questions created"))