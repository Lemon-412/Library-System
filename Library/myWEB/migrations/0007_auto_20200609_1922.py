# Generated by Django 3.0.3 on 2020-06-09 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myWEB', '0006_auto_20200609_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yytable',
            name='tsid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myWEB.tsTable'),
        ),
    ]
