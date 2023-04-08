import yaml
from django.core.management.base import BaseCommand
from reviews.models import CustomUser


class Command(BaseCommand):
    help = 'Create users from yaml'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        with open(options['path'], 'r', encoding="utf-8") as stream:
            users = yaml.safe_load(stream)
            for user in users:
                customuser, _ = CustomUser.objects.get_or_create(pk=user['id'])
                customuser.username = user['username']
                customuser.email = user['email']
                customuser.role = user['role']
                # customuser.bio = user['bio']
                # customuser.first_name = user['first_name']
                # customuser.last_name = user['last_name']
                customuser.save()

        self.stdout.write(self.style.SUCCESS('Successfully created users'))
