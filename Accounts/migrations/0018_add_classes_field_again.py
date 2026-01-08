# No-op placeholder migration to sequence after generated 0018_student_classes
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0018_student_classes'),
    ]

    operations = [
        # intentionally empty: real field add is in 0018_student_classes.py
    ]
