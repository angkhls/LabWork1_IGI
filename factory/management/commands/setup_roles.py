from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from factory.models import City, UserProfile


class Command(BaseCommand):
    help = 'Создаёт демо-пользователей: manager, director и город Минск'

    def handle(self, *args, **options):
        City.objects.get_or_create(name='Минск')
        City.objects.get_or_create(name='Гродно')

        users = [
            ('manager', 'manager123', UserProfile.ROLE_MANAGER),
            ('director', 'director123', UserProfile.ROLE_DIRECTOR),
        ]
        for username, password, role in users:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Создан {username} / {password}'))
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'role': role, 'phone': '+375 (29) 111-11-11'},
            )
            if role == UserProfile.ROLE_DIRECTOR:
                user.is_staff = True
                user.is_superuser = True
                user.save()

        for client in User.objects.filter(client__isnull=False).select_related('client'):
            UserProfile.objects.update_or_create(
                user=client,
                defaults={
                    'role': UserProfile.ROLE_CLIENT,
                    'birth_date': getattr(client.client, 'birth_date', None),
                    'phone': getattr(client.client, 'phone', ''),
                },
            )

        self.stdout.write(self.style.SUCCESS('Готово. Логины: manager/manager123, director/director123'))
