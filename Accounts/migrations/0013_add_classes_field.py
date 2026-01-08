# Generated manually: Add classes ManyToManyField to Student
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0012_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='classes',
            field=models.ManyToManyField(blank=True, related_name='students_m2m', to='Accounts.Classe'),
        ),
    ]
