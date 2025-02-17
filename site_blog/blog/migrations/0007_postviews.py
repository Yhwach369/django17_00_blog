# Generated by Django 5.1.1 on 2024-10-19 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=150)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]
