# Generated by Django 4.2 on 2023-05-10 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary_url', models.URLField()),
                ('summary_text', models.FileField(upload_to='')),
            ],
        ),
    ]
