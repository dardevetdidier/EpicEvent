from django.contrib.auth.models import User
from django.db import models


STATUS_CHOICES = [('upcoming', 'upcoming'), ('in progress', 'in progress'), ('completed', 'completed')]


class ManagementTeamMember(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    employee = models.ForeignKey(to=User,
                                 default=None,
                                 on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.last_name} {self.employee.first_name}"


class SalesTeamMember(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    employee = models.ForeignKey(to=User,
                                 default=None,
                                 on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.last_name} {self.employee.first_name}"


class SupportTeamMember(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    employee = models.ForeignKey(to=User,
                                 default=None,
                                 on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.last_name} {self.employee.first_name}"


class Client(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    first_name = models.CharField('First name', max_length=20)
    last_name = models.CharField('Last name', max_length=20)
    email = models.EmailField()
    phone = models.CharField('Phone', max_length=20)
    mobile = models.CharField('Mobile', max_length=20)
    company_name = models.CharField('Company name', max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(to=SalesTeamMember,
                                      default=None,
                                      on_delete=models.CASCADE,
                                      )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        ordering = ["last_name"]


class Contract(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    sales_contact = models.ForeignKey(to=SalesTeamMember,
                                      on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client,
                               on_delete=models.PROTECT,
                               )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due = models.DateTimeField()

    class Meta:
        ordering = ["client"]


class EventStatus(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    status = models.CharField(max_length=15,
                              choices=STATUS_CHOICES,
                              default="upcoming")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Event status"


class Event(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ForeignKey(to=Client,
                               on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=SupportTeamMember,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True
                                        )
    event_status = models.ForeignKey(to=EventStatus,
                                     on_delete=models.CASCADE,
                                     )
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField()
    notes = models.TextField()

    class Meta:
        ordering = ["event_date"]


