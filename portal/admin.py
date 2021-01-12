from django.contrib import admin
from .models import User, Grampanchayat, District, Taluka, Agency, Phase, Observar, Accountant, Director, Panchayat, Payment, DirectorApprovel, AuditDocument, Trainning, Certificate, AccountantApprovel
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','is_gp', 'is_observar', 'is_accountant', 'is_director')

@admin.register(AccountantApprovel)
class AccountantApprovelAdmin(admin.ModelAdmin):
    list_display=('date','gp_user', 'account_status', 'remark')

@admin.register(Grampanchayat)
class GrampanchayatAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'district', 'taluka', 'panchayat', 'designation', 'phone_number', 'date')
    
@admin.register(Observar)
class ObservarAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'first_name', 'last_name', 'username')

@admin.register(Accountant)
class AccountantAdmin(admin.ModelAdmin):
    list_display = ('user_id',  'date', 'first_name', 'last_name', 'username')
 
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'first_name', 'last_name', 'username')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district', 'date',)

@admin.register(Taluka)
class TalukaAdmin(admin.ModelAdmin):
    list_display = ('district', 'date','taluka')

@admin.register(Panchayat)
class PanchayatAdmin(admin.ModelAdmin):
    list_display = ('panchayat', 'date','taluka')

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'choose_goverment', 'choose_local', 'date')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'UTR_no', 'modeOFPay', 'amount', 'paymentID')

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'phaseNO')

@admin.register(DirectorApprovel)
class DirectorApprovelAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'director_status', 'gp_user')

@admin.register(Trainning)
class TrainningAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'tranning', 'place')

@admin.register(AuditDocument)
class AuditDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'pre_audit', 'date')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_dsiplay = ('user', 'date', 'certificate')
