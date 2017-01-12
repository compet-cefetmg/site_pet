from django.core.management.base import BaseCommand, CommandError
from cefet.models import *
from members.models import MemberRole

class Command(BaseCommand):
    help = 'Sets up CEFET-MG related data'

    def handle(self, *args, **options):
        campus1 = Campus(id=1, location='Belo Horizonte', roman_id='I').save()
        campus2 = Campus(id=2, location='Belo Horizonte', roman_id='II').save()
        campus3 = Campus(id=3, location='Leopoldina', roman_id='III').save()
        campus4 = Campus(id=4, location='Araxá', roman_id='IV').save()
        campus5 = Campus(id=5, location='Divinópolis', roman_id='V').save()
        campus7 = Campus(id=7, location='Timóteo', roman_id='VII').save()
        campus8 = Campus(id=8, location='Varginha', roman_id='VIII').save()
        campus9 = Campus(id=9, location='Nepomuceno', roman_id='IX').save()
        campus10 = Campus(id=10, location='Curvelo', roman_id='X').save()
        campus11 = Campus(id=11, location='Contagem', roman_id='XI').save()

        course1 = Course(name='Engenharia de Computação', campus=campus2).save()
        course2 = Course(name='Engenharia de Materiais', campus=campus1).save()
        course3 = Course(name='Administração', campus=campus2).save()
        course4 = Course(name='Engenharia Ambiental', campus=campus1).save()
        course5 = Course(name='Engenharia Mecatrônica', campus=campus3).save()

        Pet(course=course1).save()
        Pet(course=course2).save()
        Pet(course=course3).save()
        Pet(course=course4).save()
        Pet(course=course5).save()

        MemberRole(name='Tutor', name_plural='Tutores').save()
        MemberRole(name='Bolsista', name_plural='Bolsistas').save()
        MemberRole(name='Colaborador', name_plural='Colaboradores').save()
        MemberRole(name='Ex-membro', name_plural='Ex-membros').save()
        MemberRole(name='Voluntário', name_plural='Voluntários').save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded data.'))
