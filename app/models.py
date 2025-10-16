import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email


JOB_CHOICES = [
    ('new_job', 'New Job'),
    ('old_job', 'Old Job'),
]
# Create your models here.
class Registration(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    first_name = models.CharField(max_length=200, blank=True,null=True,)
    last_name = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True,validators=[validate_email])
    
    
    
class JobDetail(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    job_date = models.DateField()
    bill_no = models.CharField(max_length=200,blank=True, null=True)
    job_name = models.CharField(max_length=400,blank=True, null=True)
    company_name = models.CharField(max_length=500,blank=True, null=True)
    job_type = models.CharField(choices=JOB_CHOICES,max_length=10,blank=True, null=True)
    noc =  models.TextField(blank=True, null=True)
    prpc_purchase = models.CharField(max_length=200,blank=True, null=True)
    prpc_sell = models.CharField(max_length=200,blank=True, null=True)
    cylinder_size = models.CharField(max_length=200,blank=True, null=True)
    cylinder_made_in = models.CharField(max_length=200,blank=True, null=True)
    pouch_size = models.CharField(max_length=200,blank=True, null=True)
    pouch_open_size = models.CharField(max_length=200,blank=True, null=True)
    pouch_combination = models.CharField(max_length=200,blank=True, null=True)
    correction = models.TextField(blank=True, null=True)
    
    cylinder_date = models.DateField(blank=True, null=True)
    cylinder_bill_no = models.CharField(blank=True, null=True)
    job_status = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    
    def __str__(self):
        return self.company_name
    
    
    
    