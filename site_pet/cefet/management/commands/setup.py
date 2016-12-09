from django.core.management.base import BaseCommand, CommandError
from cefet.models import *

class Command(BaseCommand):
    help = 'Sets up CEFET-MG related data'

    def handle(self, *args, **options):
        campus1 = Campus(id=1, location='Belo Horizonte', roman_id='I')
        campus2 = Campus(id=2, location='Belo Horizonte', roman_id='II')
        campus3 = Campus(id=3, location='Araxá', roman_id='III')
        campus1.save()
        campus2.save()
        campus3.save()

        course1 = Course(name='Engenharia de Computação', campus=campus2)
        course2 = Course(name='Engenharia de Materiais', campus=campus1)
        course3 = Course(name='Administração', campus=campus2)
        course4 = Course(name='Engenharia Ambiental', campus=campus1)
        course5 = Course(name='Engenharia Mecatrônica', campus=campus3)
        course1.save()
        course2.save()
        course3.save()
        course4.save()
        course5.save()

        pet1 = Pet(course=course1)
        pet2 = Pet(course=course2)
        pet3 = Pet(course=course3)
        pet4 = Pet(course=course4)
        pet5 = Pet(course=course5)
        pet1.save()
        pet2.save()
        pet3.save()
        pet4.save()
        pet5.save()
        # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))