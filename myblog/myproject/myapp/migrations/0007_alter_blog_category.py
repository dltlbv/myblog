# Generated by Django 5.0.6 on 2024-08-22 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_blog_shared_by_blog_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('food', 'Еда'), ('life', 'Жизнь'), ('sport', 'Спорт'), ('travel', 'Путешествия'), ('hobby', 'Хобби'), ('stars', 'Звезды')], default='life', max_length=10),
        ),
    ]
