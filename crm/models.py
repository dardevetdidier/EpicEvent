from django.contrib.auth.models import User
from django.db import models



CLIENT_STATUS = [("prospect", "prospect"), ("client", "client")]


class ManagementTeamMember(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    employee = models.ForeignKey(to=User,
                                 default=None,
                                 on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.last_name} {self.employee.first_name}"

    class Meta:
        verbose_name = "Management Team Member"


class SalesTeamMember(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    employee = models.ForeignKey(to=User,
                                 default=None,
                                 on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.last_name} {self.employee.first_name}"

    class Meta:
        verbose_name = "Sales Team Member"


class SupportTeamMember(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    employee = models.ForeignKey(to=User,
                                 default=None,
                                 on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.last_name} {self.employee.first_name}"

    class Meta:
        verbose_name = "Support Team Member"


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
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True
                                      )
    status = models.CharField(max_length=10,
                              choices=CLIENT_STATUS,
                              default="prospect")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        ordering = ["last_name"]


class Contract(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    sales_contact = models.ForeignKey(to=SalesTeamMember,
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)
    client = models.ForeignKey(to=Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="contracts"
                               )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    signed_status = models.BooleanField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due = models.DateTimeField()

    class Meta:
        ordering = ["client"]


class EventStatus(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    status = models.CharField(max_length=150)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Event Status"
        verbose_name_plural = "Event Status"


class Event(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ForeignKey(to=Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=SupportTeamMember,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True
                                        )
    event_status = models.ForeignKey(to=EventStatus,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True,
                                     related_name="events"
                                     )
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Event n° {self.id}"

    class Meta:
        ordering = ["event_date"]


