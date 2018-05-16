from django.core.management.base import BaseCommand, CommandError
from cefet.models import *
from members.models import MemberRole

class Command(BaseCommand):
    help = 'Sets up CEFET-MG related data'

    def handle(self, *args, **options):

        if not Campus.objects.filter(location='Belo Horizonte', roman_id='I').exists():
            campus1 = Campus.objects.create(id=1, location='Belo Horizonte', roman_id='I')
        else:
            campus1 = Campus.objects.filter(location='Belo Horizonte', roman_id='I').first()

        if not Campus.objects.filter(location='Belo Horizonte', roman_id='II').exists():
            campus2 = Campus.objects.create(id=2, location='Belo Horizonte', roman_id='II')
        else:
            campus2 = Campus.objects.filter(location='Belo Horizonte', roman_id='II').first()

        if not Campus.objects.filter(location='Leopoldina', roman_id='III').exists():
            campus3 = Campus.objects.create(id=3, location='Leopoldina', roman_id='III')
        else:
            campus3 = Campus.objects.filter(location='Leopoldina', roman_id='III').first()

        if not Campus.objects.filter(location='Araxá', roman_id='IV').exists():
            campus4 = Campus.objects.create(id=4, location='Araxá', roman_id='IV')
        else:
            campus4 = Campus.objects.filter(location='Araxá', roman_id='IV').first()

        if not Campus.objects.filter(location='Divinópolis', roman_id='V').exists():
            campus5 = Campus.objects.create(id=5, location='Divinópolis', roman_id='V')
        else:
            campus5 = Campus.objects.filter(location='Divinópolis', roman_id='V').first()

        if not Campus.objects.filter(location='Timóteo', roman_id='VII').exists():
            campus7 = Campus.objects.create(id=7, location='Timóteo', roman_id='VII')
        else:
            campus7 = Campus.objects.filter(location='Timóteo', roman_id='VII').first()

        if not Campus.objects.filter(location='Varginha', roman_id='VIII').exists():
            campus8 = Campus.objects.create(id=8, location='Varginha', roman_id='VIII')
        else:
            campus8 = Campus.objects.filter(location='Varginha', roman_id='VIII').first()

        if not Campus.objects.filter(location='Nepomuceno', roman_id='IX').exists():
            campus9 = Campus.objects.create(id=9, location='Nepomuceno', roman_id='IX')
        else:
            campus9 = Campus.objects.filter(location='Nepomuceno', roman_id='IX').first()

        if not Campus.objects.filter(location='Curvelo', roman_id='X').exists():
            campus10  = Campus.objects.create(id=10 , location='Curvelo', roman_id='X')
        else:
            campus10  = Campus.objects.filter(location='Curvelo', roman_id='X').first()

        if not Campus.objects.filter(location='Contagem', roman_id='XI').exists():
            campus11 = Campus.objects.create(id=11, location='Contagem', roman_id='XI')
        else:
            campus11 = Campus.objects.filter(location='Contagem', roman_id='XI').first()



        course1 = Course.objects.filter(name='Engenharia de Computação', campus=campus2).first()
        if not course1:
            course1 = Course.objects.create(id=1, name='Engenharia de Computação', campus=campus2)

        course2 = Course.objects.filter(name='Engenharia de Materiais', campus=campus1).first()
        if not course2:
            course2 = Course.objects.create(id=2, name='Engenharia de Materiais', campus=campus1)

        course3 = Course.objects.filter(name='Administração', campus=campus2).first()
        if not course3:
            course3 = Course.objects.create(id=3, name='Administração', campus=campus2)

        course4 = Course.objects.filter(name='Engenharia Ambiental', campus=campus1).first()
        if not course4:
            course4 = Course.objects.create(id=4, name='Engenharia Ambiental', campus=campus1)

        course5 = Course.objects.filter(name='Engenharia Mecatrônica', campus=campus3).first()
        if not course5:
            course5 = Course.objects.create(id=5, name='Engenharia Mecatrônica', campus=campus3)

        pet1 = Pet.objects.create(id=1, course=course1)
        pet2 = Pet.objects.create(id=2, course=course2)
        pet3 = Pet.objects.create(id=3, course=course3)
        pet4 = Pet.objects.create(id=4, course=course4)
        pet5 = Pet.objects.create(id=5, course=course5)


        member1 = MemberRole.objects.create(id=1, name='Tutor', verbose_name='Tutor', verbose_name_plural='Tutores')
        member2 = MemberRole.objects.create(id=2, name='membro', verbose_name='membro', verbose_name_plural='membros')
        member3 = MemberRole.objects.create(id=3, name='co-tutor', verbose_name='co-tutor', verbose_name_plural='co-tutores')

        self.stdout.write(self.style.SUCCESS('Successfully loaded data.'))
