# Generated by Django 4.0.1 on 2022-02-01 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sells', '0002_alter_item_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sells',
            name='company_name',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='sells.companyname'),
        ),
    ]
