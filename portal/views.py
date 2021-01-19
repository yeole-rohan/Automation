from django.shortcuts import render, redirect, get_object_or_404

from .forms import GPSignUPForm, GovermentForm, PublicForm, PaymentForm, AuditDocumentForm, CertificateForm, AccountantApprovelForm, DirectorApprovelForm, AccountantSignUpForm, DirectorSignUpForm, ObservarSignUpForm, TrainningForm

from django.views.generic import CreateView
from .models import User, District, Taluka, Panchayat, Agency, Payment, AuditDocument, Certificate, AccountantApprovel, DirectorApprovel, Grampanchayat, Phase, Accountant, Trainning
import razorpay
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from automation import settings
 
'''Renders Logins View For Diffrent Users, Window to House'''
'''Grampachayat = gp, '''
'''Deafult Login View'''
def login_view(request):
    form = AuthenticationForm()
    return render(request = request, template_name = "registration/login.html", context={'form':form})

'''Grampanchayat Register View'''
class GPRegister(CreateView):
    model = User
    form_class = GPSignUPForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('portal:home')

'''Accountant Register View'''
class AccountantRegsiter(CreateView):
    model = User
    form_class= AccountantSignUpForm
    template_name = 'registration/User-Sign-Up.html'
    success_url = reverse_lazy('portal:home')

'''Observar Register View'''
class ObservarRegsiter(CreateView):
    model = User
    form_class= ObservarSignUpForm
    template_name = 'registration/User-Sign-Up.html'
    success_url = reverse_lazy('portal:home')

'''Director Register View'''
class DirectorRegsiter(CreateView):
    model = User
    form_class= DirectorSignUpForm
    template_name = 'registration/User-Sign-Up.html'
    success_url = reverse_lazy('portal:home')

'''Home/Dashboard View, when USer log In'''
@login_required
def home(request):
    agency = Agency.objects.filter(user = request.user)
    gov_choose = GovermentForm()
    pub_form = PublicForm()
    
    trainning, pay, audit_pdf, cert, account_approve,dir_app = '', '', '', '', '',''
    try:
        pay = Payment.objects.get(user=Grampanchayat.objects.get(user = request.user.id))
        dir_app = DirectorApprovel.objects.get(gp_user=Grampanchayat.objects.get(user = request.user.id))
        audit_pdf = AuditDocument.objects.filter(user=request.user.id)
        cert = Certificate.objects.filter(user=request.user.id)
        trainning = Trainning.objects.get(user=Grampanchayat.objects.get(user = request.user.id))
        account_approve = AccountantApprovel.objects.filter(gp_user=Grampanchayat.objects.get(user = request.user.id)).exclude(remark__contains="paid")
    except:
        pass
    if request.method == "POST" and "goverment" in request.POST:
        gov_choose = GovermentForm(request.POST or None)
        if gov_choose.is_valid():
            gov_choose = gov_choose.save(commit=False)
            gov_choose.user = request.user
            gov_choose.choose_local = "False"
            gov_choose.save()
            return redirect('portal:payments')

    if request.method == "POST" and "public" in request.POST:
        pub_form = PublicForm(request.POST or None)
        if pub_form.is_valid():
            pub_form = pub_form.save(commit=False)
            pub_form.user = request.user
            pub_form.choose_goverment = "False"
            pub_form.save()
            return redirect('portal:home')
    return render(request, template_name="home.html", context={ 'gov_form' : gov_choose, 'pub_form' : pub_form, 'agency' : agency, 'pay' : pay, 'trainning' : trainning, 'audit_pdf' : audit_pdf, 'cert' : cert, 'account_approve' : account_approve})

'''Ajax calling views for dropdown from grampanchayat register view'''
def load_taluka(request):
    district_id = request.GET.get('district')
    talukas = Taluka.objects.filter(district=district_id).order_by('taluka')
    return render(request, template_name="talukadropdown.html", context={ 'talukas' : talukas })

def load_panchayat(request): 
    taluka_id = request.GET.get('taluka')
    print(taluka_id)
    panchayat = Panchayat.objects.filter(taluka=taluka_id).order_by('panchayat')
    print(panchayat)
    return render(request, template_name="panchayatdropdown.html", context={ 'panchayats' : panchayat })

