# Generated by Django 3.2.9 on 2021-11-15 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20, verbose_name='First name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20, verbose_name='Phone')),
                ('mobile', models.CharField(max_length=20, verbose_name='Mobile')),
                ('company_name', models.CharField(max_length=250, verbose_name='Company name')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('upcoming', 'upcoming'), ('in progress', 'in progress'), ('completed', 'completed')], default='upcoming', max_length=15)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SupportTeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalesTeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManagementTeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('attendees', models.IntegerField(blank=True, null=True)),
                ('event_date', models.DateTimeField()),
                ('notes', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.client')),
                ('event_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.eventstatus')),
                ('support_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.supportteammember')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_due', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.client')),
                ('sales_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.salesteammember')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.salesteammember'),
        ),
    ]
