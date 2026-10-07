from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from progress.gamification import ensure_badges_exist
from .seed_data_tutorials import seed_tutorials
from .seed_data_exercises import seed_exercises
from .seed_data_quizzes import seed_quizzes
from .seed_data_projects import seed_projects

class Command(BaseCommand):
    help = "Populate the database with comprehensive Python tutorials, exercises, quizzes, badges, and demo users."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting comprehensive PyMaster database seeding..."))

        with transaction.atomic():
            # 1. Badges
            self.stdout.write("Seeding Gamification Badges...")
            ensure_badges_exist()

            # 2. Tutorials (all 66 topics!)
            seed_tutorials()

            # 3. Exercises & Test cases
            seed_exercises()

            # 4. Quizzes & Questions
            seed_quizzes()

            # 5. Real Python Projects
            seed_projects()

            # 6. Admin & Demo User
            self.stdout.write("Creating Admin & Demo Users...")
            admin_user, admin_created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@pymaster.dev',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            admin_user.set_password('adminpassword123')
            admin_user.save()
            admin_user.profile.update_streak()

            demo_user, demo_created = User.objects.get_or_create(
                username='gowtham',
                defaults={
                    'email': 'gowtham@example.com',
                }
            )
            demo_user.set_password('python123')
            demo_user.save()
            demo_user.profile.update_streak()

        self.stdout.write(self.style.SUCCESS(
            "\nSuccessfully seeded PyMaster database!\n"
            "------------------------------------------\n"
            "Admin Login : admin / adminpassword123\n"
            "Demo Login  : gowtham / python123\n"
            "------------------------------------------"
        ))
