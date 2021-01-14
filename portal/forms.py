from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Grampanchayat, District, Taluka, Panchayat, Agency, Payment, AuditDocument, Certificate, AccountantApprovel, DirectorApprovel, Accountant, Director, Observar, Trainning
from django.db import transaction
from django.core.validators import RegexValidator, EmailValidator

DESIGNATION = [
    ('gram_sevak', 'Gram Sevak'),
    ('gram_vikas_adhikari', 'Gram Vikas Adhikari'),
]
class GPSignUPForm(UserCreationForm):
    first_name = forms.CharField( max_length=100, required=True)
    last_name = forms.CharField( max_length=100, required=True)
    district = forms.ModelChoiceField(queryset=District.objects.all())
    taluka = forms.ModelChoiceField(queryset=Taluka.objects.all())
    panchayat = forms.ModelChoiceField(queryset=Panchayat.objects.all())
    designation = forms.ChoiceField( choices=DESIGNATION, required=False)
    phone_regex = RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be entered in the format: '1234567890'. Up to 10 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=10)
    email = forms.EmailField(max_length=254, validators=[EmailValidator])

    class Meta(UserCreationForm.Meta):
        model = User
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['taluka'].queryset = Taluka.objects.none()
        self.fields['panchayat'].queryset = Panchayat.objects.none()
        
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                print(district_id)
                self.fields['taluka'].queryset = Taluka.objects.filter(district=district_id)
            except(ValueError, TypeError):
                pass
        elif self.instance.id:
            self.fields['taluka'].queryset = self.instance.district.taluka_set
        
        if 'taluka' in self.data:
            try:
                taluka_id = int(self.data.get('taluka'))
                print(taluka_id)
                self.fields['panchayat'].queryset = Panchayat.objects.filter(taluka=taluka_id)
            except(ValueError, TypeError):
                pass
        elif self.instance.id:
            self.fields['panchayat'].queryset = self.instance.taluka.panchayat_set

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_gp = True
        user.save()
        username = self.cleaned_data.get('username')
        first = self.cleaned_data.get('first_name')
        last = self.cleaned_data.get('last_name')
        district_id = self.cleaned_data.get('district')
        taluka_id = self.cleaned_data.get('taluka')
        panchayat_id = self.cleaned_data.get('panchayat')
        number = self.cleaned_data.get('phone_number')
        email = self.cleaned_data.get("email")
        designation = self.cleaned_data.get('designation')
        gp = Grampanchayat.objects.create(user=user, first_name= first, last_name= last, district = district_id, taluka=taluka_id, panchayat = panchayat_id, email=email, designation=designation, phone_number=number, username=username)
        gp.save()
        return user

class AccountantSignUpForm(UserCreationForm):
    first_name = forms.CharField( max_length=100, required=True)
    last_name = forms.CharField( max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_accountant = True
        user.save()
        username = self.cleaned_data.get('username')
        first = self.cleaned_data.get('first_name')
        last = self.cleaned_data.get('last_name')
        accountant = Accountant.objects.create(user = user,first_name = first, last_name= last, username= username )
        accountant.save()
        return user

class DirectorSignUpForm(UserCreationForm):
    first_name = forms.CharField( max_length=100, required=True)
    last_name = forms.CharField( max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_director = True
        user.save()
        username = self.cleaned_data.get('username')
        first = self.cleaned_data.get('first_name')
        last = self.cleaned_data.get('last_name')
        accountant = Director.objects.create(user = user,first_name = first, last_name= last, username= username )
        accountant.save()
        return user

class ObservarSignUpForm(UserCreationForm):
    first_name = forms.CharField( max_length=100, required=True)
    last_name = forms.CharField( max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_observar = True
        user.save()
        username = self.cleaned_data.get('username')
        first = self.cleaned_data.get('first_name')
        last = self.cleaned_data.get('last_name')
        accountant = Observar.objects.create(user = user,first_name = first, last_name= last, username= username )
        accountant.save()
        return user

class GovermentForm(forms.ModelForm):
    
    class Meta:
        model = Agency
        fields = ("choose_goverment",)

class PublicForm(forms.ModelForm):
    
    class Meta:
        model = Agency
        fields = ("choose_local",)

class PaymentForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        fields = ("UTR_no",)

class AuditDocumentForm(forms.ModelForm):
    
    class Meta:
        model = AuditDocument
        fields = ("pre_audit",)

class CertificateForm(forms.ModelForm):
    
    class Meta:
        model = Certificate
        fields = ("certificate",)

class AccountantApprovelForm(forms.ModelForm):
    
    class Meta:
        model = AccountantApprovel
        fields = ("account_status", 'remark')

class DirectorApprovelForm(forms.ModelForm):
    
    class Meta:
        model = DirectorApprovel
        fields = ("director_status",)
    
class TrainningForm(forms.ModelForm):
    class Meta:
        model = Trainning
        fields = ("trainning_completed",)
