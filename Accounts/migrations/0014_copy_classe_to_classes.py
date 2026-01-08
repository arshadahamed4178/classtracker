from django.db import migrations


def copy_classe_to_classes(apps, schema_editor):
    Student = apps.get_model('Accounts', 'Student')
    for student in Student.objects.all():
        # if a student had a classe FK, add it to the new M2M 'classes'
        if student.classe_id:
            student.classes.add(student.classe_id)


def reverse_copy(apps, schema_editor):
    Student = apps.get_model('Accounts', 'Student')
    for student in Student.objects.all():
        # remove all M2M links (best-effort)
        student.classes.clear()


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0013_add_classes_field'),
    ]

    operations = [
        migrations.RunPython(copy_classe_to_classes, reverse_copy),
    ]
