from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self) -> None:
        # DO THESE AT STARTUP (runserver)

        from django.contrib.auth.models import Group
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import User

        # create custom permissions

        usercontent_type = ContentType.objects.get_for_model(User)

        if not Permission.objects.filter(codename='is_student').exists():       
            student_permission = Permission.objects.create(
            codename='is_student',
            name='This User Is a Student',
            content_type=usercontent_type,
            )

        # create user groups

        if not Group.objects.filter(name='Student').exists():
            student_permission = Permission.objects.get(codename='is_student')

            student_group = Group.objects.create(name='Student')            
            student_group.permissions.add(student_permission)
            student_group.save()


        return super().ready()