# Generated by Django 4.1.5 on 2023-03-21 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('image_field', models.ImageField(upload_to='media/')),
                ('description', models.TextField()),
            ],
        ),
    ]
