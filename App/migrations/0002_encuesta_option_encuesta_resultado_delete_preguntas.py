# Generated by Django 4.0.4 on 2022-09-08 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuesta',
            name='option',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='encuesta',
            name='resultado',
            field=models.CharField(choices=[('0', 'Si'), ('1', 'No')], default='0', max_length=30),
        ),
        migrations.DeleteModel(
            name='Preguntas',
        ),
    ]
