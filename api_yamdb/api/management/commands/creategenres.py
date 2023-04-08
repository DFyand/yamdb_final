import yaml
from django.core.management.base import BaseCommand
from reviews.models import Genre


class Command(BaseCommand):
    help = 'Create genres from yaml'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        with open(options['path'], 'r', encoding="utf-8") as stream:
            objects = yaml.safe_load(stream)
            for obj in objects:
                genre, _ = Genre.objects.get_or_create(pk=obj['id'])
                genre.name = obj['name']
                genre.slug = obj['slug']
                genre.save()

        self.stdout.write(self.style.SUCCESS('Successfully created genres'))
