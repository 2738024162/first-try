# Generated by Django 5.0.6 on 2024-05-21 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(db_comment='登陆密码', max_length=8),
        ),
    ]