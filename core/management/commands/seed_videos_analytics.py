import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from tutorials.models import TutorialCategory, VideoTutorial
from core.models import PageView

class Command(BaseCommand):
    help = "Seeds initial video tutorials and realistic page view analytics for graphs demonstration."

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample video tutorials and analytics data...")

        # 1. Sample Video Tutorials
        categories = list(TutorialCategory.objects.all())
        cat_basics = TutorialCategory.objects.filter(slug='python-basics-setup').first() or (categories[0] if categories else None)
        cat_loops = TutorialCategory.objects.filter(slug='loops-iterations').first() or (categories[1] if len(categories) > 1 else None)
        cat_oop = TutorialCategory.objects.filter(name__icontains='OOP').first() or (categories[2] if len(categories) > 2 else None)

        sample_videos = [
            {
                'title': 'Python Full Course for Beginners - Zero to Hero in 15 Minutes',
                'description': 'A comprehensive, beginner-friendly introduction to Python programming syntax, variables, conditionals, and functions with live coding demonstrations.',
                'category': cat_basics,
                'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
                'duration_mins': 15,
                'views_count': 142,
                'order': 1,
            },
            {
                'title': 'Mastering Python Loops & Iterations (For, While, Range & Break)',
                'description': 'Deep dive into Python control flow: for loops, while loops, nested iterations, list processing, and loop control statements (break, continue, pass).',
                'category': cat_loops,
                'video_url': 'https://www.youtube.com/watch?v=6iF8Xb7Z3wQ',
                'duration_mins': 12,
                'views_count': 98,
                'order': 2,
            },
            {
                'title': 'Object-Oriented Programming (OOP) in Python: Classes & Objects',
                'description': 'Understand Object-Oriented Programming in Python from the ground up: creating classes, instantiating objects, using __init__ constructors, and encapsulation.',
                'category': cat_oop,
                'video_url': 'https://www.youtube.com/watch?v=JeznW_7DlB0',
                'duration_mins': 20,
                'views_count': 185,
                'order': 3,
            },
            {
                'title': 'Python Dictionaries, Lists & Data Collections Masterclass',
                'description': 'Learn how to store, manipulate, and query complex data structures in Python with dictionaries, lists, sets, and tuples.',
                'category': cat_basics,
                'video_url': 'https://www.youtube.com/watch?v=daefaLgNkw0',
                'duration_mins': 18,
                'views_count': 76,
                'order': 4,
            }
        ]

        for vdata in sample_videos:
            VideoTutorial.objects.get_or_create(
                title=vdata['title'],
                defaults=vdata
            )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(sample_videos)} Video Tutorials."))

        # 2. Seed Realistic Page Views (Last 14 Days)
        paths = [
            '/',
            '/tutorials/',
            '/videos/',
            '/exercises/',
            '/quizzes/',
            '/practice/',
            '/roadmap/',
            '/python/tutorial/variables-data-types/',
            '/python/tutorial/loops-break-continue/',
            '/python/exercises/reverse-a-string/',
            '/python/quizzes/python-basics-assessment/',
        ]

        users = list(User.objects.all())
        now = timezone.now()

        # Seed realistic distribution if fewer than 50 pageviews exist
        if PageView.objects.count() < 30:
            views_to_create = []
            for day_offset in range(14, -1, -1):
                day_time = now - timedelta(days=day_offset)
                # Generate between 15 and 45 visits per day
                daily_count = random.randint(18, 52)
                for _ in range(daily_count):
                    visit_time = day_time.replace(
                        hour=random.randint(6, 23),
                        minute=random.randint(0, 59),
                        second=random.randint(0, 59)
                    )
                    user = random.choice(users) if (users and random.random() < 0.4) else None
                    path = random.choice(paths)
                    ip = f"192.168.1.{random.randint(2, 60)}"
                    views_to_create.append(
                        PageView(
                            path=path,
                            user=user,
                            ip_address=ip,
                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
                            timestamp=visit_time
                        )
                    )
            PageView.objects.bulk_create(views_to_create)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(views_to_create)} PageView analytics events."))
        else:
            self.stdout.write("PageView events already exist, skipped seeding views.")
