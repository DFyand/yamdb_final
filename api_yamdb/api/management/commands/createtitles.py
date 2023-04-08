import yaml
from django.core.management.base import BaseCommand
from reviews.models import Title, Category


class Command(BaseCommand):
    help = 'Create genres from yaml'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        with open(options['path'], 'r', encoding="utf-8") as stream:
            objects = yaml.safe_load(stream)
            for obj in objects:
                title, _ = Title.objects.get_or_create(
                    pk=obj['id'],
                    year=obj['year']
                )
                title.name = obj['name']
                title.category = Category.objects.get(id=obj['category'])
                title.save()

        self.stdout.write(self.style.SUCCESS('Successfully created titles'))
