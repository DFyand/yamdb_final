import yaml
from django.core.management.base import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = 'Create categories from yaml'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        with open(options['path'], 'r', encoding="utf-8") as stream:
            objects = yaml.safe_load(stream)
            for obj in objects:
                category, _ = Category.objects.get_or_create(pk=obj['id'])
                category.name = obj['name']
                category.slug = obj['slug']
                category.save()

        self.stdout.write(self.style.SUCCESS('Categories created successful'))