'''Grampachayat Payments view and form handling'''
@login_required
def payments(request):
    print(request.POST)
    pays = Payment.objects.filter(user=request.user.id)
    audit_pdf = AuditDocument.objects.filter(user=request.user.id)
    cert = Certificate.objects.filter(user=request.user.id)
    approve = '' 
    # AccountantApprovel.objects.filter(gp_user=request.user.id, account_status__iexact="unmatched")
    pdf = 'yes' if audit_pdf else 'no'
    app = 'yes' if approve else 'no'
    certificate = 'yes' if cert else 'no'
    if pays:
        if approve:
            paid = 'no'
        else:
            paid = 'yes'
    else:
        paid = 'no'

    order_amount = 3894000 
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    client = razorpay.Client(auth = ('rzp_test_RFsHcz1H7YbOw2', 'LNodPNAN6LQqVk8a898PnJH3'))
    payment = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='1'))
    if request.method == "POST" and 'razorpay_order_id' in request.POST:
        print('from razorpay') 
        get_post = request.POST
        order_id = ''
        params_dict = {}
        for key, value in get_post.items():
            if key == "razorpay_order_id":
                params_dict['razorpay_order_id'] = value
                order_id = value
            elif key == "razorpay_payment_id":
                params_dict['razorpay_payment_id'] = value
            elif key == "razorpay_signature":
                params_dict['razorpay_signature'] = value
        status = client.utility.verify_payment_signature(params_dict)
        if status:
            return render(request, 'payment-confirm.html',context= {'status': 'Payment was unsuccesfull!!!'})
        else:
            pay = Payment.objects.create(user=Grampanchayat.objects.get(user = request.user.id), paymentID=order_id, UTR_no=0, amount=38940,modeOFPay = "Internet Banking")
            pay.save()
            # phase = Phase.objects.create(user=Grampanchayat.objects.get(user = request.user.id), phaseNO=1)
            # phase.save()
            create_aprrove_pending = AccountantApprovel.objects.create(gp_user=Grampanchayat.objects.get(user = request.user.id), account_status='unmatched', remark='paid')
            create_aprrove_pending.save()
            return redirect('portal:home')
    try:
        pays = get_object_or_404(Payment, user_id = request.user)
        if pays:
            pay_form = PaymentForm(instance=pays)
    except:
        pay_form = PaymentForm()
    audit_form = AuditDocumentForm()
    cert_form = CertificateForm()
    if request.method == "POST" and 'pay_id' in request.POST:
        try:
            pays = get_object_or_404(Payment, user_id = request.user)
            if pays:
                pay_form = PaymentForm(request.POST or None, instance=pays)
        except:
            pay_form = PaymentForm(request.POST or None)
        if pay_form.is_valid():
            pay_form = pay_form.save(commit=False)
           
            pay_form.user = Grampanchayat.objects.get(user = request.user.id)
            pay_form.amount = 38940
            pay_form.modeOFPay = "RTGS"
            pay_form.paymentID = 0
            pay_form.save()
            # phase = Phase.objects.create(user=Grampanchayat.objects.get(user = request.user.id), phaseNO=1)
            # phase.save()
            create_aprrove_pending = AccountantApprovel.objects.create(gp_user=Grampanchayat.objects.get(user = request.user.id), account_status='unmatched', remark='paid')
            create_aprrove_pending.save()
            return redirect('portal:home')
    

    if request.method == "POST" and 'cert' in request.POST:
        cert_form = CertificateForm(request.POST or None, request.FILES)
        if cert_form.is_valid():
            image = cert_form.cleaned_data['certificate']
            content_type = image.content_type.split('/')[1]
            if content_type in settings.CONTENT_TYPES_IMG:
                if image.size > int(settings.MAX_UPLOAD_SIZE_IMG):
                    messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE_IMG), filesizeformat(image.size)))
                else:
                    cert_form = cert_form.save(commit=False)
                    cert_form.user = request.user
                    cert_form.save()
            else:
                messages.error(request, "File is not supported")
            return redirect('portal:payments')

    if request.method == "POST" and 'audit_id' in request.POST:
        audit_form = AuditDocumentForm(request.POST or None, request.FILES)
        if audit_form.is_valid():
            files = audit_form.cleaned_data['pre_audit']
            content_type = files.content_type.split('/')[1]
            print(files)
            print(files.size)
            print(files.content_type)
            print(files.content_type.split())
            if content_type in settings.CONTENT_TYPES:
                if files.size > int(settings.MAX_UPLOAD_SIZE):
                    messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(files.size)))
                else:
                    audit_form = audit_form.save(commit=False)
                    audit_form.user = request.user
                    audit_form.save()
            else:
                messages.error(request, "File is not supported")
            return redirect('portal:payments')

    return render(request, template_name='payments.html', context={'pay_form' : pay_form, 'paid' : paid, 'audit_form' : audit_form, 'pdf' : pdf, 'certificate' : certificate, 'cert_form' : cert_form, 'app': app, 'payment' : payment })

