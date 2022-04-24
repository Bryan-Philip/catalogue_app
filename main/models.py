from email.policy import default
from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator

# Create your models here.

class Auctions(models.Model):
    Pid = models.AutoField(primary_key=True)
    number = models.CharField(max_length=55, validators=[RegexValidator(r'^\d{1,10}$')])
    year = models.CharField(max_length=25, validators=[RegexValidator(r'^\d{1,10}$')], null=True)
    date = models.DateField(null=True)
    catalogue_closing_date = models.DateField(null=True)
    allocations = models.JSONField(null=True)
    catalogue = models.JSONField(null=True)
    invoices = models.JSONField(null=True)
    sales = models.JSONField(null=True)
    invoice_data = models.CharField(max_length=255, null=True)
    catalogue_data = models.CharField(max_length=255, null=True)
    catalogue_closing_date = models.DateField(null=True)
    prompt_date = models.DateField(null=True)
    invoice_number = models.IntegerField(null=False, default=1)
    account_sales = models.JSONField(null=True)
    account_sale_data = models.CharField(max_length=255, null=True)
    account_sale_number = models.IntegerField(null=False, default=1)
    warehouse_confirmations = models.JSONField(null=True)

    def __str__(self):
        return self.number
    
class MarksOrder(models.Model):
    name = models.CharField(max_length=55, null=False, default="marks_order")
    order = models.JSONField(null=True)
    
    def __str__(self):
        return self.order
    
# date = models.PositiveIntegerField(validators=[MaxValueValidator(999999999999999999999)])