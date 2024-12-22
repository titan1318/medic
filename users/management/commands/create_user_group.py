from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = ('Create a user group with specified name and assign permissions\n'
            'Usage: python3 manage.py create_user_group group_name permission1 permission2 ...')

    def add_arguments(self, parser):
        parser.add_argument('group_name', type=str, help='Name of the user group')
        parser.add_argument('permissions', nargs='+', type=str, help='List of permission codenames')

    def handle(self, *args, **options):
        group_name = options['group_name']
        permission_codenames = options['permissions']

        # Проверка наличия группы с таким именем
        if Group.objects.filter(name=group_name).exists():
            self.stdout.write(self.style.ERROR(f'Group with name "{group_name}" already exists.'))
            return

        # Создание новой группы
        group = Group(name=group_name)
        group.save()

        # Назначение разрешений группе
        for codename in permission_codenames:
            try:
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission with codename "{codename}" does not exist.'))

        self.stdout.write(self.style.SUCCESS(f'User group "{group_name}" successfully created'))
