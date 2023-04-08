import yaml
from django.core.management.base import BaseCommand
from reviews.models import Review, Title, CustomUser


class Command(BaseCommand):
    help = 'Create reviews for Title from yaml'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        with open(options['path'], 'r', encoding="utf-8") as stream:
            objects = yaml.safe_load(stream)
            for obj in objects:
                author = CustomUser.objects.get(pk=obj['author'])
                title = Title.objects.get(pk=obj['title_id'])
                review, _ = Review.objects.get_or_create(
                    pk=obj['id'],
                    score=obj['score'],
                    author=author,
                    title=title,
                )
                review.text = obj['text']
                review.pub_date = obj['pub_date']
                review.save()

        self.stdout.write(self.style.SUCCESS('Successfully created reviews'))
