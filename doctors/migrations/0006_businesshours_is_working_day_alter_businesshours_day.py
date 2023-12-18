# Generated by Django 5.0 on 2023-12-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0005_alter_businesshours_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesshours',
            name='is_working_day',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='businesshours',
            name='day',
            field=models.CharField(choices=[('monday', '월요일'), ('tuesday', '화요일'), ('wednesday', '수요일'), ('thursday', '목요일'), ('friday', '금요일'), ('saturday', '토요일'), ('sunday', '일요일')], db_index=True, max_length=10),
        ),
    ]
