from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from polls.models import Question


class Command(BaseCommand):
    help = "Create demo users and questions"

    def handle(self, *args, **kwargs):
        if User.objects.exists():
            self.stdout.write("Demo data already exists")
            return

        john = User.objects.create_user(username='john', password='salainen')
        maureen = User.objects.create_user(username='maureen', password='salainen')

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

        self.stdout.write(self.style.SUCCESS("Demo data created"))