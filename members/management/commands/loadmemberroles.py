from django.core.management.base import BaseCommand, CommandError
from members.models import MemberRole

class Command(BaseCommand):
    help = 'Sets up member roles'

    def handle(self, *args, **options):
        MemberRole(name='Tutor', name_plural='Tutores').save()
        MemberRole(name='Bolsista', name_plural='Bolsistas').save()
        MemberRole(name='Colaborador', name_plural='Colaboradores').save()
        MemberRole(name='Ex-membro', name_plural='Ex-membros').save()
        MemberRole(name='Voluntário', name_plural='Voluntários').save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded data.'))
