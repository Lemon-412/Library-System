# Generated by Django 3.0.3 on 2020-06-09 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myWEB', '0005_yytable_tsid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yytable',
            name='tsid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='myWEB.tsTable'),
        ),
    ]