'''Accountant Payments lists before approvel includes pending, matched, unmatched and User phases'''
@login_required
def accountant_list(request):
    get_all_gp_users_objects = Grampanchayat.objects.filter(payment__UTR_no__isnull=False, payment__paymentID__isnull=False)
    print(get_all_gp_users_objects)
    get_approved_payments = AccountantApprovel.objects.filter(account_status__iexact='unmatched', remark__contains ='paid')
    get_all_id_or_utr_no = Payment.objects.filter(UTR_no__isnull=False, paymentID__isnull=False)
    get_phase_for_paid_user = Phase.objects.all()
    approved_payments_matched = AccountantApprovel.objects.filter(account_status__iexact='matched')
    get_unmatched_and_exlude_paid = AccountantApprovel.objects.exclude(remark__contains ='paid')
    trainning_user = Trainning.objects.filter(trainning_completed=True)
    return render(request, template_name='all-payments.html', context={'all_gp_users' : get_all_gp_users_objects,  'all_utr_or_id' : get_all_id_or_utr_no, 'filtered_approved_payments' : get_approved_payments, 'phase_for_paid_users' : get_phase_for_paid_user, 'approved_payments_matched' : approved_payments_matched, 'get_unmatched_and_exlude_paid' : get_unmatched_and_exlude_paid, 'trainning_users' : trainning_user})

'''Accontant approverl view, here accountant will match or unmathced payment by verifing paymentID or UTR No'''
@login_required
def action(request, user_id):
    get_user_pay_obj = Payment.objects.filter(user = user_id)
    
    get_user_from_account = ''
    try:
        get_user_from_account = AccountantApprovel.objects.get(gp_user = user_id)
    except:
        pass
    approve_form = AccountantApprovelForm()
    if request.method == 'POST':
        approve_form = AccountantApprovelForm(request.POST or None)
        # if approve_form.is_valid():
        #     approve_form = approve_form.save(commit=False)
        #     user = Grampanchayat.objects.get(user=user_id)
        #     approve_form.gp_user = Grampanchayat.objects.get(user=user_id)
        #     approve_form.user = Accountant.objects.get(user=request.user.id)
        #     approve_form.save()
        return redirect('portal:accountant_list')
    return render(request, template_name="action.html", context={'payment' : get_user_pay_obj,'approve_form' : approve_form,})


@login_required 
def director_approve(request):
    get_approved_payments = AccountantApprovel.objects.filter(account_status__iexact='Matched')
    get_phase_for_paid_user = Phase.objects.all()
    get_all_gp_users_objects = Grampanchayat.objects.filter(accountantapprovel__account_status__iexact='Matched')
    get_all_id_or_utr_no = Payment.objects.filter(UTR_no__isnull=False, paymentID__isnull=False)
    return render(request, template_name="director-approve.html", context={'all_gp_users' : get_all_gp_users_objects, 'all_utr_or_id' : get_all_id_or_utr_no, 'filtered_approved_payments' : get_approved_payments,'phase_for_paid_users' : get_phase_for_paid_user })

@login_required
def director_action(request, user_id):
    # accounts = AccountantApprovel.objects.filter(id=id)
    # for user in accounts:
    # pay_user = Payment.objects.get(UTR_no__isnull=False, user_id= user_id, paymentID__isnull=False)
    get_user_pay_obj = Payment.objects.filter(user = user_id)
    director_form = DirectorApprovelForm()
    if request.method == 'POST':
        # director_form = DirectorApprovelForm(request.POST or None)
        # if director_form.is_valid():
        #     director_form = director_form.save(commit=False)
        #     u = Grampanchayat.objects.filter(user = user_id)
        #     for us in u:
        #         user = us
        #         print(us) 
        #     director_form.gp_user = user
        #     director_form.save()
        return redirect('portal:director')
    return render(request, template_name="dir-action.html", context={'payment' : get_user_pay_obj, 'director_form' : director_form}) 

    # static views

