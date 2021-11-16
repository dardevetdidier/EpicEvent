# Generated by Django 3.2.9 on 2021-11-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventstatus',
            options={'verbose_name_plural': 'Event status'},
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_due',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.BooleanField(null=True),
        ),
    ]
