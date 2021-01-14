from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, EmailValidator, validate_slug, URLValidator

# Create your models here.
DESIGNATION = [
    ('gram_sevak', 'Gram Sevak'),
    ('gram_vikas_adhikari', 'Gram Vikas Adhikari'),
]
PAYMENT_STATUS = [
    ('matched', 'Matched'),
    ('unmatched', 'Unmatched'),
        # ('pending', 'Pending'),
]
DIRECTOR_APPROVEL = [
    ('yes', 'yes'),
    # ('no', 'no'),
]

class User(AbstractUser):
    is_gp = models.BooleanField(default=False)
    is_observar = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.id)

class Grampanchayat(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="GP", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    taluka = models.ForeignKey('Taluka', on_delete=models.CASCADE)
    panchayat = models.ForeignKey('Panchayat', on_delete=models.CASCADE)
    designation = models.CharField( choices=DESIGNATION, max_length=200, )
    phone_regex = RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be entered in the format: '1234567890'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)
    date = models.DateTimeField(auto_now=True)
    email =  models.EmailField(max_length=254, validators=[EmailValidator], unique=True, default="rayeole@gmail.com")
    username = models.TextField()

    class Meta:
        verbose_name = "Grampanchayat"
        verbose_name_plural = "Grampanchayats"

    def __str__(self):
        return str(self.first_name)
    
class Observar(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="observar", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    date = models.DateTimeField(auto_now=True)
    username = models.TextField(default='ac')
    
    class Meta:
        verbose_name = "Observar"
        verbose_name_plural = "Observars"

    def __str__(self):
        return str(self.first_name)

class Accountant(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="account", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    date = models.DateTimeField(auto_now=True)
    username = models.TextField(default="ac")

    class Meta:
        verbose_name = "Accountant"
        verbose_name_plural = "Accountants"

    def __str__(self):
        return str(self.user)

class Director(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="director", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    date = models.DateTimeField(auto_now=True)
    username = models.TextField(default='ac')

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"

    def __str__(self):
        return str(self.user)

class District(models.Model):
    district = models.CharField(max_length=1000)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.district)

class Taluka(models.Model):
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    taluka = models.CharField(max_length=1000)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.taluka)

class Panchayat(models.Model):
    taluka = models.ForeignKey('Taluka', on_delete=models.CASCADE)
    panchayat = models.CharField(max_length=1000)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.panchayat)

class Agency(models.Model):
    user = models.ForeignKey("User", verbose_name="user_agency", on_delete=models.CASCADE)
    choose_goverment = models.BooleanField(default=False)
    choose_local = models.BooleanField(default=False)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.choose_goverment) + ' ' + str(self.choose_local)

class Payment(models.Model):
    user = models.OneToOneField("Grampanchayat", primary_key=True, verbose_name="gp_payment", on_delete=models.CASCADE) 
    date = models.DateTimeField( auto_now=True)
    paymentID = models.CharField(max_length=10000000000000000)
    UTR_no = models.CharField(max_length=10000000000000000)
    amount = models.CharField( max_length=10000000)
    modeOFPay = models.TextField()

    def __str__(self):
        return str(self.UTR_no)

class Phase(models.Model):
    user = models.OneToOneField("Grampanchayat", primary_key=True, verbose_name="gp_phase", on_delete=models.CASCADE) 
    phaseNO = models.CharField(max_length=50)
    date = models.DateTimeField( auto_now=True)

    class Meta:
        verbose_name = "Phase"
        verbose_name_plural = "Phases"

    def __str__(self):
        return str(self.phaseNO)
        
class AccountantApprovel(models.Model):
    gp_user = models.OneToOneField("Grampanchayat", primary_key=True, verbose_name="Grampanchayat User", on_delete=models.CASCADE)
    account_status = models.CharField(choices=PAYMENT_STATUS, max_length=1000)
    remark = models.CharField(max_length=50, default="paid", blank=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.account_status)
    
class DirectorApprovel(models.Model):
    user = models.OneToOneField("Director", primary_key=True, verbose_name="director_app", on_delete=models.CASCADE)
    
    director_status = models.CharField(choices=DIRECTOR_APPROVEL, max_length=1000)
    gp_user = models.OneToOneField("Grampanchayat", verbose_name="Grampanchayat User", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.director_status)


class Trainning(models.Model):
    user = models.OneToOneField("Grampanchayat", primary_key=True, verbose_name="gp_trainning", on_delete=models.CASCADE) 
    trainning_completed= models.BooleanField(default=False, verbose_name="I have completed the trainning and essentials.")
    date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Trainning"
        verbose_name_plural = "Trainnings"

    def __str__(self):
        return str(self.user_id)

class AuditDocument(models.Model):
    user = models.OneToOneField("Grampanchayat", primary_key=True, verbose_name="gp_audit_doc", on_delete=models.CASCADE) 
    pre_audit = models.FileField(upload_to='images/', max_length=100)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.user)

class Certificate(models.Model):
    user =  models.OneToOneField("Grampanchayat", primary_key=True, verbose_name="gp_cert", on_delete=models.CASCADE) 
    certificate = models.FileField(upload_to='images/', max_length=100)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.user)