# Generated by Django 3.2.9 on 2021-11-25 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20211122_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='status',
            new_name='signed_status',
        ),
        migrations.AlterField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contracts', to='crm.client'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.salesteammember'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='crm.eventstatus'),
        ),
    ]