def phase_two(request):
    training = TrainningForm()
    print(request.POST)
    pays = Payment.objects.filter(user=request.user.id)
    audit_pdf = AuditDocument.objects.filter(user=request.user.id)
    cert = Certificate.objects.filter(user=request.user.id)
    approve = '' 
    # AccountantApprovel.objects.filter(gp_user=request.user.id, account_status__iexact="unmatched")
    pdf = 'yes' if audit_pdf else 'no'
    app = 'yes' if approve else 'no'
    certificate = 'yes' if cert else 'no'
    if pays:
        if approve:
            paid = 'no'
        else:
            paid = 'yes'
    else:
        paid = 'no'

    order_amount = 3894000 
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    client = razorpay.Client(auth = ('rzp_test_RFsHcz1H7YbOw2', 'LNodPNAN6LQqVk8a898PnJH3'))
    payment = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='1'))
    pay_form = PaymentForm()
    if request.method == "POST" and 'razorpay_order_id' in request.POST:
        print('from razorpay') 
        get_post = request.POST
        order_id = ''
        params_dict = {}
        for key, value in get_post.items():
            if key == "razorpay_order_id":
                params_dict['razorpay_order_id'] = value
                order_id = value
            elif key == "razorpay_payment_id":
                params_dict['razorpay_payment_id'] = value
            elif key == "razorpay_signature":
                params_dict['razorpay_signature'] = value
        status = client.utility.verify_payment_signature(params_dict)
        if status:
            return render(request, 'payment-confirm.html',context= {'status': 'Payment was unsuccesfull!!!'})
        else:
            pay = Payment.objects.create(user=Grampanchayat.objects.get(user = request.user.id), paymentID=order_id, UTR_no=0, amount=38940,modeOFPay = "Internet Banking")
            pay.save()
            # phase = Phase.objects.create(user=Grampanchayat.objects.get(user = request.user.id), phaseNO=1)
            # phase.save()
            create_aprrove_pending = AccountantApprovel.objects.create(gp_user=Grampanchayat.objects.get(user = request.user.id), account_status='unmatched', remark='paid')
            create_aprrove_pending.save()
            return redirect('portal:home')
    if request.method == "POST" and 'trainning' in request.POST: 
        training = TrainningForm(request.POST or None)
        if training.is_valid():
            training = training.save(commit=False)
            training.user =  Grampanchayat.objects.get(user_id=request.user.id)
            training.save()
            return redirect('portal:home')
    return render(request, template_name="phase-2.html", context={'training' : training,'pay_form':pay_form,'payment' : payment, 'paid':paid, 'app':app, 'pdf':pdf})

    
def phase_three(request):
    audit_form = AuditDocumentForm(request.POST or None, request.FILES)
    order_amount = 3894000 
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    client = razorpay.Client(auth = ('rzp_test_RFsHcz1H7YbOw2', 'LNodPNAN6LQqVk8a898PnJH3'))
    payment = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='1'))
    pay_form = PaymentForm()
    if audit_form.is_valid():
        files = audit_form.cleaned_data['pre_audit']
        content_type = files.content_type.split('/')[1]
        print(files)
        print(files.size)
        print(files.content_type)
        print(files.content_type.split())
        if content_type in settings.CONTENT_TYPES:
            if files.size > int(settings.MAX_UPLOAD_SIZE):
                messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(files.size)))
            else:
                audit_form = audit_form.save(commit=False)
                user=Grampanchayat.objects.get(user = request.user.id)
                audit_form.user = user
                audit_form.save()
        else:
            messages.error(request, "File is not supported")
        return redirect('portal:home')
    return render(request, template_name="phase-3.html", context={'audit_form':audit_form,'pay_form':pay_form,'payment' : payment})

def phase_four(request): 
    cert_form = CertificateForm(request.POST or None, request.FILES)
    order_amount = 3894000 
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    client = razorpay.Client(auth = ('rzp_test_RFsHcz1H7YbOw2', 'LNodPNAN6LQqVk8a898PnJH3'))
    payment = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='1'))
    pay_form = PaymentForm()
    if cert_form.is_valid():
        image = cert_form.cleaned_data['certificate']
        content_type = image.content_type.split('/')[1]
        if content_type in settings.CONTENT_TYPES_IMG:
            if image.size > int(settings.MAX_UPLOAD_SIZE_IMG):
                messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE_IMG), filesizeformat(image.size)))
            else:
                cert_form = cert_form.save(commit=False)
                user=Grampanchayat.objects.get(user = request.user.id)
                cert_form.user = user
                cert_form.save()
        else:
            messages.error(request, "File is not supported")
        return redirect('portal:home')
    return render(request, template_name="phase-4.html", context={'cert_form':cert_form,'pay_form':pay_form,'payment' : payment})

def servilance(request):
    return render(request, template_name="servilance-audit.html", context={})

def observar(request):
    return render(request, template_name="observar.html", context={})
