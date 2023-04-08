import yaml
from django.core.management.base import BaseCommand
from reviews.models import Genre, Title


class Command(BaseCommand):
    help = 'Insert genres to Titles from yaml'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        with open(options['path'], 'r', encoding="utf-8") as stream:
            objects = yaml.safe_load(stream)
            for obj in objects:
                title, _ = Title.objects.get_or_create(pk=obj['title_id'])
                genre = Genre.objects.get(pk=obj['genre_id'])
                title.genre.add(genre)
                title.save()

        self.stdout.write(self.style.SUCCESS('Genres Successfully added'))
