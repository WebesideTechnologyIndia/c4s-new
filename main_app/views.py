from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import (
    HomeSectionCard, 
    CollegeCounsellingCard, 
    CareerCounsellingService,
    AdmissionIndiaCard
)
from .forms import (
    HomeSectionCardForm, 
    CollegeCounsellingCardForm,
    CareerCounsellingServiceForm,
    AdmissionIndiaCardForm
)
from django.views.decorators.cache import never_cache


# ==================== HELPER FUNCTION ====================


def is_admin_or_staff(user):
    """Check if user is staff or superuser"""
    return user.is_staff or user.is_superuser


# ==================== PUBLIC VIEWS ====================


def home_view(request):
    """Home page view with dynamic cards"""
    cards = HomeSectionCard.objects.filter(is_active=True)
    context = {'cards': cards}
    return render(request, 'home.html', context)


def college_counselling_view(request):
    """College Admission Counselling Services Page"""
    cards = CollegeCounsellingCard.objects.filter(is_active=True)
    context = {'cards': cards}
    return render(request, 'college_counselling.html', context)


def career_counselling_view(request):
    """Career Counselling Services Page"""
    services = CareerCounsellingService.objects.filter(is_active=True)
    return render(request, 'career_counselling.html', {'services': services})


# ==================== USER AUTHENTICATION ====================


# ==================== USER AUTHENTICATION (SMART LOGIN) ====================


def user_login_view(request):
    """Smart Login - Works for BOTH Admin and Normal Users"""
    if request.user.is_authenticated:
        # Already logged in
        if request.user.is_staff or request.user.is_superuser:
            return redirect('main_app:admin_dashboard')
        
        # ✅ Check if there's a 'next' parameter
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        
        return redirect('main_app:admission_india_services')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # ✅ AUTO-DETECT: Admin ya Normal User?
            if user.is_staff or user.is_superuser:
                messages.success(request, f'Welcome back, Admin {user.username}!')
                return redirect('main_app:admin_dashboard')
            else:
                messages.success(request, f'Welcome back, {user.username}!')
                
                # ✅ DYNAMIC REDIRECT: Check 'next' parameter from login page
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                # Default redirect if no 'next' parameter
                return redirect('main_app:admission_india_services')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'admin/login.html')


@never_cache  # ✅ YE ADD KARO
def user_logout_view(request):
    """Universal Logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    response = redirect('main_app:user_login')
    
    # ✅ Cache headers add karo
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


# ✅ ALIAS: admin_login aur admin_logout same hain user_login ke
admin_login_view = user_login_view
admin_logout_view = user_logout_view


# ==================== ADMISSION INDIA (LOGIN REQUIRED) ====================
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.cache import never_cache
from .models import AdmissionIndiaCard, StudentCardPurchase, UserRegistration

@never_cache
@login_required(login_url='main_app:user_login')
def admission_india_services_view(request):
    """Admission India Services Page - LOGIN REQUIRED (Normal Users)"""
    
    # Agar admin hai to admin dashboard bhej do
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins can access from admin panel.')
        return redirect('main_app:admin_dashboard')
    
    # Student ka registration data nikalo
    try:
        student = UserRegistration.objects.get(user=request.user)
    except UserRegistration.DoesNotExist:
        student = None
    
    # ✅ SAHI LOGIC: Sab active cards nikalo (FREE + PAID dono)
    all_cards = AdmissionIndiaCard.objects.filter(is_active=True).order_by('order', 'id')
    
    # Student ke purchased cards nikalo
    purchased_card_ids = set()
    if student:
        purchased_card_ids = set(
            StudentCardPurchase.objects.filter(
                student=student,
                payment_status='completed'
            ).values_list('card_id', flat=True)
        )
    
    # ✅ Cards ko prepare karo (sab dikhaega - free, paid, purchased)
    cards_to_display = []
    
    for card in all_cards:
        is_purchased = card.id in purchased_card_ids
        
        card_data = {
            'id': card.id,
            'title': card.title,
            'feature_1': card.feature_1,
            'feature_2': card.feature_2,
            'feature_3': card.feature_3,
            'feature_4': card.feature_4,
            'redirect_link': card.redirect_link,
            'border_gradient_start': card.border_gradient_start,
            'border_gradient_end': card.border_gradient_end,
            'card_type': card.card_type,  # 'free' or 'paid'
            'price': card.price,
            'is_purchased': is_purchased,
        }
        
        # ✅ ADD SABB CARDS - frontend decide karega kya show karna hai
        cards_to_display.append(card_data)
    
    context = {
        'cards': cards_to_display,
        'student': student,
    }
    
    return render(request, 'admission_india_services.html', context)




@never_cache
@login_required(login_url='main_app:user_login')
def purchase_card_view(request, card_id):
    """Payment page for card purchase"""
    
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    try:
        student = UserRegistration.objects.get(user=request.user)
        card = AdmissionIndiaCard.objects.get(id=card_id, is_active=True)
    except (UserRegistration.DoesNotExist, AdmissionIndiaCard.DoesNotExist):
        messages.error(request, 'Invalid request.')
        return redirect('main_app:admission_india_services')
    
    # Check agar already purchased hai
    if StudentCardPurchase.objects.filter(
        student=student,
        card=card,
        payment_status='completed'
    ).exists():
        messages.info(request, 'You have already purchased this card.')
        return redirect(card.redirect_link or 'main_app:admission_india_services')
    
    if request.method == 'POST':
        # ✅ Payment process - Status 'pending' rakhenge (admin approve karega baad mein)
        
        purchase = StudentCardPurchase.objects.create(
            student=student,
            card=card,
            amount=card.price,
            payment_status='pending',  # ✅ PENDING - completed nahi
            transaction_id=f"TXN_{student.id}_{card.id}_{int(timezone.now().timestamp())}",
            payment_method='Online'
        )
        # Don't set payment_completed_at - it will be set when admin approves
        purchase.save()
        
        messages.info(request, f'Card "{card.title}" purchase request submitted! Waiting for approval.')
        return redirect('main_app:admission_india_services')
    
    context = {
        'student': student,
        'card': card,
    }
    return render(request, 'purchase_card.html', context)


# ==================== ADMIN LOGIN/LOGOUT ====================


# ==================== ADMIN DASHBOARD ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_dashboard_view(request):
    """Admin dashboard home - Staff/Superuser Only"""
    total_home_cards = HomeSectionCard.objects.count()
    active_home_cards = HomeSectionCard.objects.filter(is_active=True).count()
    
    total_counselling_cards = CollegeCounsellingCard.objects.count()
    active_counselling_cards = CollegeCounsellingCard.objects.filter(is_active=True).count()
    
    total_career_services = CareerCounsellingService.objects.count()
    active_career_services = CareerCounsellingService.objects.filter(is_active=True).count()
    
    total_admission_cards = AdmissionIndiaCard.objects.count()
    active_admission_cards = AdmissionIndiaCard.objects.filter(is_active=True).count()
    
    context = {
        'total_home_cards': total_home_cards,
        'active_home_cards': active_home_cards,
        'total_counselling_cards': total_counselling_cards,
        'active_counselling_cards': active_counselling_cards,
        'total_career_services': total_career_services,
        'active_career_services': active_career_services,
        'total_admission_cards': total_admission_cards,
        'active_admission_cards': active_admission_cards,
    }
    return render(request, 'admin/dashboard.html', context)


# ==================== HOME SECTION CARD MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_cards_list(request):
    """List all HOME SECTION cards"""
    cards = HomeSectionCard.objects.all()
    context = {'cards': cards}
    return render(request, 'admin/cards_list.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_card_add(request):
    """Add new HOME SECTION card"""
    if request.method == 'POST':
        form = HomeSectionCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_cards_list')
    else:
        form = HomeSectionCardForm()
    
    context = {'form': form}
    return render(request, 'admin/card_form.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_card_edit(request, card_id):
    """Edit existing HOME SECTION card"""
    card = get_object_or_404(HomeSectionCard, id=card_id)
    
    if request.method == 'POST':
        form = HomeSectionCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated successfully!')
            return redirect('main_app:admin_cards_list')
    else:
        form = HomeSectionCardForm(instance=card)
    
    context = {'form': form, 'card': card}
    return render(request, 'admin/card_form.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_card_delete(request, card_id):
    """Delete HOME SECTION card"""
    card = get_object_or_404(HomeSectionCard, id=card_id)
    
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted successfully!')
        return redirect('main_app:admin_cards_list')
    
    context = {'card': card}
    return render(request, 'admin/card_delete.html', context)


# ==================== COLLEGE COUNSELLING CARD MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_counselling_cards_list(request):
    """List all COLLEGE COUNSELLING cards"""
    cards = CollegeCounsellingCard.objects.all()
    context = {'cards': cards, 'card_type': 'counselling'}
    return render(request, 'admin/counselling_cards_list.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_counselling_card_add(request):
    """Add new COLLEGE COUNSELLING card"""
    if request.method == 'POST':
        form = CollegeCounsellingCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Counselling card added successfully!')
            return redirect('main_app:admin_counselling_cards_list')
    else:
        form = CollegeCounsellingCardForm()
    
    context = {'form': form, 'card_type': 'counselling'}
    return render(request, 'admin/counselling_card_form.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_counselling_card_edit(request, card_id):
    """Edit COLLEGE COUNSELLING card"""
    card = get_object_or_404(CollegeCounsellingCard, id=card_id)
    
    if request.method == 'POST':
        form = CollegeCounsellingCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Counselling card updated successfully!')
            return redirect('main_app:admin_counselling_cards_list')
    else:
        form = CollegeCounsellingCardForm(instance=card)
    
    context = {'form': form, 'card': card, 'card_type': 'counselling'}
    return render(request, 'admin/counselling_card_form.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_counselling_card_delete(request, card_id):
    """Delete COLLEGE COUNSELLING card"""
    card = get_object_or_404(CollegeCounsellingCard, id=card_id)
    
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Counselling card deleted successfully!')
        return redirect('main_app:admin_counselling_cards_list')
    
    context = {'card': card, 'card_type': 'counselling'}
    return render(request, 'admin/counselling_card_delete.html', context)


# ==================== CAREER COUNSELLING SERVICE MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_career_services_list(request):
    """List all Career Services"""
    services = CareerCounsellingService.objects.all()
    return render(request, 'admin/career_services_list.html', {'services': services})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_career_service_add(request):
    """Add Career Service"""
    if request.method == 'POST':
        form = CareerCounsellingServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            messages.success(request, 'Service added successfully!')
            return redirect('main_app:admin_career_services_list')
        else:
            messages.error(request, "Form validation failed!")
    else:
        form = CareerCounsellingServiceForm()
    return render(request, 'admin/career_service_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_career_service_edit(request, service_id):
    """Edit Career Service"""
    service = get_object_or_404(CareerCounsellingService, id=service_id)
    if request.method == 'POST':
        form = CareerCounsellingServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated!')
            return redirect('main_app:admin_career_services_list')
    else:
        form = CareerCounsellingServiceForm(instance=service)
    return render(request, 'admin/career_service_form.html', {'form': form, 'service': service})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_career_service_delete(request, service_id):
    """Delete Career Service"""
    service = get_object_or_404(CareerCounsellingService, id=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted!')
        return redirect('main_app:admin_career_services_list')
    return render(request, 'admin/career_service_delete.html', {'service': service})


# ==================== ADMISSION INDIA CARD MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_cards_list(request):
    """List all Admission India cards"""
    cards = AdmissionIndiaCard.objects.all()
    return render(request, 'admin/admission_cards_list.html', {'cards': cards})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_card_add(request):
    """Add new Admission India card"""
    if request.method == 'POST':
        form = AdmissionIndiaCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_admission_cards_list')
    else:
        form = AdmissionIndiaCardForm()
    
    return render(request, 'admin/admission_card_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_card_edit(request, card_id):
    """Edit Admission India card"""
    card = get_object_or_404(AdmissionIndiaCard, id=card_id)
    
    if request.method == 'POST':
        form = AdmissionIndiaCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated successfully!')
            return redirect('main_app:admin_admission_cards_list')
    else:
        form = AdmissionIndiaCardForm(instance=card)
    
    return render(request, 'admin/admission_card_form.html', {'form': form, 'card': card})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_card_delete(request, card_id):
    """Delete Admission India card"""
    card = get_object_or_404(AdmissionIndiaCard, id=card_id)
    
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted successfully!')
        return redirect('main_app:admin_admission_cards_list')
    
    return render(request, 'admin/admission_card_delete.html', {'card': card})









from .models import AllIndiaServiceCard
from .forms import AllIndiaServiceCardForm

# ==================== PUBLIC VIEW ====================
@never_cache
@login_required(login_url='main_app:user_login')
def all_india_services_view(request):
    """All India State Wise Counselling Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins can access from admin panel.')
        return redirect('main_app:admin_dashboard')
    
    # Cards alphabetically sorted by title (A to Z)
    cards = AllIndiaServiceCard.objects.filter(is_active=True).order_by('title')
    
    context = {'cards': cards}
    return render(request, 'all_india_services.html', context)


# ==================== ADMIN VIEWS ====================


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_all_india_cards_list(request):
    """List all All India Service cards"""
    cards = AllIndiaServiceCard.objects.all()
    return render(request, 'admin/all_india_cards_list.html', {'cards': cards})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_all_india_card_add(request):
    """Add new All India Service card"""
    if request.method == 'POST':
        form = AllIndiaServiceCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_all_india_cards_list')
    else:
        form = AllIndiaServiceCardForm()
    
    return render(request, 'admin/all_india_card_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_all_india_card_edit(request, card_id):
    """Edit All India Service card"""
    card = get_object_or_404(AllIndiaServiceCard, id=card_id)
    
    if request.method == 'POST':
        form = AllIndiaServiceCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated successfully!')
            return redirect('main_app:admin_all_india_cards_list')
    else:
        form = AllIndiaServiceCardForm(instance=card)
    
    return render(request, 'admin/all_india_card_form.html', {'form': form, 'card': card})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_all_india_card_delete(request, card_id):
    """Delete All India Service card"""
    card = get_object_or_404(AllIndiaServiceCard, id=card_id)
    
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted successfully!')
        return redirect('main_app:admin_all_india_cards_list')
    
    return render(request, 'admin/all_india_card_delete.html', {'card': card})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import (
    ProfessionalCounsellingCard,
    StudentDocument,
    ChoiceFilling,
    CounsellingStatus,
    DoubtSession,
    Complaint
)
from .forms import (
    StudentDocumentForm,
    ChoiceFillingForm,
    DoubtSessionForm,
    ComplaintForm
)


# ==================== STUDENT DASHBOARD VIEW ====================
@never_cache
@login_required(login_url='main_app:user_login')
def student_dashboard_view(request):
    """Student Dashboard - Professional Counselling by Experts"""
    
    # Check if admin
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins should use admin panel.')
        return redirect('main_app:admin_dashboard')
    
    # Get or create counselling status for student
    status, created = CounsellingStatus.objects.get_or_create(student=request.user)
    
    # Get all cards
    cards = ProfessionalCounsellingCard.objects.filter(is_active=True)
    
    # Get student data
    documents = StudentDocument.objects.filter(student=request.user)
    uploaded_doc_types = list(documents.values_list('document_type', flat=True))
    
    choices = ChoiceFilling.objects.filter(student=request.user)
    doubts = DoubtSession.objects.filter(student=request.user)
    complaints = Complaint.objects.filter(student=request.user)
    
    # Handle POST requests for different sections
    if request.method == 'POST':
        
        # ===== DOCUMENT UPLOAD =====
        if 'upload_document' in request.POST:
            document_type = request.POST.get('document_type')
            document_file = request.FILES.get('document_file')
            
            # Check if document already exists
            if StudentDocument.objects.filter(student=request.user, document_type=document_type).exists():
                messages.error(request, f'{document_type} already uploaded. Please delete the old one first.')
            else:
                StudentDocument.objects.create(
                    student=request.user,
                    document_type=document_type,
                    document_file=document_file
                )
                messages.success(request, f'{document_type} uploaded successfully!')
                
                # Update status
                status.application_submitted = True
                status.current_stage = 'documents_upload'
                status.save()
            
            return redirect('main_app:student_dashboard')
        
        # ===== DELETE DOCUMENT =====
        elif 'delete_document' in request.POST:
            doc_id = request.POST.get('delete_document_id')
            try:
                doc = StudentDocument.objects.get(id=doc_id, student=request.user)
                doc.delete()
                messages.success(request, 'Document deleted successfully!')
            except StudentDocument.DoesNotExist:
                messages.error(request, 'Document not found!')
            
            return redirect('main_app:student_dashboard')
        
        # ===== CHOICE FILLING =====
        elif 'add_choice' in request.POST:
            form = ChoiceFillingForm(request.POST)
            if form.is_valid():
                choice = form.save(commit=False)
                choice.student = request.user
                
                # Check if preference number already exists
                if ChoiceFilling.objects.filter(student=request.user, preference_number=choice.preference_number).exists():
                    messages.error(request, f'Preference #{choice.preference_number} already exists!')
                else:
                    choice.save()
                    messages.success(request, f'Choice #{choice.preference_number} added successfully!')
                    
                    # Update status
                    status.choice_filling_completed = True
                    status.current_stage = 'choice_filling'
                    status.save()
            else:
                messages.error(request, 'Please fill all fields correctly!')
            
            return redirect('main_app:student_dashboard')
        
        # ===== SUBMIT DOUBT =====
        elif 'submit_doubt' in request.POST:
            form = DoubtSessionForm(request.POST)
            if form.is_valid():
                doubt = form.save(commit=False)
                doubt.student = request.user
                doubt.save()
                messages.success(request, 'Doubt submitted successfully!')
            else:
                messages.error(request, 'Please fill all fields!')
            
            return redirect('main_app:student_dashboard')
        
        # ===== SUBMIT COMPLAINT =====
        elif 'submit_complaint' in request.POST:
            form = ComplaintForm(request.POST)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.student = request.user
                complaint.save()
                messages.success(request, 'Complaint registered successfully!')
            else:
                messages.error(request, 'Please fill all fields!')
            
            return redirect('main_app:student_dashboard')
    
    context = {
        'cards': cards,
        'documents': documents,
        'uploaded_doc_types': uploaded_doc_types,
        'choices': choices,
        'status': status,
        'doubts': doubts,
        'complaints': complaints,
    }
    
    return render(request, 'student_dashboard.html', context)


# ==================== ADMIN - PROFESSIONAL COUNSELLING CARDS MANAGEMENT ====================


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_pro_counselling_cards_list(request):
    """List all Professional Counselling Cards"""
    cards = ProfessionalCounsellingCard.objects.all()
    return render(request, 'admin/pro_counselling_cards_list.html', {'cards': cards})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_pro_counselling_card_add(request):
    """Add new Professional Counselling Card"""
    if request.method == 'POST':
        form = ProfessionalCounsellingCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_pro_counselling_cards_list')
    else:
        form = ProfessionalCounsellingCardForm()
    
    return render(request, 'admin/pro_counselling_card_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_pro_counselling_card_edit(request, card_id):
    """Edit Professional Counselling Card"""
    card = get_object_or_404(ProfessionalCounsellingCard, id=card_id)
    
    if request.method == 'POST':
        form = ProfessionalCounsellingCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated successfully!')
            return redirect('main_app:admin_pro_counselling_cards_list')
    else:
        form = ProfessionalCounsellingCardForm(instance=card)
    
    return render(request, 'admin/pro_counselling_card_form.html', {'form': form, 'card': card})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_pro_counselling_card_delete(request, card_id):
    """Delete Professional Counselling Card"""
    card = get_object_or_404(ProfessionalCounsellingCard, id=card_id)
    
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted successfully!')
        return redirect('main_app:admin_pro_counselling_cards_list')
    
    return render(request, 'admin/pro_counselling_card_delete.html', {'card': card})


# ==================== ADMIN - VIEW ALL STUDENTS ====================
from .forms import *

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_students_list(request):
    """View all students"""
    from django.contrib.auth.models import User
    students = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')
    
    context = {'students': students}
    return render(request, 'admin/students_list.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_student_detail(request, student_id):
    """View individual student details"""
    from django.contrib.auth.models import User
    student = get_object_or_404(User, id=student_id, is_staff=False)
    
    documents = StudentDocument.objects.filter(student=student)
    choices = ChoiceFilling.objects.filter(student=student)
    status, created = CounsellingStatus.objects.get_or_create(student=student)
    doubts = DoubtSession.objects.filter(student=student)
    complaints = Complaint.objects.filter(student=student)
    
    context = {
        'student': student,
        'documents': documents,
        'choices': choices,
        'status': status,
        'doubts': doubts,
        'complaints': complaints,
    }
    
    return render(request, 'admin/student_detail.html', context)


# ==================== ADMIN - DOCUMENT APPROVAL ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_documents_list(request):
    """View all student documents"""
    documents = StudentDocument.objects.all().order_by('-uploaded_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        documents = documents.filter(status=status_filter)
    
    context = {'documents': documents}
    return render(request, 'admin/documents_list.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_document_review(request, doc_id):
    """Review and approve/reject document"""
    document = get_object_or_404(StudentDocument, id=doc_id)
    
    if request.method == 'POST':
        form = DocumentApprovalForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            
            # Update student status if all docs approved
            student = document.student
            all_docs = StudentDocument.objects.filter(student=student)
            if all(doc.status == 'approved' for doc in all_docs):
                status, created = CounsellingStatus.objects.get_or_create(student=student)
                status.documents_verified = True
                status.current_stage = 'documents_verification'
                status.save()
            
            messages.success(request, 'Document reviewed successfully!')
            return redirect('main_app:admin_documents_list')
    else:
        form = DocumentApprovalForm(instance=document)
    
    context = {'form': form, 'document': document}
    return render(request, 'admin/document_review.html', context)


# ==================== ADMIN - DOUBTS MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_doubts_list(request):
    """View all student doubts"""
    doubts = DoubtSession.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        doubts = doubts.filter(status=status_filter)
    
    context = {'doubts': doubts}
    return render(request, 'admin/doubts_list.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_doubt_respond(request, doubt_id):
    """Respond to student doubt"""
    doubt = get_object_or_404(DoubtSession, id=doubt_id)
    
    if request.method == 'POST':
        form = DoubtResponseForm(request.POST, instance=doubt)
        if form.is_valid():
            doubt_obj = form.save(commit=False)
            doubt_obj.responded_by = request.user
            doubt_obj.save()
            messages.success(request, 'Response submitted successfully!')
            return redirect('main_app:admin_doubts_list')
    else:
        form = DoubtResponseForm(instance=doubt)
    
    context = {'form': form, 'doubt': doubt}
    return render(request, 'admin/doubt_respond.html', context)


# ==================== ADMIN - COMPLAINTS MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_complaints_list(request):
    """View all complaints"""
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    context = {'complaints': complaints}
    return render(request, 'admin/complaints_list.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_complaint_respond(request, complaint_id):
    """Respond to complaint"""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        form = ComplaintResponseForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint_obj = form.save(commit=False)
            complaint_obj.responded_by = request.user
            complaint_obj.save()
            messages.success(request, 'Response submitted successfully!')
            return redirect('main_app:admin_complaints_list')
    else:
        form = ComplaintResponseForm(instance=complaint)
    
    context = {'form': form, 'complaint': complaint}
    return render(request, 'admin/complaint_respond.html', context)


# ==================== ADMIN - UPDATE COUNSELLING STATUS ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_update_status(request, student_id):
    """Update student's counselling status"""
    from django.contrib.auth.models import User
    student = get_object_or_404(User, id=student_id)
    status, created = CounsellingStatus.objects.get_or_create(student=student)
    
    if request.method == 'POST':
        form = CounsellingStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status updated successfully!')
            return redirect('main_app:admin_student_detail', student_id=student_id)
    else:
        form = CounsellingStatusForm(instance=status)
    
    context = {'form': form, 'student': student, 'status': status}
    return render(request, 'admin/update_status.html', context)


from .models import DistanceEducationCard, OnlineEducationCard
from .forms import DistanceEducationCardForm, OnlineEducationCardForm


# ==================== DISTANCE EDUCATION ====================
@never_cache
@login_required(login_url='main_app:user_login')
def distance_education_view(request):
    """Distance Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = DistanceEducationCard.objects.filter(is_active=True)
    return render(request, 'distance_education.html', {'cards': cards})


#@never_cache ADMIN - Distance Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_cards_list(request):
    cards = DistanceEducationCard.objects.all()
    return render(request, 'admin/distance_education_cards_list.html', {'cards': cards})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_card_add(request):
    if request.method == 'POST':
        form = DistanceEducationCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            
            # ✅ Auto-generate slug if empty
            if not card.slug:
                from django.utils.text import slugify
                card.slug = slugify(card.title)
            
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_distance_education_cards_list')
    else:
        form = DistanceEducationCardForm()
    
    return render(request, 'admin/distance_education_card_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_card_edit(request, card_id):
    card = get_object_or_404(DistanceEducationCard, id=card_id)
    if request.method == 'POST':
        form = DistanceEducationCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated!')
            return redirect('main_app:admin_distance_education_cards_list')
    else:
        form = DistanceEducationCardForm(instance=card)
    return render(request, 'admin/distance_education_card_form.html', {'form': form, 'card': card})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_card_delete(request, card_id):
    card = get_object_or_404(DistanceEducationCard, id=card_id)
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted!')
        return redirect('main_app:admin_distance_education_cards_list')
    return render(request, 'admin/distance_education_card_delete.html', {'card': card})


# ==================== ONLINE EDUCATION ====================
@never_cache
@login_required(login_url='main_app:user_login')
def online_education_view(request):
    """Online Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = OnlineEducationCard.objects.filter(is_active=True)
    return render(request, 'online_education.html', {'cards': cards})


#@never_cache ADMIN - Online Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_cards_list(request):
    cards = OnlineEducationCard.objects.all()
    return render(request, 'admin/online_education_cards_list.html', {'cards': cards})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_card_add(request):
    if request.method == 'POST':
        form = OnlineEducationCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_online_education_cards_list')
    else:
        form = OnlineEducationCardForm()
    return render(request, 'admin/online_education_card_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_card_edit(request, card_id):
    card = get_object_or_404(OnlineEducationCard, id=card_id)
    if request.method == 'POST':
        form = OnlineEducationCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated!')
            return redirect('main_app:admin_online_education_cards_list')
    else:
        form = OnlineEducationCardForm(instance=card)
    return render(request, 'admin/online_education_card_form.html', {'form': form, 'card': card})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_card_delete(request, card_id):
    card = get_object_or_404(OnlineEducationCard, id=card_id)
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted!')
        return redirect('main_app:admin_online_education_cards_list')
    return render(request, 'admin/online_education_card_delete.html', {'card': card})



from .models import DistanceEducationCard, OnlineEducationCard
from .forms import DistanceEducationCardForm, OnlineEducationCardForm

# ==================== DISTANCE EDUCATION ====================
@never_cache
@login_required(login_url='main_app:user_login')
def distance_education_view(request):
    """Distance Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = DistanceEducationCard.objects.filter(is_active=True)
    return render(request, 'distance_education.html', {'cards': cards})


#@never_cache ADMIN - Distance Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_cards_list(request):
    cards = DistanceEducationCard.objects.all()
    return render(request, 'admin/distance_education_cards_list.html', {'cards': cards})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_card_add(request):
    if request.method == 'POST':
        form = DistanceEducationCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_distance_education_cards_list')
    else:
        form = DistanceEducationCardForm()
    return render(request, 'admin/distance_education_card_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_card_edit(request, card_id):
    card = get_object_or_404(DistanceEducationCard, id=card_id)
    if request.method == 'POST':
        form = DistanceEducationCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated!')
            return redirect('main_app:admin_distance_education_cards_list')
    else:
        form = DistanceEducationCardForm(instance=card)
    return render(request, 'admin/distance_education_card_form.html', {'form': form, 'card': card})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_card_delete(request, card_id):
    card = get_object_or_404(DistanceEducationCard, id=card_id)
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted!')
        return redirect('main_app:admin_distance_education_cards_list')
    return render(request, 'admin/distance_education_card_delete.html', {'card': card})


# ==================== ONLINE EDUCATION ====================
@never_cache
@login_required(login_url='main_app:user_login')
def online_education_view(request):
    """Online Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = OnlineEducationCard.objects.filter(is_active=True)
    return render(request, 'online_education.html', {'cards': cards})


#@never_cache ADMIN - Online Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_cards_list(request):
    cards = OnlineEducationCard.objects.all()
    return render(request, 'admin/online_education_cards_list.html', {'cards': cards})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_card_add(request):
    if request.method == 'POST':
        form = OnlineEducationCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_online_education_cards_list')
    else:
        form = OnlineEducationCardForm()
    return render(request, 'admin/online_education_card_form.html', {'form': form})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_card_edit(request, card_id):
    card = get_object_or_404(OnlineEducationCard, id=card_id)
    if request.method == 'POST':
        form = OnlineEducationCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated!')
            return redirect('main_app:admin_online_education_cards_list')
    else:
        form = OnlineEducationCardForm(instance=card)
    return render(request, 'admin/online_education_card_form.html', {'form': form, 'card': card})


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_card_delete(request, card_id):
    card = get_object_or_404(OnlineEducationCard, id=card_id)
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted!')
        return redirect('main_app:admin_online_education_cards_list')
    return render(request, 'admin/online_education_card_delete.html', {'card': card})


from django.http import JsonResponse
from .models import Country, State, UserRegistration
from .forms import CountryForm, StateForm, UserRegistrationForm
from django.contrib.auth.hashers import make_password

# ==================== AJAX - LOAD STATES ====================
def load_states(request):
    """AJAX endpoint to load states based on country"""
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id, is_active=True).values('id', 'name')
    return JsonResponse(list(states), safe=False)


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse



from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Country, State  # Import your models

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Country, State

# ==================== USER REGISTRATION ====================
def user_register_view(request):
    """User Registration with Country Filtering based on 'next' URL"""
    
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('main_app:admin_dashboard')
        return redirect('main_app:admission_india_services')
    
    # ✅ Get parameters
    source_page = request.GET.get('from', 'direct')
    next_url = request.GET.get('next', None)
    
    # ✅ Determine country filter based on 'next' URL
    country_filter = 'all'  # Default
    
    if next_url:
        if 'admission-india' in next_url:
            country_filter = 'india_only'
        elif 'admission-abroad' in next_url:
            country_filter = 'exclude_india'
    
    if request.method == 'POST':
        # ✅ Pass country_filter to form
        form = UserRegistrationForm(
            request.POST, 
            country_filter=request.POST.get('country_filter', country_filter)
        )
        
        post_source = request.POST.get('source', source_page)
        post_next = request.POST.get('next', next_url)
        
        if form.is_valid():
            registration = form.save(commit=False)
            registration.password = make_password(form.cleaned_data['password'])
            registration.save()
            
            user = User.objects.create_user(
                username=registration.email,
                email=registration.email,
                password=form.cleaned_data['password']
            )
            registration.user = user
            registration.save()
            
            login(request, user)
            
            # ✅ Debug logs
            # print(f"✅ User registered: {registration.email}")
            # print(f"📍 Source: {post_source}")
            # print(f"🔗 Next URL: {post_next}")
            # print(f"🌍 Country Filter: {country_filter}")
            
            messages.success(request, f'Welcome {registration.name}!')
            
            if post_next:
                return redirect(post_next)
            else:
                return redirect('main_app:admission_india_services')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # ✅ Pass country_filter to form
        form = UserRegistrationForm(country_filter=country_filter)
    
    context = {
        'form': form,
        'source_page': source_page,
        'next_url': next_url,
        'country_filter': country_filter,  # For debugging
    }
    
    return render(request, 'user/register.html', context)


#@never_cache ==================== ADMIN - COUNTRIES ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_countries_list(request):
    countries = Country.objects.all()
    return render(request, 'admin/countries_list.html', {'countries': countries})
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_country_add(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Country added successfully!')
            return redirect('main_app:admin_countries_list')
    else:
        form = CountryForm()
    return render(request, 'admin/country_form.html', {'form': form})
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_country_edit(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            messages.success(request, 'Country updated!')
            return redirect('main_app:admin_countries_list')
    else:
        form = CountryForm(instance=country)
    return render(request, 'admin/country_form.html', {'form': form, 'country': country})
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_country_delete(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    if request.method == 'POST':
        country.delete()
        messages.success(request, 'Country deleted!')
        return redirect('main_app:admin_countries_list')
    return render(request, 'admin/country_delete.html', {'country': country})


#@never_cache ==================== ADMIN - STATES ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_states_list(request):
    states = State.objects.all()
    return render(request, 'admin/states_list.html', {'states': states})
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_state_add(request):
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'State added successfully!')
            return redirect('main_app:admin_states_list')
    else:
        form = StateForm()
    return render(request, 'admin/state_form.html', {'form': form})
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_state_edit(request, state_id):
    state = get_object_or_404(State, id=state_id)
    if request.method == 'POST':
        form = StateForm(request.POST, instance=state)
        if form.is_valid():
            form.save()
            messages.success(request, 'State updated!')
            return redirect('main_app:admin_states_list')
    else:
        form = StateForm(instance=state)
    return render(request, 'admin/state_form.html', {'form': form, 'state': state})
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_state_delete(request, state_id):
    state = get_object_or_404(State, id=state_id)
    if request.method == 'POST':
        state.delete()
        messages.success(request, 'State deleted!')
        return redirect('main_app:admin_states_list')
    return render(request, 'admin/state_delete.html', {'state': state})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import College, CollegeComparison, Country, State, UserRegistration

#@never_cache ==================== ADMIN: COLLEGES LIST ====================
@login_required
def admin_colleges_list(request):
    """Admin dashboard - All colleges list"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    colleges = College.objects.all().order_by('-created_at')
    
    context = {
        'colleges': colleges,
    }
    return render(request, 'admin/colleges_list.html', context)



## **Views mein ek fix (`views.py` mein update karo)**


#@never_cache ==================== ADMIN: ADD COLLEGE ====================
@login_required
def admin_college_add(request):
    """Admin dashboard - Add new college"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        country_id = request.POST.get('country')
        state_id = request.POST.get('state')
        city = request.POST.get('city')
        ranking = request.POST.get('ranking') or None
        tuition_fees = request.POST.get('tuition_fees')
        courses_offered = request.POST.get('courses_offered')
        facilities = request.POST.get('facilities')
        image_url = request.POST.get('image_url')
        website = request.POST.get('website')
        is_active = request.POST.get('is_active') == 'true'  # FIX: Handle checkbox
        
        college_image = request.FILES.get('college_image')
        
        try:
            country = Country.objects.get(id=country_id)
            state = State.objects.get(id=state_id)
            
            college = College.objects.create(
                name=name,
                country=country,
                state=state,
                city=city,
                ranking=ranking,
                tuition_fees=tuition_fees,
                courses_offered=courses_offered,
                facilities=facilities,
                college_image=college_image,
                image_url=image_url,
                website=website,
                is_active=is_active,  # FIX: Add this
            )
            
            messages.success(request, f"College '{name}' added successfully!")
            return redirect('main_app:admin_colleges_list')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    countries = Country.objects.filter(is_active=True)
    states = State.objects.filter(is_active=True)
    
    context = {
        'countries': countries,
        'states': states,
    }
    return render(request, 'admin/college_add.html', context)


#@never_cache ==================== ADMIN: EDIT COLLEGE ====================
@login_required
def admin_college_edit(request, pk):
    """Admin dashboard - Edit college"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    college = get_object_or_404(College, pk=pk)
    
    if request.method == 'POST':
        college.name = request.POST.get('name')
        college.country_id = request.POST.get('country')
        college.state_id = request.POST.get('state')
        college.city = request.POST.get('city')
        college.ranking = request.POST.get('ranking') or None
        college.tuition_fees = request.POST.get('tuition_fees')
        college.courses_offered = request.POST.get('courses_offered')
        college.facilities = request.POST.get('facilities')
        college.image_url = request.POST.get('image_url')
        college.website = request.POST.get('website')
        college.is_active = request.POST.get('is_active') == 'true'  # FIX: Handle checkbox
        
        if request.FILES.get('college_image'):
            college.college_image = request.FILES.get('college_image')
        
        college.save()
        
        messages.success(request, "College updated successfully!")
        return redirect('main_app:admin_colleges_list')
    
    countries = Country.objects.filter(is_active=True)
    states = State.objects.filter(is_active=True)
    
    context = {
        'college': college,
        'countries': countries,
        'states': states,
    }
    return render(request, 'admin/college_edit.html', context)

#@never_cache ==================== ADMIN: DELETE COLLEGE ====================
@login_required
def admin_college_delete(request, pk):
    """Admin dashboard - Delete college"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    college = get_object_or_404(College, pk=pk)
    college_name = college.name
    college.delete()
    
    messages.success(request, f"College '{college_name}' deleted successfully!")
    return redirect('main_app:admin_colleges_list')


#@never_cache ==================== ADMIN: COMPARISONS LIST ====================
@login_required
def admin_comparisons_list(request):
    """Admin dashboard - All comparisons list"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    comparisons = CollegeComparison.objects.all().order_by('-created_at')
    
    context = {
        'comparisons': comparisons,
    }
    return render(request, 'admin/comparisons_list.html', context)


# ==================== ADMIN: ADD COMPARISON ====================
#@never_cache ==================== ADMIN: ADD COMPARISON (UPDATED) ====================
@login_required
def admin_comparison_add(request):
    """Admin dashboard - Add new comparison with multiple colleges"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    if request.method == 'POST':
        comparison_title = request.POST.get('comparison_title')
        college_ids = request.POST.getlist('colleges')  # CHANGE: Get multiple colleges
        country_id = request.POST.get('country')
        state_id = request.POST.get('state') or None
        comparison_summary = request.POST.get('comparison_summary')
        status = request.POST.get('status')
        
        try:
            # Validation: At least 2 colleges required
            if len(college_ids) < 2:
                messages.error(request, "Please select at least 2 colleges to compare!")
                return redirect('main_app:admin_comparison_add')
            
            country = Country.objects.get(id=country_id)
            state = State.objects.get(id=state_id) if state_id else None
            
            # Create comparison
            comparison = CollegeComparison.objects.create(
                comparison_title=comparison_title,
                country=country,
                state=state,
                comparison_summary=comparison_summary,
                status=status,
                created_by=request.user
            )
            
            # Add colleges (ManyToMany)
            comparison.colleges.set(college_ids)
            
            messages.success(request, f"Comparison '{comparison_title}' created successfully with {len(college_ids)} colleges!")
            return redirect('main_app:admin_comparisons_list')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    colleges = College.objects.filter(is_active=True).order_by('name')
    countries = Country.objects.filter(is_active=True)
    states = State.objects.filter(is_active=True)
    
    context = {
        'colleges': colleges,
        'countries': countries,
        'states': states,
    }
    return render(request, 'admin/comparison_add.html', context)


#@never_cache ==================== ADMIN: EDIT COMPARISON (UPDATED) ====================
@login_required
def admin_comparison_edit(request, pk):
    """Admin dashboard - Edit comparison"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    comparison = get_object_or_404(CollegeComparison, pk=pk)
    
    if request.method == 'POST':
        comparison.comparison_title = request.POST.get('comparison_title')
        comparison.country_id = request.POST.get('country')
        comparison.state_id = request.POST.get('state') or None
        comparison.comparison_summary = request.POST.get('comparison_summary')
        comparison.status = request.POST.get('status')
        
        college_ids = request.POST.getlist('colleges')
        
        # Validation: At least 2 colleges
        if len(college_ids) < 2:
            messages.error(request, "Please select at least 2 colleges to compare!")
            return redirect('main_app:admin_comparison_edit', pk=pk)
        
        comparison.save()
        comparison.colleges.set(college_ids)  # Update ManyToMany
        
        messages.success(request, "Comparison updated successfully!")
        return redirect('main_app:admin_comparisons_list')
    
    colleges = College.objects.filter(is_active=True).order_by('name')
    countries = Country.objects.filter(is_active=True)
    states = State.objects.filter(is_active=True)
    
    context = {
        'comparison': comparison,
        'colleges': colleges,
        'countries': countries,
        'states': states,
        'selected_colleges': list(comparison.colleges.values_list('id', flat=True)),  # Selected colleges IDs
    }
    return render(request, 'admin/comparison_edit.html', context)


#@never_cache ==================== STUDENT: VIEW COMPARISON DETAIL (UPDATED) ====================
@login_required
def student_comparison_detail(request, pk):
    """Student side - Detailed comparison view for multiple colleges"""
    comparison = get_object_or_404(CollegeComparison, pk=pk, status='active')
    
    # Get all colleges in comparison
    colleges_data = []
    for college in comparison.colleges.all():
        courses = [course.strip() for course in college.courses_offered.split(',')]
        colleges_data.append({
            'college': college,
            'courses': courses,
        })
    
    context = {
        'comparison': comparison,
        'colleges_data': colleges_data,
    }
    return render(request, 'student/comparison_detail.html', context)


#@never_cache ==================== ADMIN: DELETE COMPARISON ====================
@login_required
def admin_comparison_delete(request, pk):
    """Admin dashboard - Delete comparison"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    comparison = get_object_or_404(CollegeComparison, pk=pk)
    comparison_title = comparison.comparison_title
    comparison.delete()
    
    messages.success(request, f"Comparison '{comparison_title}' deleted successfully!")
    return redirect('main_app:admin_comparisons_list')






# ==================== STUDENT: VIEW COMPARISONS ====================
# ==================== STUDENT: VIEW COMPARISONS ====================




from django.db.models import Q
@never_cache
@login_required
def student_comparisons_list(request):
    """Student side - View comparisons with filters for custom selection"""
    
    # Get user's default location
    user_country = None
    user_state = None
    default_view = True  # Flag to show if showing default user's location
    
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
        user_country = user_registration.country
        user_state = user_registration.state
    except UserRegistration.DoesNotExist:
        pass
    
    # Get filter parameters from GET request
    filter_country_id = request.GET.get('country')
    filter_state_id = request.GET.get('state')
    search_query = request.GET.get('search', '').strip()
    
    # Start with active comparisons
    comparisons = CollegeComparison.objects.filter(status='active')
    
    # Apply filters based on user selection
    if filter_country_id:
        # User selected a specific country - show that country's comparisons
        default_view = False
        comparisons = comparisons.filter(country_id=filter_country_id)
        
        if filter_state_id:
            # User also selected a state
            comparisons = comparisons.filter(Q(state_id=filter_state_id) | Q(state__isnull=True))
        
        # Get selected country/state objects for display
        selected_country = Country.objects.filter(id=filter_country_id).first()
        selected_state = State.objects.filter(id=filter_state_id).first() if filter_state_id else None
    
    else:
        # No filter applied - show user's country/state by default
        if user_country:
            comparisons = comparisons.filter(country=user_country)
            
            if user_state:
                comparisons = comparisons.filter(Q(state=user_state) | Q(state__isnull=True))
        
        selected_country = user_country
        selected_state = user_state
    
    # Search filter (search in title, summary, or college names)
    if search_query:
        comparisons = comparisons.filter(
            Q(comparison_title__icontains=search_query) |
            Q(comparison_summary__icontains=search_query) |
            Q(colleges__name__icontains=search_query)
        ).distinct()
    
    # Get all countries and states for filter dropdowns
    all_countries = Country.objects.filter(is_active=True).order_by('name')
    all_states = State.objects.filter(is_active=True).order_by('country__name', 'name')
    
    context = {
        'comparisons': comparisons,
        'user_country': user_country,
        'user_state': user_state,
        'all_countries': all_countries,
        'all_states': all_states,
        'selected_country': selected_country,
        'selected_state': selected_state,
        'search_query': search_query,
        'default_view': default_view,
    }
    return render(request, 'student/comparisons_list.html', context)


from .models import StateWiseCounsellingUpdate

#@never_cache ==================== ADMIN: STATE COUNSELLING UPDATES LIST ====================
@login_required
def admin_state_counselling_list(request):
    """Admin dashboard - State wise counselling updates list"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    updates = StateWiseCounsellingUpdate.objects.all().order_by('state', 'order')
    
    context = {
        'updates': updates,
    }
    return render(request, 'admin/state_counselling_list.html', context)


#@never_cache ==================== ADMIN: ADD STATE COUNSELLING UPDATE ====================
@login_required
def admin_state_counselling_add(request):
    """Admin dashboard - Add new state counselling update"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    if request.method == 'POST':
        state_id = request.POST.get('state')
        title = request.POST.get('title')
        description = request.POST.get('description')
        external_link = request.POST.get('external_link')
        icon_url = request.POST.get('icon_url')
        icon_color = request.POST.get('icon_color')
        last_updated = request.POST.get('last_updated') or None
        is_new = request.POST.get('is_new') == 'on'
        order = request.POST.get('order') or 0
        status = request.POST.get('status')
        
        icon_image = request.FILES.get('icon_image')
        
        try:
            state = State.objects.get(id=state_id)
            
            update = StateWiseCounsellingUpdate.objects.create(
                state=state,
                title=title,
                description=description,
                external_link=external_link,
                icon_image=icon_image,
                icon_url=icon_url,
                icon_color=icon_color,
                last_updated=last_updated,
                is_new=is_new,
                order=order,
                status=status,
                created_by=request.user
            )
            
            messages.success(request, f"Update '{title}' added successfully!")
            return redirect('main_app:admin_state_counselling_list')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    states = State.objects.filter(is_active=True).order_by('name')
    
    context = {
        'states': states,
    }
    return render(request, 'admin/state_counselling_add.html', context)


#@never_cache ==================== ADMIN: EDIT STATE COUNSELLING UPDATE ====================
@login_required
def admin_state_counselling_edit(request, pk):
    """Admin dashboard - Edit state counselling update"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    update = get_object_or_404(StateWiseCounsellingUpdate, pk=pk)
    
    if request.method == 'POST':
        update.state_id = request.POST.get('state')
        update.title = request.POST.get('title')
        update.description = request.POST.get('description')
        update.external_link = request.POST.get('external_link')
        update.icon_url = request.POST.get('icon_url')
        update.icon_color = request.POST.get('icon_color')
        update.last_updated = request.POST.get('last_updated') or None
        update.is_new = request.POST.get('is_new') == 'on'
        update.order = request.POST.get('order') or 0
        update.status = request.POST.get('status')
        
        if request.FILES.get('icon_image'):
            update.icon_image = request.FILES.get('icon_image')
        
        update.save()
        
        messages.success(request, "Update edited successfully!")
        return redirect('main_app:admin_state_counselling_list')
    
    states = State.objects.filter(is_active=True).order_by('name')
    
    context = {
        'update': update,
        'states': states,
    }
    return render(request, 'admin/state_counselling_edit.html', context)


#@never_cache ==================== ADMIN: DELETE STATE COUNSELLING UPDATE ====================
@login_required
def admin_state_counselling_delete(request, pk):
    """Admin dashboard - Delete state counselling update"""
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('main_app:home')
    
    update = get_object_or_404(StateWiseCounsellingUpdate, pk=pk)
    title = update.title
    update.delete()
    
    messages.success(request, f"Update '{title}' deleted successfully!")
    return redirect('main_app:admin_state_counselling_list')


# ==================== STUDENT: STATE WISE COUNSELLING UPDATES ====================
def state_wise_counselling_updates(request):
    """Student side - State wise counselling updates page"""
    
    # Get user's state if logged in
    user_state = None
    if request.user.is_authenticated:
        try:
            user_registration = UserRegistration.objects.get(user=request.user)
            user_state = user_registration.state
        except UserRegistration.DoesNotExist:
            pass
    
    # Get all active updates grouped by state
    updates = StateWiseCounsellingUpdate.objects.filter(status='active').order_by('state', 'order')
    
    # Group updates by state
    states_updates = {}
    for update in updates:
        state_name = update.state.name
        if state_name not in states_updates:
            states_updates[state_name] = []
        states_updates[state_name].append(update)
    
    context = {
        'states_updates': states_updates,
        'user_state': user_state,
    }
    return render(request, 'student/state_counselling_updates.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AllIndiaServiceCard, SubCategory, ContentPage

# ==================== ADMIN: SUB-CATEGORIES MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_categories_list(request):
    """Admin dashboard - All sub-categories list"""
    # ✅ CHANGE: contentpage_set → content_pages
    sub_categories = SubCategory.objects.all().select_related(
        'parent_card', 'state', 'created_by'
    ).prefetch_related('content_pages').order_by('parent_card', 'order')
    
    # Calculate stats
    total_subcategories = sub_categories.count()
    active_subcategories = sub_categories.filter(is_active=True).count()
    inactive_subcategories = sub_categories.filter(is_active=False).count()
    
    # Count total pages across all sub-categories
    from django.db.models import Count
    total_pages = ContentPage.objects.count()
    
    context = {
        'sub_categories': sub_categories,
        'total_subcategories': total_subcategories,
        'active_subcategories': active_subcategories,
        'inactive_subcategories': inactive_subcategories,
        'total_pages': total_pages,
    }
    return render(request, 'admin/sub_categories_list.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_category_add(request):
    """Admin dashboard - Add new sub-category"""
    if request.method == 'POST':
        parent_card_id = request.POST.get('parent_card')
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        icon_url = request.POST.get('icon_url')
        icon_color = request.POST.get('icon_color')
        order = request.POST.get('order') or 0
        is_active = request.POST.get('is_active') == 'on'
        
        icon_image = request.FILES.get('icon_image')
        
        try:
            parent_card = AllIndiaServiceCard.objects.get(id=parent_card_id)
            
            # Auto-generate slug if not provided
            if not slug:
                from django.utils.text import slugify
                slug = slugify(title)
            
            sub_category = SubCategory.objects.create(
                parent_card=parent_card,
                title=title,
                slug=slug,
                description=description,
                icon_image=icon_image,
                icon_url=icon_url,
                icon_color=icon_color,
                order=order,
                is_active=is_active,
                created_by=request.user
            )
            
            messages.success(request, f"Sub-category '{title}' added successfully!")
            return redirect('main_app:admin_sub_categories_list')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    parent_cards = AllIndiaServiceCard.objects.filter(is_active=True).order_by('title')
    
    context = {
        'parent_cards': parent_cards,
    }
    return render(request, 'admin/sub_category_add.html', context)



@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_category_edit(request, pk):
    """Admin dashboard - Edit sub-category"""
    sub_category = get_object_or_404(SubCategory, pk=pk)
    
    if request.method == 'POST':
        sub_category.title = request.POST.get('title')
        sub_category.slug = request.POST.get('slug')
        sub_category.description = request.POST.get('description')
        sub_category.order = request.POST.get('order') or 0
        sub_category.is_active = request.POST.get('is_active') == 'on'
        sub_category.icon_color = request.POST.get('icon_color')
        
        # State and course filters
        state_id = request.POST.get('state')
        sub_category.state_id = state_id if state_id else None
        
        course = request.POST.get('course')
        sub_category.course = course if course else None
        
        # Handle icon upload
        if request.FILES.get('icon_image'):
            sub_category.icon_image = request.FILES.get('icon_image')
            sub_category.icon_url = ''
        else:
            icon_url = request.POST.get('icon_url', '').strip()
            if icon_url:
                sub_category.icon_url = icon_url
        
        sub_category.save()
        
        messages.success(request, f"Sub-category '{sub_category.title}' updated successfully!")
        
        if sub_category.parent_subcategory:
            root = sub_category.parent_subcategory
            while root.parent_subcategory:
                root = root.parent_subcategory
            if root.parent_card:
                return redirect('main_app:admin_sub_categories_by_card', root.parent_card.id)
        elif sub_category.parent_card:
            return redirect('main_app:admin_sub_categories_by_card', sub_category.parent_card.id)
        
        return redirect('main_app:admin_sub_categories_list')
    
    # GET request
    # ✅ Find root parent card
    def get_root_parent_card(subcategory):
        if subcategory.parent_subcategory:
            root = subcategory.parent_subcategory
            while root.parent_subcategory:
                root = root.parent_subcategory
            return root.parent_card
        return subcategory.parent_card
    
    # ✅ Calculate full path
    def get_full_path(subcategory):
        path = []
        current = subcategory
        
        # Build path from child to parent
        while current:
            path.insert(0, current.title)
            current = current.parent_subcategory
        
        # Add root card
        root_card = get_root_parent_card(subcategory)
        if root_card:
            path.insert(0, root_card.title)
        
        return " → ".join(path)
    
    root_parent_card = get_root_parent_card(sub_category)
    full_path = get_full_path(sub_category)
    
    try:
        india = Country.objects.get(name='India')
        states = State.objects.filter(country=india).order_by('name')
    except Country.DoesNotExist:
        states = State.objects.filter(country__name__icontains='India').order_by('name')
    
    courses = [
        ('btech', 'B.Tech'),
        ('mtech', 'M.Tech'),
        ('bba', 'BBA'),
        ('mba', 'MBA'),
        ('bca', 'BCA'),
        ('mca', 'MCA'),
        ('bsc', 'B.Sc'),
        ('msc', 'M.Sc'),
        ('ba', 'B.A'),
        ('ma', 'M.A'),
    ]
    
    parent_cards = AllIndiaServiceCard.objects.filter(is_active=True).order_by('title')
    
    context = {
        'subcategory': sub_category,
        'root_parent_card': root_parent_card,  # ✅ Root card
        'full_path': full_path,  # ✅ Full path
        'parent_cards': parent_cards,
        'states': states,
        'courses': courses,
    }
    return render(request, 'admin/sub_category_edit.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_category_delete(request, pk):
    """Admin dashboard - Delete sub-category"""
    sub_category = get_object_or_404(SubCategory, pk=pk)
    title = sub_category.title
    sub_category.delete()
    
    messages.success(request, f"Sub-category '{title}' deleted successfully!")
    return redirect('main_app:admin_sub_categories_list')


# ==================== ADMIN: CONTENT PAGES MANAGEMENT ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_pages_list(request):
    """Admin dashboard - All content pages list"""
    pages = ContentPage.objects.all().select_related('sub_category__parent_card').order_by('sub_category', 'order')
    
    # Calculate stats
    total_pages = pages.count()
    active_pages = pages.filter(is_active=True).count()
    featured_pages = pages.filter(is_featured=True).count()
    inactive_pages = pages.filter(is_active=False).count()
    
    context = {
        'pages': pages,
        'total_pages': total_pages,
        'active_pages': active_pages,
        'featured_pages': featured_pages,
        'inactive_pages': inactive_pages,
    }
    return render(request, 'admin/content_pages_list.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_page_add(request):
    """Admin dashboard - Add new content page"""
    if request.method == 'POST':
        sub_category_id = request.POST.get('sub_category')
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        featured_image_url = request.POST.get('featured_image_url')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        order = request.POST.get('order') or 0
        is_active = request.POST.get('is_active') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        
        featured_image = request.FILES.get('featured_image')
        
        try:
            sub_category = SubCategory.objects.get(id=sub_category_id)
            
            # Auto-generate slug if not provided
            if not slug:
                from django.utils.text import slugify
                slug = slugify(title)
            
            page = ContentPage.objects.create(
                sub_category=sub_category,
                title=title,
                slug=slug,
                summary=summary,
                content=content,
                featured_image=featured_image,
                featured_image_url=featured_image_url,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                order=order,
                is_active=is_active,
                is_featured=is_featured,
                created_by=request.user
            )
            
            messages.success(request, f"Page '{title}' added successfully!")
            return redirect('main_app:admin_content_pages_list')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    sub_categories = SubCategory.objects.filter(is_active=True).select_related('parent_card').order_by('parent_card', 'title')
    
    context = {
        'sub_categories': sub_categories,
    }
    return render(request, 'admin/content_page_add.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_page_edit(request, pk):
    """Admin dashboard - Edit content page"""
    page = get_object_or_404(ContentPage, pk=pk)
    
    if request.method == 'POST':
        page.sub_category_id = request.POST.get('sub_category')
        page.country_id = request.POST.get('country') or None
        page.state_id = request.POST.get('state') or None
        page.course = request.POST.get('course') or None  # Direct field, not FK
        page.title = request.POST.get('title')
        page.slug = request.POST.get('slug')
        page.summary = request.POST.get('summary')
        page.content = request.POST.get('content')
        page.featured_image_url = request.POST.get('featured_image_url')
        page.meta_description = request.POST.get('meta_description')
        page.meta_keywords = request.POST.get('meta_keywords')
        page.order = request.POST.get('order') or 0
        page.is_active = request.POST.get('is_active') == 'on'
        page.is_featured = request.POST.get('is_featured') == 'on'
        
        if request.FILES.get('featured_image'):
            page.featured_image = request.FILES.get('featured_image')
        
        page.save()
        
        messages.success(request, "Page updated successfully!")
        return redirect('main_app:admin_content_pages_list')
    
    # Get dropdown data
    sub_categories = SubCategory.objects.filter(is_active=True).select_related('parent_card').order_by('parent_card', 'title')
    countries = Country.objects.filter(is_active=True).order_by('name')
    
    # Get states for selected country
    states = []
    if page.country_id:
        states = State.objects.filter(country_id=page.country_id, is_active=True).order_by('name')
    
    # Get course choices from UserRegistration model
    course_choices = UserRegistration.COURSE_CHOICES
    
    context = {
        'page': page,
        'sub_categories': sub_categories,
        'countries': countries,
        'states': states,
        'course_choices': course_choices,
    }
    return render(request, 'admin/content_page_edit.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_page_delete(request, pk):
    """Admin dashboard - Delete content page"""
    page = get_object_or_404(ContentPage, pk=pk)
    title = page.title
    page.delete()
    
    messages.success(request, f"Page '{title}' deleted successfully!")
    return redirect('main_app:admin_content_pages_list')


#@never_cache ==================== ADMIN: SUB-CATEGORIES BY CARD ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_categories_by_card(request, card_id):
    """Admin dashboard - Sub-categories for specific card"""
    parent_card = get_object_or_404(AllIndiaServiceCard, pk=card_id)
    sub_categories = SubCategory.objects.filter(parent_card=parent_card).order_by('order')
    
    context = {
        'parent_card': parent_card,
        'sub_categories': sub_categories,
    }
    return render(request, 'admin/sub_categories_by_card.html', context)

# views.py mein UPDATE karo

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import AllIndiaServiceCard, SubCategory, State, UserRegistration

def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_category_add_for_card(request, card_id):
    """Admin dashboard - Add sub-category for specific card with State & Course filters"""
    parent_card = get_object_or_404(AllIndiaServiceCard, pk=card_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        
        # ✅ NEW: Get State & Course
        state_id = request.POST.get('state')
        course = request.POST.get('course')
        
        icon_url = request.POST.get('icon_url')
        icon_color = request.POST.get('icon_color')
        order = request.POST.get('order') or 0
        is_active = request.POST.get('is_active') == 'on'
        
        icon_image = request.FILES.get('icon_image')
        
        try:
            if not slug:
                from django.utils.text import slugify
                slug = slugify(title)
            
            # ✅ Handle State (optional)
            state = None
            if state_id:
                state = State.objects.get(pk=state_id)
            
            # ✅ Create SubCategory with State & Course
            sub_category = SubCategory.objects.create(
                parent_card=parent_card,
                title=title,
                slug=slug,
                description=description,
                state=state,  # ✅ NEW
                course=course if course else None,  # ✅ NEW
                icon_image=icon_image,
                icon_url=icon_url,
                icon_color=icon_color,
                order=order,
                is_active=is_active,
                created_by=request.user
            )
            
            messages.success(request, f"Sub-category '{title}' added successfully!")
            return redirect('main_app:admin_sub_categories_by_card', card_id=card_id)
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    # ✅ Pass only Indian states and courses to template
    context = {
        'parent_card': parent_card,
        'states': State.objects.filter(is_active=True, country__name='India').order_by('name'),
        'courses': UserRegistration.COURSE_CHOICES,  # Course choices
    }
    return render(request, 'admin/sub_category_add.html', context)





#@never_cache ==================== ADMIN: CONTENT PAGES BY SUB-CATEGORY ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_pages_by_subcategory(request, subcategory_id):
    """Admin dashboard - Pages for specific sub-category"""
    sub_category = get_object_or_404(SubCategory, pk=subcategory_id)
    pages = ContentPage.objects.filter(sub_category=sub_category).order_by('order')
    
    context = {
        'sub_category': sub_category,
        'pages': pages,
    }
    return render(request, 'admin/content_pages_by_subcategory.html', context)




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse
from .models import SubCategory, State
from .forms import ContentPageForm

# ==================== AJAX: Get States by Country (Reuse same function) ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def get_states_by_country(request):
    """AJAX endpoint to get states based on selected country"""
    country_id = request.GET.get('country_id')
    
    if country_id:
        states = State.objects.filter(
            country_id=country_id, 
            is_active=True
        ).values('id', 'name').order_by('name')
        return JsonResponse({'states': list(states)})
    
    return JsonResponse({'states': []})


# ==================== ADMIN: ADD CONTENT PAGE ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_page_add_for_subcategory(request, subcategory_id):
    """Admin dashboard - Add page for specific sub-category"""
    sub_category = get_object_or_404(SubCategory, pk=subcategory_id)
    
    if request.method == 'POST':
        form = ContentPageForm(request.POST, request.FILES)
        
        if form.is_valid():
            page = form.save(commit=False)
            page.sub_category = sub_category
            page.created_by = request.user
            
            # Auto-generate slug if not provided
            if not page.slug:
                from django.utils.text import slugify
                page.slug = slugify(page.title)
            
            page.save()
            messages.success(request, f"Page '{page.title}' added successfully!")
            return redirect('main_app:admin_content_pages_by_subcategory', subcategory_id=subcategory_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Pre-fill sub_category in the form
        form = ContentPageForm(initial={'sub_category': sub_category})
    
    # DEBUG - Remove after testing
    print("Countries count:", form.fields['country'].queryset.count())
    print("Course choices count:", len(form.fields['course'].choices))
    
    context = {
        'sub_category': sub_category,
        'form': form,
    }

    return render(request, 'admin/content_page_add.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AllIndiaServiceCard, SubCategory, ContentPage

# ==================== STUDENT: CARD DETAIL (SUB-CATEGORIES LIST) ====================
# views.py mein YE VIEW UPDATE KARO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import AllIndiaServiceCard, SubCategory, UserRegistration
@never_cache
@login_required(login_url='main_app:user_login')
def card_detail_view(request, card_slug):
    """
    Student side - Show FILTERED sub-categories for a card
    URL: /all-india-services/rti/
    
    ✅ Shows only subcategories matching student's STATE and COURSE
    """
    # Check if admin
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins should use admin panel.')
        return redirect('main_app:admin_dashboard')
    
    # Get card by slug or redirect_link
    card = get_object_or_404(AllIndiaServiceCard, 
                            redirect_link__icontains=card_slug, 
                            is_active=True)
    
    # ✅ STEP 1: Get logged-in user's STATE and COURSE
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
        user_state = user_registration.state
        user_course = user_registration.course
    except UserRegistration.DoesNotExist:
        # If user hasn't completed registration, show all subcategories
        user_state = None
        user_course = None
    
    # ✅ STEP 2: Filter sub-categories by STATE and COURSE
    sub_categories = SubCategory.objects.filter(
        parent_card=card, 
        is_active=True
    )
    
    # ✅ FILTER BY STATE: Show if (matches user's state) OR (no state filter set)
    if user_state:
        sub_categories = sub_categories.filter(
            Q(state=user_state) | Q(state__isnull=True)
        )
    else:
        # If user has no state, show only subcategories with no state filter
        sub_categories = sub_categories.filter(state__isnull=True)
    
    # ✅ FILTER BY COURSE: Show if (matches user's course) OR (no course filter set)
    if user_course:
        sub_categories = sub_categories.filter(
            Q(course=user_course) | Q(course__isnull=True) | Q(course='')
        )
    else:
        # If user has no course, show only subcategories with no course filter
        sub_categories = sub_categories.filter(
            Q(course__isnull=True) | Q(course='')
        )
    
    # Order by display order
    sub_categories = sub_categories.order_by('order')
    
    # ✅ STEP 3: Pass to template
    context = {
        'card': card,
        'sub_categories': sub_categories,
        'user_state': user_state,
        'user_course': user_course,
        'total_filtered': sub_categories.count(),
    }
    
    return render(request, 'student/card_detail.html', context)

#@never_cache ==================== STUDENT: SUB-CATEGORY DETAIL (PAGES LIST) ====================
@login_required(login_url='main_app:user_login')
def subcategory_detail_view(request, card_slug, subcategory_path):
    """
    Show subcategory with filtered pages
    """
    
    # Get student data
    try:
        student = UserRegistration.objects.get(user=request.user)
        student_country = student.country
        student_state = student.state
        student_course = student.course
    except UserRegistration.DoesNotExist:
        student_country = None
        student_state = None
        student_course = None
    
    # Get card
    card = get_object_or_404(AllIndiaServiceCard, 
                            redirect_link__icontains=card_slug, 
                            is_active=True)
    
    # Parse path and get subcategory
    slugs = subcategory_path.strip('/').split('/')
    current_subcategory = None
    
    for slug in slugs:
        if current_subcategory is None:
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
    
    # Get child subcategories
    child_subcategories = SubCategory.objects.filter(
        parent_subcategory=current_subcategory,
        is_active=True
    ).order_by('order')
    
    # ✅ Get pages with filtering
    pages_query = Q(
        sub_category=current_subcategory,
        is_active=True
    )
    
    if student_country or student_state or student_course:
        pages_query &= (
            Q(country__isnull=True) | Q(country=student_country)
        ) & (
            Q(state__isnull=True) | Q(state=student_state)
        ) & (
            Q(course__isnull=True) | Q(course='') | Q(course=student_course)
        )
    
    pages = ContentPage.objects.filter(pages_query).order_by('order', '-created_at')
    
    context = {
        'card': card,
        'sub_category': current_subcategory,
        'child_subcategories': child_subcategories,
        'pages': pages,
        'breadcrumb': current_subcategory.get_breadcrumb(),
        'student': student,
    }
    
    return render(request, 'student/subcategory_detail.html', context)


#@never_cache ==================== STUDENT: PAGE DETAIL (FULL CONTENT) ====================
from django.db.models import Q

from django.db.models import Q
from django.http import Http404

@login_required(login_url='main_app:user_login')
def page_detail_view(request, card_slug, subcategory_path, page_slug):
    """
    Show individual page OR redirect to subcategory if page doesn't exist
    WITH Country, State, Course filtering
    """
    
    # ✅ STEP 1: Get student data
    try:
        student = UserRegistration.objects.get(user=request.user)
        student_country = student.country
        student_state = student.state
        student_course = student.course
    except UserRegistration.DoesNotExist:
        student_country = None
        student_state = None
        student_course = None
    
    # ✅ STEP 2: Get card with filtering
    card_query = Q(redirect_link__icontains=card_slug, is_active=True)
    
    if student_country or student_state or student_course:
        card_query &= (
            Q(country__isnull=True) | Q(country=student_country)
        ) & (
            Q(state__isnull=True) | Q(state=student_state)
        ) & (
            Q(course__isnull=True) | Q(course='') | Q(course=student_course)
        )
    
    card = get_object_or_404(AllIndiaServiceCard, card_query)
    
    # ✅ STEP 3: Parse path and get subcategory with filtering
    slugs = subcategory_path.strip('/').split('/')
    
    current_subcategory = None
    for slug in slugs:
        if current_subcategory is None:
            # First level subcategory
            subcat_query = Q(
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            # Nested subcategory
            subcat_query = Q(
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
        
        # Apply filtering for subcategories
        if student_country or student_state or student_course:
            subcat_query &= (
                Q(country__isnull=True) | Q(country=student_country)
            ) & (
                Q(state__isnull=True) | Q(state=student_state)
            ) & (
                Q(course__isnull=True) | Q(course='') | Q(course=student_course)
            )
        
        current_subcategory = get_object_or_404(SubCategory, subcat_query)
    
    # ✅ STEP 4: Try to find page with filtering
    page_query = Q(
        sub_category=current_subcategory,
        slug=page_slug,
        is_active=True
    )
    
    # Apply smart filtering based on student data
    if student_country or student_state or student_course:
        page_query &= (
            Q(country__isnull=True) | Q(country=student_country)
        ) & (
            Q(state__isnull=True) | Q(state=student_state)
        ) & (
            Q(course__isnull=True) | Q(course='') | Q(course=student_course)
        )
    
    try:
        page = ContentPage.objects.get(page_query)
        
        # ✅ Page found - show it
        page.views_count += 1
        page.save(update_fields=['views_count'])
        
        # Get related pages with same filtering
        related_query = Q(
            sub_category=current_subcategory,
            is_active=True
        ) & ~Q(id=page.id)
        
        if student_country or student_state or student_course:
            related_query &= (
                Q(country__isnull=True) | Q(country=student_country)
            ) & (
                Q(state__isnull=True) | Q(state=student_state)
            ) & (
                Q(course__isnull=True) | Q(course='') | Q(course=student_course)
            )
        
        related_pages = ContentPage.objects.filter(related_query).order_by('order', '-created_at')[:5]
        
        context = {
            'page': page,
            'card': card,
            'sub_category': current_subcategory,
            'breadcrumb': current_subcategory.get_breadcrumb(),
            'related_pages': related_pages,
            'student': student,
        }
        return render(request, 'student/page_detail.html', context)
    
    except ContentPage.DoesNotExist:
        # ✅ FALLBACK: Check if page_slug is actually a nested subcategory
        nested_query = Q(
            slug=page_slug,
            parent_subcategory=current_subcategory,
            is_active=True
        )
        
        if student_country or student_state or student_course:
            nested_query &= (
                Q(country__isnull=True) | Q(country=student_country)
            ) & (
                Q(state__isnull=True) | Q(state=student_state)
            ) & (
                Q(course__isnull=True) | Q(course='') | Q(course=student_course)
            )
        
        try:
            nested_sub = SubCategory.objects.get(nested_query)
            
            # It's a subcategory! Redirect to subcategory view
            full_path = f"{subcategory_path}/{page_slug}/"
            return redirect('main_app:subcategory_detail_view', 
                          card_slug=card_slug, 
                          subcategory_path=full_path)
        
        except SubCategory.DoesNotExist:
            # Neither page nor subcategory found
            raise Http404("Content not found or not accessible for your profile")
        
        
# views.py mein YE VIEWS ADD KARO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import AllIndiaServiceCard, SubCategory, ContentPage

# Helper function (if not already present)
def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


#@never_cache ==================== NESTED SUBCATEGORIES VIEW ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_nested_subcategories(request, parent_subcategory_id):
    """
    Shows child subcategories of a parent subcategory
    URL: /admin/subcategory/<id>/children/
    """
    current_parent_subcategory = get_object_or_404(SubCategory, pk=parent_subcategory_id)
    
    # Get child subcategories
    sub_categories = SubCategory.objects.filter(
        parent_subcategory=current_parent_subcategory,
        is_active=True
    ).order_by('order')
    
    # Get breadcrumb path
    breadcrumb_path = current_parent_subcategory.get_breadcrumb()[:-1]  # Exclude current
    
    # Get parent card (navigate up the tree)
    parent_card = None
    temp = current_parent_subcategory
    while temp:
        if temp.parent_card:
            parent_card = temp.parent_card
            break
        temp = temp.parent_subcategory
    
    context = {
        'current_parent_subcategory': current_parent_subcategory,
        'sub_categories': sub_categories,
        'breadcrumb_path': breadcrumb_path,
        'parent_card': parent_card,
    }
    return render(request, 'admin/nested_subcategories_list.html', context)


#@never_cache ==================== ADD NESTED SUBCATEGORY ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_nested_subcategory_add(request, parent_subcategory_id):
    """
    Add a child subcategory under a parent subcategory
    """
    parent_subcategory = get_object_or_404(SubCategory, pk=parent_subcategory_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        icon_url = request.POST.get('icon_url')
        icon_color = request.POST.get('icon_color')
        order = request.POST.get('order') or 0
        is_active = request.POST.get('is_active') == 'on'
        
        icon_image = request.FILES.get('icon_image')
        
        try:
            # Auto-generate slug if not provided
            if not slug:
                from django.utils.text import slugify
                slug = slugify(title)
            
            sub_category = SubCategory.objects.create(
                parent_subcategory=parent_subcategory,  # Set parent subcategory
                parent_card=None,  # No direct card parent
                title=title,
                slug=slug,
                description=description,
                icon_image=icon_image,
                icon_url=icon_url,
                icon_color=icon_color,
                order=order,
                is_active=is_active,
                created_by=request.user
            )
            
            messages.success(request, f"✓ Sub-category '{title}' added under '{parent_subcategory.title}'!")
            return redirect('main_app:admin_nested_subcategories', parent_subcategory_id=parent_subcategory_id)
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    context = {
        'parent_subcategory': parent_subcategory,
        'breadcrumb_path': parent_subcategory.get_breadcrumb(),
    }
    return render(request, 'admin/nested_subcategory_add.html', context)


# ==================== UPDATE EXISTING VIEW ====================
#@never_cache Update your existing admin_sub_categories_by_card view
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_categories_by_card(request, card_id):
    """
    Shows TOP-LEVEL subcategories for a card (no parent_subcategory)
    """
    parent_card = get_object_or_404(AllIndiaServiceCard, pk=card_id)
    
    # Only get direct children (no parent_subcategory)
    sub_categories = SubCategory.objects.filter(
        parent_card=parent_card,
        parent_subcategory__isnull=True  # Important: only top-level
    ).order_by('order')
    
    context = {
        'parent_card': parent_card,
        'sub_categories': sub_categories,
        'current_parent_subcategory': None,
        'breadcrumb_path': [],
    }
    return render(request, 'admin/nested_subcategories_list.html', context)


from django.db.models import Q
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='main_app:user_login')
def subcategory_detail_view(request, card_slug, subcategory_path):
    """
    Student side - Navigate through nested subcategories
    WITH STRICT Course filtering
    """
    
    # Get student data
    try:
        student = UserRegistration.objects.get(user=request.user)
        student_country = student.country
        student_state = student.state
        student_course = student.course
        
        # ✅ DEBUG: Print student info
        print(f"DEBUG: Student Course = {student_course}")
        print(f"DEBUG: Student Country = {student_country}")
        print(f"DEBUG: Student State = {student_state}")
        
    except UserRegistration.DoesNotExist:
        student_country = None
        student_state = None
        student_course = None
    
    # Get card
    card = get_object_or_404(
        AllIndiaServiceCard, 
        redirect_link__icontains=card_slug, 
        is_active=True
    )
    
    # Parse nested path
    slugs = subcategory_path.strip('/').split('/')
    
    current_subcategory = None
    for slug in slugs:
        if current_subcategory is None:
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
    
    # Get child subcategories
    children = current_subcategory.get_children()
    
    # ✅ BUILD QUERY with STRICT filtering
    pages_query = Q(sub_category=current_subcategory, is_active=True)
    
    # ✅ CRITICAL: Only show pages that match OR have no filter set
    if student_course:
        # Show pages with matching course OR no course filter
        pages_query &= (Q(course__isnull=True) | Q(course='') | Q(course=student_course))
    
    if student_country:
        pages_query &= (Q(country__isnull=True) | Q(country=student_country))
    
    if student_state:
        pages_query &= (Q(state__isnull=True) | Q(state=student_state))
    
    # Get pages
    pages = ContentPage.objects.filter(pages_query).order_by('order', '-created_at')
    
    # ✅ DEBUG: Print filtered pages
    print(f"\nDEBUG: Total pages found = {pages.count()}")
    for page in pages:
        print(f"  - Page: {page.title}, Course: {page.course}, Country: {page.country}, State: {page.state}")
    
    # Render template
    if children.exists():
        context = {
            'card': card,
            'sub_category': current_subcategory,
            'sub_categories': children,
            'pages': pages,
            'breadcrumb': current_subcategory.get_breadcrumb(),
            'student': student,
        }
        return render(request, 'student/subcategory_children.html', context)
    else:
        context = {
            'card': card,
            'sub_category': current_subcategory,
            'pages': pages,
            'breadcrumb': current_subcategory.get_breadcrumb(),
            'student': student,
        }
        return render(request, 'student/subcategory_pages.html', context)
# views.py - YE VIEW UPDATE KARO

from django.http import Http404

from django.db.models import Q

@login_required(login_url='main_app:user_login')
def page_detail_view(request, card_slug, subcategory_path, page_slug):
    """
    Show individual page OR redirect to subcategory if page doesn't exist
    WITH Country, State, Course filtering
    """
    
    # Get student registration data
    try:
        student = UserRegistration.objects.get(user=request.user)
        student_country = student.country
        student_state = student.state
        student_course = student.course
    except UserRegistration.DoesNotExist:
        student_country = None
        student_state = None
        student_course = None
    
    # Get card
    card = get_object_or_404(AllIndiaServiceCard, 
                            redirect_link__icontains=card_slug, 
                            is_active=True)
    
    # Parse path
    slugs = subcategory_path.strip('/').split('/')
    
    # Navigate to find current subcategory
    current_subcategory = None
    for slug in slugs:
        if current_subcategory is None:
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
    
    # ✅ BUILD QUERY with filtering
    page_query = Q(
        sub_category=current_subcategory,
        slug=page_slug,
        is_active=True
    )
    
    # Apply smart filtering based on student data
    if student_country or student_state or student_course:
        page_query &= (
            Q(country__isnull=True) | Q(country=student_country)  # No country filter OR matching country
        ) & (
            Q(state__isnull=True) | Q(state=student_state)        # No state filter OR matching state
        ) & (
            Q(course__isnull=True) | Q(course='') | Q(course=student_course)  # No course filter OR matching course
        )
    
    # ✅ TRY: Find page with filtering
    try:
        page = ContentPage.objects.get(page_query)
        
        # Page found - show it
        page.views_count += 1
        page.save(update_fields=['views_count'])
        
        # Get related pages with same filtering
        related_query = Q(
            sub_category=current_subcategory,
            is_active=True
        ) & ~Q(id=page.id)
        
        if student_country or student_state or student_course:
            related_query &= (
                Q(country__isnull=True) | Q(country=student_country)
            ) & (
                Q(state__isnull=True) | Q(state=student_state)
            ) & (
                Q(course__isnull=True) | Q(course='') | Q(course=student_course)
            )
        
        related_pages = ContentPage.objects.filter(related_query).order_by('order', '-created_at')[:5]
        
        context = {
            'page': page,
            'card': card,
            'sub_category': current_subcategory,
            'breadcrumb': current_subcategory.get_breadcrumb(),
            'related_pages': related_pages,
            'student': student,
        }
        return render(request, 'student/page_detail.html', context)
    
    except ContentPage.DoesNotExist:
        # ✅ FALLBACK: Check if page_slug is actually a nested subcategory
        try:
            nested_sub = SubCategory.objects.get(
                slug=page_slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
            
            # It's a subcategory! Redirect to subcategory view
            full_path = f"{subcategory_path}/{page_slug}/"
            return redirect('main_app:subcategory_detail_view', 
                          card_slug=card_slug, 
                          subcategory_path=full_path)
        
        except SubCategory.DoesNotExist:
            # Neither page nor subcategory - show 404
            raise Http404("Content not found or not accessible for your profile")
# abroad india 
# views.py mein add karo
# Admin - Sub-categories by Card
# Add these views to your views.py (REPLACE the incomplete admission abroad section at the bottom)

from .models import AdmissionAbroadCard, AdmissionAbroadSubCategory, AdmissionAbroadPage
from .forms import AdmissionAbroadCardForm, AdmissionAbroadSubCategoryForm, AdmissionAbroadPageForm

# ==================== PUBLIC VIEW (LOGIN REQUIRED) ====================
# ==================== PUBLIC VIEW (LOGIN REQUIRED) ====================
# ==================== PUBLIC VIEW (LOGIN REQUIRED) ====================
# ==================== PUBLIC VIEW (LOGIN REQUIRED) ====================
# ==================== PUBLIC VIEW (LOGIN REQUIRED) ====================

@never_cache
@login_required(login_url='main_app:user_login')
def admission_abroad_view(request):
    """Admission Abroad Services Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins can access from admin panel.')
        return redirect('main_app:admin_dashboard')    
    cards = AdmissionAbroadCard.objects.filter(is_active=True).order_by('order')
    context = {'cards': cards}
    return render(request, 'admission_abroad.html', context)

# ==================== ADMIN: CARDS MANAGEMENT ====================


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_cards_list(request):
    """List all Admission Abroad cards"""
    cards = AdmissionAbroadCard.objects.all().order_by('order')
    return render(request, 'admin/admission_abroad_cards_list.html', {'cards': cards})

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_card_add(request):
    """Add new Admission Abroad card"""
    if request.method == 'POST':
        form = AdmissionAbroadCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.created_by = request.user
            card.save()
            messages.success(request, 'Card added successfully!')
            return redirect('main_app:admin_admission_abroad_cards_list')
    else:
        form = AdmissionAbroadCardForm()
    
    return render(request, 'admin/admission_abroad_card_form.html', {'form': form})

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_card_edit(request, card_id):
    """Edit Admission Abroad card"""
    card = get_object_or_404(AdmissionAbroadCard, id=card_id)
    
    if request.method == 'POST':
        form = AdmissionAbroadCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated successfully!')
            return redirect('main_app:admin_admission_abroad_cards_list')
    else:
        form = AdmissionAbroadCardForm(instance=card)
    
    return render(request, 'admin/admission_abroad_card_form.html', {'form': form, 'card': card})

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_card_delete(request, card_id):
    """Delete Admission Abroad card"""
    card = get_object_or_404(AdmissionAbroadCard, id=card_id)
    
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Card deleted successfully!')
        return redirect('main_app:admin_admission_abroad_cards_list')
    
    return render(request, 'admin/admission_abroad_card_delete.html', {'card': card})


# ==================== ADMIN: SUBCATEGORIES BY CARD ====================

from django.db.models import Count
@never_cache
@login_required(login_url='main_app:admin_login')
def admin_admission_abroad_subcategories(request, card_id):
    """
    List all TOP-LEVEL subcategories under a specific card
    """
    card = get_object_or_404(AdmissionAbroadCard, id=card_id)
    
    # ✅ Use annotate to add children_count directly in query
    subcategories = AdmissionAbroadSubCategory.objects.filter(
        parent_card=card,
        parent_subcategory__isnull=True
    ).annotate(
        children_count=Count('children')  # ✅ Directly count children
    ).order_by('order', 'title')
    
    context = {
        'card': card,
        'subcategories': subcategories,
    }
    
    return render(request, 'admin/admission_abroad_subcategories.html', context)


# ==================== ADMIN: ADD SUBCATEGORY FOR CARD ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_subcategory_add(request, card_id=None, parent_id=None):
    """Add subcategory - either under card or under parent subcategory"""
    
    if request.method == 'POST':
        form = AdmissionAbroadSubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.created_by = request.user
            subcategory.save()
            messages.success(request, 'Subcategory added successfully!')
            
            # Redirect back to appropriate view
            if parent_id:
                return redirect('main_app:admin_admission_abroad_nested_subcategories', parent_id=parent_id)
            elif card_id:
                return redirect('main_app:admin_admission_abroad_subcategories', card_id=card_id)
            else:
                return redirect('main_app:admin_admission_abroad_cards_list')
    else:
        form = AdmissionAbroadSubCategoryForm()
        
        # Set initial values if card_id or parent_id provided
        if card_id:
            form.initial['parent_card'] = get_object_or_404(AdmissionAbroadCard, pk=card_id)
        if parent_id:
            form.initial['parent_subcategory'] = get_object_or_404(AdmissionAbroadSubCategory, pk=parent_id)
    
    context = {
        'form': form,
        'card_id': card_id,
        'parent_id': parent_id,
    }
    return render(request, 'admin/admission_abroad_subcategory_form.html', context)


#@never_cache ==================== ADMIN: NESTED SUBCATEGORIES ====================
@login_required(login_url='main_app:admin_login')
def admin_admission_abroad_nested_subcategories(request, parent_id):
    """
    List all child subcategories under a parent subcategory
    """
    parent = get_object_or_404(AdmissionAbroadSubCategory, id=parent_id)
    
    # ✅ Use annotate here too
    subcategories = AdmissionAbroadSubCategory.objects.filter(
        parent_subcategory=parent
    ).annotate(
        children_count=Count('children')  # ✅ Directly count children
    ).order_by('order', 'title')
    
    # Build breadcrumb
    breadcrumb = parent.get_breadcrumb() if hasattr(parent, 'get_breadcrumb') else []
    
    context = {
        'parent': parent,
        'subcategories': subcategories,
        'breadcrumb': breadcrumb,
    }
    
    return render(request, 'admin/admission_abroad_nested_subcategories.html', context)



# ==================== ADMIN: CONTENT PAGES FOR SUBCATEGORY ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_pages_by_subcategory(request, subcategory_id):
    """View content pages for a subcategory"""
    subcategory = get_object_or_404(AdmissionAbroadSubCategory, pk=subcategory_id)
    pages = subcategory.content_pages.all().order_by('order')
    
    context = {
        'subcategory': subcategory,
        'pages': pages,
        'breadcrumb': subcategory.get_breadcrumb(),
    }
    return render(request, 'admin/admission_abroad_pages_list.html', context)



from django.http import JsonResponse

# ==================== AJAX: Get States by Country ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def get_states_by_country(request):
    """AJAX endpoint to get states based on selected country"""
    country_id = request.GET.get('country_id')
    
    if country_id:
        states = State.objects.filter(
            country_id=country_id, 
            is_active=True
        ).values('id', 'name').order_by('name')
        return JsonResponse({'states': list(states)})
    
    return JsonResponse({'states': []})


# ==================== ADMIN: ADD CONTENT PAGE FOR SUBCATEGORY ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_page_add(request, subcategory_id):
    """Add content page for subcategory"""
    subcategory = get_object_or_404(AdmissionAbroadSubCategory, pk=subcategory_id)
    
    if request.method == 'POST':
        form = AdmissionAbroadPageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.sub_category = subcategory
            page.created_by = request.user
            page.save()
            messages.success(request, 'Page added successfully!')
            return redirect('main_app:admin_admission_abroad_pages_by_subcategory', subcategory_id=subcategory_id)
    else:
        form = AdmissionAbroadPageForm(initial={'sub_category': subcategory})
    
    context = {
        'form': form,
        'subcategory': subcategory,
    }
    return render(request, 'admin/admission_abroad_page_form.html', context)


# ==================== STUDENT: FRONTEND VIEWS ====================


# views.py mein YE VIEW UPDATE KARO

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import AdmissionAbroadCard, AdmissionAbroadSubCategory, UserRegistration
@never_cache
@login_required(login_url='main_app:user_login')
def admission_abroad_card_detail(request, card_slug):
    """
    Student: Display main card with FILTERED subcategories
    ✅ Filters by: Student State + Course
    """
    card = get_object_or_404(AdmissionAbroadCard, 
                            slug=card_slug, 
                            is_active=True)
    
    # ✅ STEP 1: Get logged-in user's STATE and COURSE
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
        user_state = user_registration.state
        user_course = user_registration.course
    except UserRegistration.DoesNotExist:
        # If user hasn't completed registration, show all subcategories
        user_state = None
        user_course = None
    
    # ✅ STEP 2: Get TOP-LEVEL subcategories with FILTERING
    subcategories = card.sub_categories.filter(
        is_active=True, 
        parent_subcategory__isnull=True  # Only top-level
    )
    
    # ✅ FILTER BY STUDENT STATE: Show if (matches user's state) OR (no state filter)
    if user_state:
        subcategories = subcategories.filter(
            Q(student_state=user_state) | Q(student_state__isnull=True)
        )
    else:
        # If user has no state, show only subcategories with no state filter
        subcategories = subcategories.filter(student_state__isnull=True)
    
    # ✅ FILTER BY COURSE: Show if (matches user's course) OR (no course filter)
    if user_course:
        subcategories = subcategories.filter(
            Q(course=user_course) | Q(course__isnull=True) | Q(course='')
        )
    else:
        # If user has no course, show only subcategories with no course filter
        subcategories = subcategories.filter(
            Q(course__isnull=True) | Q(course='')
        )
    
    # Order by display order
    subcategories = subcategories.order_by('order')
    
    # ✅ DEBUG: Print karo
    print(f"Card: {card.title}")
    print(f"User State: {user_state}")
    print(f"User Course: {user_course}")
    print(f"Filtered Subcategories: {subcategories.count()}")
    for sub in subcategories:
        print(f"  - {sub.title} (slug: {sub.slug})")
    
    # ✅ STEP 3: Pass to template
    context = {
        'card': card,
        'subcategories': subcategories,
        'user_state': user_state,
        'user_course': user_course,
        'total_filtered': subcategories.count(),
    }
    
    return render(request, 'student/admission_abroad_card_detail.html', context)

@never_cache
@login_required(login_url='main_app:user_login')
def admission_abroad_subcategory_detail(request, card_slug, subcategory_path):
    """Student: Display subcategory with children or pages"""
    card = get_object_or_404(AdmissionAbroadCard, slug=card_slug, is_active=True)
    
    # Parse nested path: "engineering/government/delhi"
    path_parts = subcategory_path.strip('/').split('/')
    
    # Navigate through the path to find current subcategory
    current_subcategory = None
    for slug in path_parts:
        if current_subcategory is None:
            # First level - find under card
            current_subcategory = get_object_or_404(
                AdmissionAbroadSubCategory,
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            # Nested level - find under parent
            current_subcategory = get_object_or_404(
                AdmissionAbroadSubCategory,
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
    
    # Get children and pages
    children = current_subcategory.get_children()
    pages = current_subcategory.content_pages.filter(is_active=True).order_by('order')
    
    # Build current path for nested links
    current_path = subcategory_path.rstrip('/')
    
    context = {
        'card': card,
        'subcategory': current_subcategory,
        'children': children,
        'pages': pages,
        'current_path': current_path,  # ✅ Pass this to template
        'breadcrumb': current_subcategory.get_breadcrumb(),
    }
    
    return render(request, 'student/admission_abroad_subcategory_detail.html', context)



@never_cache
@login_required(login_url='main_app:user_login')
def admission_abroad_page_detail(request, card_slug, subcategory_path, page_slug):
    """Student: Display full page content OR child subcategory"""
    
    print("="*50)
    print(f"🔍 VIEW CALLED: admission_abroad_page_detail")
    print(f"📌 card_slug: {card_slug}")
    print(f"📌 subcategory_path: {subcategory_path}")
    print(f"📌 page_slug: {page_slug}")
    print("="*50)
    
    card = get_object_or_404(AdmissionAbroadCard, slug=card_slug, is_active=True)
    
    # Get subcategory from path
    path_parts = subcategory_path.strip('/').split('/')
    current_slug = path_parts[-1]
    
    print(f"🔍 Looking for subcategory with slug: {current_slug}")
    
    subcategory = get_object_or_404(
        AdmissionAbroadSubCategory,
        slug=current_slug,
        is_active=True
    )
    
    print(f"✅ Subcategory found: {subcategory}")
    
    # PEHLE CHECK KARO - KYA YEH EK PAGE HAI?
    try:
        page = AdmissionAbroadPage.objects.get(
            sub_category=subcategory,
            slug=page_slug,
            is_active=True
        )
        
        print(f"✅ PAGE FOUND: {page}")
        print(f"📄 Rendering template: student/admission_abroad_page_detail.html")
        
        page.increment_views()
        
        related_pages = subcategory.content_pages.filter(
            is_active=True
        ).exclude(id=page.id).order_by('order')[:5]
        
        context = {
            'card': card,
            'subcategory': subcategory,
            'page': page,
            'related_pages': related_pages,
            'breadcrumb': subcategory.get_breadcrumb(),
        }
        
        return render(request, 'student/admission_abroad_page_detail.html', context)
    
    except AdmissionAbroadPage.DoesNotExist:
        print(f"❌ PAGE NOT FOUND")
        print(f"🔍 Checking if it's a CHILD SUBCATEGORY...")
        
        try:
            child_subcategory = AdmissionAbroadSubCategory.objects.get(
                slug=page_slug,
                parent_subcategory=subcategory,
                is_active=True
            )
            
            print(f"✅ CHILD SUBCATEGORY FOUND: {child_subcategory}")
            print(f"📄 Rendering template: student/admission_abroad_subcategory_detail.html")
            
            # ✅ SAB KUCH DIKHAO - NO FILTERING!
            children = child_subcategory.children.filter(is_active=True).order_by('order')
            pages = child_subcategory.content_pages.filter(is_active=True).order_by('order')
            
            print(f"✅ Total children: {children.count()}")
            print(f"✅ Total pages: {pages.count()}")
            
            current_path = f"{subcategory_path.rstrip('/')}/{page_slug}"
            
            context = {
                'card': card,
                'subcategory': child_subcategory,
                'children': children,
                'pages': pages,
                'current_path': current_path,
                'breadcrumb': child_subcategory.get_breadcrumb(),
            }
            
            return render(request, 'student/admission_abroad_subcategory_detail.html', context)
        
        except AdmissionAbroadSubCategory.DoesNotExist:
            print(f"❌ CHILD SUBCATEGORY ALSO NOT FOUND")
            print(f"🚫 Raising 404")
            raise Http404("Page or Subcategory not found")




# views.py mein UPDATE karo




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import AdmissionAbroadCard, AdmissionAbroadSubCategory, Country, State, UserRegistration
@never_cache
@login_required(login_url='main_app:admin_login')
def admin_admission_abroad_nested_subcategory_add(request, parent_id):
    """
    Add a new subcategory under either a Card or another Subcategory
    with Country, State & Course filtering
    """
    parent_card = None
    parent_subcategory = None
    
    # Try to find if parent_id is a Card
    try:
        parent_card = AdmissionAbroadCard.objects.get(id=parent_id)
    except AdmissionAbroadCard.DoesNotExist:
        # If not a card, try to find if it's a subcategory
        try:
            parent_subcategory = AdmissionAbroadSubCategory.objects.get(id=parent_id)
            # Get the root card from the subcategory
            parent_card = parent_subcategory.get_root_card()
        except AdmissionAbroadSubCategory.DoesNotExist:
            messages.error(request, "Invalid parent ID")
            return redirect('main_app:admin_admission_abroad_cards_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug', '').strip()
        description = request.POST.get('description', '')
        
        # ✅ NEW: Get Country, State & Course
        target_country_id = request.POST.get('target_country')
        student_state_id = request.POST.get('student_state')
        course = request.POST.get('course')
        
        icon_image = request.FILES.get('icon_image')
        icon_url = request.POST.get('icon_url', '')
        icon_color = request.POST.get('icon_color', '#007bff')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # Auto-generate slug if empty
        if not slug:
            slug = slugify(title)
        
        # ✅ Handle Country (optional)
        target_country = None
        if target_country_id:
            try:
                target_country = Country.objects.get(pk=target_country_id)
            except Country.DoesNotExist:
                pass
        
        # ✅ Handle State (optional)
        student_state = None
        if student_state_id:
            try:
                student_state = State.objects.get(pk=student_state_id)
            except State.DoesNotExist:
                pass
        
        # Create subcategory
        subcategory = AdmissionAbroadSubCategory.objects.create(
            parent_card=parent_card,
            parent_subcategory=parent_subcategory,
            title=title,
            slug=slug,
            description=description,
            target_country=target_country,  # ✅ NEW
            student_state=student_state,    # ✅ NEW
            course=course if course else None,  # ✅ NEW
            icon_image=icon_image,
            icon_url=icon_url,
            icon_color=icon_color,
            order=order or 0,
            is_active=is_active,
            created_by=request.user
        )
        
        messages.success(request, f"Subcategory '{title}' added successfully!")
        
        # Redirect back to the parent view
        if parent_subcategory:
            return redirect('main_app:admin_admission_abroad_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_admission_abroad_subcategories', card_id=parent_card.id)
    
    # Build breadcrumb
    breadcrumb = []
    if parent_subcategory:
        breadcrumb = parent_subcategory.get_breadcrumb()
    elif parent_card:
        breadcrumb = [{'id': parent_card.id, 'title': parent_card.title}]
    
    # ✅ Pass Countries, States & Courses to template
    context = {
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'card_id': parent_card.id if parent_card else None,
        'parent_id': parent_subcategory.id if parent_subcategory else None,
        'countries': Country.objects.filter(is_active=True).order_by('name'),  # ✅ NEW
        'states': State.objects.filter(is_active=True).order_by('name'),       # ✅ NEW
        'courses': UserRegistration.COURSE_CHOICES,                            # ✅ NEW
    }
    
    return render(request, 'admin/admission_abroad_subcategory_form.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_subcategory_edit(request, subcategory_id):
    """
    Edit an existing subcategory
    """
    subcategory = get_object_or_404(AdmissionAbroadSubCategory, id=subcategory_id)
    parent_card = subcategory.get_root_card()
    parent_subcategory = subcategory.parent_subcategory
    
    if request.method == 'POST':
        form = AdmissionAbroadSubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.created_by = request.user
            subcategory.save()
            
            messages.success(request, f"Subcategory '{subcategory.title}' updated successfully!")
            
            # Redirect back to appropriate list
            if parent_subcategory:
                return redirect('main_app:admin_admission_abroad_nested_subcategories', parent_id=parent_subcategory.id)
            else:
                return redirect('main_app:admin_admission_abroad_subcategories', card_id=parent_card.id)
    else:
        # GET request - populate form with existing data
        form = AdmissionAbroadSubCategoryForm(instance=subcategory)
    
    # Build breadcrumb
    breadcrumb = subcategory.get_breadcrumb() if hasattr(subcategory, 'get_breadcrumb') else []
    
    context = {
        'form': form,
        'subcategory': subcategory,
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'is_edit': True,
        'card_id': parent_card.id if parent_card else None,
        'parent_id': parent_subcategory.id if parent_subcategory else None,
        
        # ✅ YE NAMES TEMPLATE KE MATCH HONE CHAHIYE
        'countries': Country.objects.filter(is_active=True).order_by('name'),
        'states': State.objects.filter(is_active=True).order_by('name'),
        'courses': UserRegistration.COURSE_CHOICES,  # ✅ YE ALREADY TUPLE LIST HAI
    }
    
    return render(request, 'admin/admission_abroad_subcategory_form.html', context)



@never_cache
@login_required(login_url='main_app:admin_login')
def admin_admission_abroad_subcategory_delete(request, subcategory_id):
    """
    Delete a subcategory
    """
    subcategory = get_object_or_404(AdmissionAbroadSubCategory, id=subcategory_id)
    parent_card = subcategory.get_root_card()
    parent_subcategory = subcategory.parent_subcategory
    
    # Check if it has children
    if subcategory.children.exists():
        messages.error(request, f"Cannot delete '{subcategory.title}' because it has child subcategories!")
        if parent_subcategory:
            return redirect('main_app:admin_admission_abroad_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_admission_abroad_subcategories', card_id=parent_card.id)
    
    # Delete the subcategory
    title = subcategory.title
    subcategory.delete()
    
    messages.success(request, f"Subcategory '{title}' deleted successfully!")
    
    # Redirect back to appropriate list
    if parent_subcategory:
        return redirect('main_app:admin_admission_abroad_nested_subcategories', parent_id=parent_subcategory.id)
    else:
        return redirect('main_app:admin_admission_abroad_subcategories', card_id=parent_card.id)
    

# ==================== DISTANCE EDUCATION - NESTED STRUCTURE ====================

from .models import DistanceEducationCard, DistanceEducationSubCategory, DistanceEducationPage
from .forms import DistanceEducationSubCategoryForm, DistanceEducationPageForm

# ==================== ADMIN: SUBCATEGORIES BY CARD ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_subcategories(request, card_id):
    """List all TOP-LEVEL subcategories under a specific card"""
    card = get_object_or_404(DistanceEducationCard, id=card_id)
    
    subcategories = DistanceEducationSubCategory.objects.filter(
        parent_card=card,
        parent_subcategory__isnull=True
    ).annotate(
        children_count=Count('children')
    ).order_by('order', 'title')
    
    context = {
        'card': card,
        'subcategories': subcategories,
    }
    
    return render(request, 'admin/distance_education_subcategories.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_nested_subcategories(request, parent_id):
    """List all child subcategories under a parent subcategory"""
    parent = get_object_or_404(DistanceEducationSubCategory, id=parent_id)
    
    subcategories = DistanceEducationSubCategory.objects.filter(
        parent_subcategory=parent
    ).annotate(
        children_count=Count('children')
    ).order_by('order', 'title')
    
    breadcrumb = parent.get_breadcrumb() if hasattr(parent, 'get_breadcrumb') else []
    
    context = {
        'parent': parent,
        'subcategories': subcategories,
        'breadcrumb': breadcrumb,
    }
    
    return render(request, 'admin/distance_education_nested_subcategories.html', context)


# views.py mein admin_distance_education_nested_subcategory_add UPDATE karo
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_nested_subcategory_add(request, parent_id):
    """Add a new subcategory under either a Card or another Subcategory"""
    parent_card = None
    parent_subcategory = None
    
    # Check if it's a subcategory
    try:
        parent_subcategory = DistanceEducationSubCategory.objects.get(id=parent_id)
        parent_card = parent_subcategory.get_root_card()
    except DistanceEducationSubCategory.DoesNotExist:
        # If not a subcategory, then it must be a card
        try:
            parent_card = DistanceEducationCard.objects.get(id=parent_id)
        except DistanceEducationCard.DoesNotExist:
            messages.error(request, "Invalid parent ID")
            return redirect('main_app:admin_distance_education_cards_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug', '').strip()
        description = request.POST.get('description', '')
        
        # ✅ NEW: Get Country, State & Course
        target_country_id = request.POST.get('target_country')
        student_state_id = request.POST.get('student_state')
        course = request.POST.get('course')
        
        icon_image = request.FILES.get('icon_image')
        icon_url = request.POST.get('icon_url', '')
        icon_color = request.POST.get('icon_color', '#007bff')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # Auto-generate slug if empty
        if not slug:
            from django.utils.text import slugify
            slug = slugify(title)
        
        # ✅ Handle Country & State
        target_country = None
        student_state = None
        
        if target_country_id:
            try:
                target_country = Country.objects.get(pk=target_country_id)
            except Country.DoesNotExist:
                pass
        
        if student_state_id:
            try:
                student_state = State.objects.get(pk=student_state_id)
            except State.DoesNotExist:
                pass
        
        # Create subcategory
        new_subcategory = DistanceEducationSubCategory.objects.create(
            parent_card=parent_card if not parent_subcategory else None,
            parent_subcategory=parent_subcategory,
            title=title,
            slug=slug,
            description=description,
            target_country=target_country,  # ✅ NEW
            student_state=student_state,    # ✅ NEW
            course=course if course else None,  # ✅ NEW
            icon_image=icon_image,
            icon_url=icon_url,
            icon_color=icon_color,
            order=order or 0,
            is_active=is_active,
            created_by=request.user
        )
        
        messages.success(request, f"✓ Subcategory '{title}' added successfully!")
        
        # Redirect back
        if parent_subcategory:
            return redirect('main_app:admin_distance_education_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_distance_education_subcategories', card_id=parent_card.id)
    
    # Build breadcrumb
    breadcrumb = []
    if parent_subcategory:
        breadcrumb = parent_subcategory.get_breadcrumb()
    elif parent_card:
        breadcrumb = [{'id': parent_card.id, 'title': parent_card.title}]
    
    # ✅ Pass Countries, States & Courses to template
    context = {
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'card_id': parent_card.id if parent_card else None,
        'parent_id': parent_subcategory.id if parent_subcategory else None,
        'countries': Country.objects.filter(is_active=True).order_by('name'),  # ✅ NEW
        'states': State.objects.filter(is_active=True).order_by('name'),       # ✅ NEW
        'courses': UserRegistration.COURSE_CHOICES,                            # ✅ NEW
    }
    
    return render(request, 'admin/distance_education_subcategory_form.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_subcategory_edit(request, subcategory_id):
    """Edit an existing subcategory"""
    subcategory = get_object_or_404(DistanceEducationSubCategory, id=subcategory_id)
    parent_card = subcategory.get_root_card()
    parent_subcategory = subcategory.parent_subcategory
    
    if request.method == 'POST':
        subcategory.title = request.POST.get('title')
        slug = request.POST.get('slug', '').strip()
        subcategory.slug = slug if slug else slugify(subcategory.title)
        subcategory.description = request.POST.get('description', '')
        subcategory.icon_url = request.POST.get('icon_url', '')
        subcategory.icon_color = request.POST.get('icon_color', '#007bff')
        subcategory.order = request.POST.get('order', 0)
        subcategory.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('icon_image'):
            subcategory.icon_image = request.FILES['icon_image']
        
        subcategory.save()
        
        messages.success(request, f"Subcategory '{subcategory.title}' updated successfully!")
        
        if parent_subcategory:
            return redirect('main_app:admin_distance_education_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_distance_education_subcategories', card_id=parent_card.id)
    
    breadcrumb = subcategory.get_breadcrumb() if hasattr(subcategory, 'get_breadcrumb') else []
    
    context = {
        'form': {'instance': subcategory},
        'subcategory': subcategory,
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'is_edit': True,
    }
    
    return render(request, 'admin/distance_education_subcategory_form.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_subcategory_delete(request, subcategory_id):
    """Delete a subcategory"""
    subcategory = get_object_or_404(DistanceEducationSubCategory, id=subcategory_id)
    parent_card = subcategory.get_root_card()
    parent_subcategory = subcategory.parent_subcategory
    
    if subcategory.children.exists():
        messages.error(request, f"Cannot delete '{subcategory.title}' because it has child subcategories!")
        if parent_subcategory:
            return redirect('main_app:admin_distance_education_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_distance_education_subcategories', card_id=parent_card.id)
    
    title = subcategory.title
    subcategory.delete()
    
    messages.success(request, f"Subcategory '{title}' deleted successfully!")
    
    if parent_subcategory:
        return redirect('main_app:admin_distance_education_nested_subcategories', parent_id=parent_subcategory.id)
    else:
        return redirect('main_app:admin_distance_education_subcategories', card_id=parent_card.id)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_pages_by_subcategory(request, subcategory_id):
    """View content pages for a subcategory"""
    subcategory = get_object_or_404(DistanceEducationSubCategory, pk=subcategory_id)
    pages = subcategory.content_pages.all().order_by('order')
    
    context = {
        'subcategory': subcategory,
        'pages': pages,
        'breadcrumb': subcategory.get_breadcrumb(),
    }
    return render(request, 'admin/distance_education_pages_list.html', context)

@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_page_add(request, subcategory_id):
    """Add content page for subcategory"""
    subcategory = get_object_or_404(DistanceEducationSubCategory, pk=subcategory_id)
    
    if request.method == 'POST':
        form = DistanceEducationPageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.sub_category = subcategory
            page.created_by = request.user
            
            # Auto-generate slug if not provided
            if not page.slug:
                from django.utils.text import slugify
                page.slug = slugify(page.title)
            
            page.save()
            messages.success(request, 'Page added successfully!')
            return redirect('main_app:admin_distance_education_pages_by_subcategory', subcategory_id=subcategory_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DistanceEducationPageForm()
    
    context = {
        'form': form,
        'subcategory': subcategory,
    }
    return render(request, 'admin/distance_education_page_form.html', context)


# ==================== STUDENT: FRONTEND VIEWS ====================



# views.py mein distance_education_card_detail UPDATE karo
# views.py mein distance_education_card_detail UPDATE karo
@never_cache
@login_required(login_url='main_app:user_login')
def distance_education_card_detail(request, card_slug):
    """Student: Display main card with FILTERED subcategories"""
    card = get_object_or_404(DistanceEducationCard, slug=card_slug, is_active=True)
    
    # ✅ STEP 1: Get logged-in user's STATE and COURSE
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
        user_state = user_registration.state
        user_course = user_registration.course
    except UserRegistration.DoesNotExist:
        user_state = None
        user_course = None
    
    # ✅ STEP 2: Get TOP-LEVEL subcategories with FILTERING
    subcategories = card.sub_categories.filter(
        is_active=True, 
        parent_subcategory__isnull=True
    )
    
    # ✅ FILTER BY STUDENT STATE
    if user_state:
        from django.db.models import Q
        subcategories = subcategories.filter(
            Q(student_state=user_state) | Q(student_state__isnull=True)
        )
    else:
        subcategories = subcategories.filter(student_state__isnull=True)
    
    # ✅ FILTER BY COURSE
    if user_course:
        from django.db.models import Q
        subcategories = subcategories.filter(
            Q(course=user_course) | Q(course__isnull=True) | Q(course='')
        )
    else:
        subcategories = subcategories.filter(
            Q(course__isnull=True) | Q(course='')
        )
    
    subcategories = subcategories.order_by('order')
    
    # ✅ Get unique target countries for filter dropdown
    unique_countries = subcategories.exclude(
        target_country__isnull=True
    ).values_list('target_country__name', flat=True).distinct().order_by('target_country__name')
    
    # ✅ DEBUG: Print karo
    print(f"Card: {card.title}")
    print(f"User State: {user_state}")
    print(f"User Course: {user_course}")
    print(f"Filtered Subcategories: {subcategories.count()}")
    print(f"Unique Countries: {list(unique_countries)}")
    
    # ✅ STEP 3: Pass to template
    context = {
        'card': card,
        'subcategories': subcategories,
        'user_state': user_state,
        'user_course': user_course,
        'total_filtered': subcategories.count(),
        'unique_countries': unique_countries,  # ✅ NEW
    }
    
    return render(request, 'student/distance_education_card_detail.html', context)


@never_cache
@login_required(login_url='main_app:user_login')
def distance_education_subcategory_detail(request, card_slug, subcategory_path):
    """Student: Display subcategory with children or pages"""
    card = get_object_or_404(DistanceEducationCard, slug=card_slug, is_active=True)
    
    path_parts = subcategory_path.strip('/').split('/')
    
    current_subcategory = None
    for slug in path_parts:
        if current_subcategory is None:
            current_subcategory = get_object_or_404(
                DistanceEducationSubCategory,
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            current_subcategory = get_object_or_404(
                DistanceEducationSubCategory,
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
    
    children = current_subcategory.get_children()
    pages = current_subcategory.content_pages.filter(is_active=True).order_by('order')
    current_path = subcategory_path.rstrip('/')
    
    context = {
        'card': card,
        'subcategory': current_subcategory,
        'children': children,
        'pages': pages,
        'current_path': current_path,
        'breadcrumb': current_subcategory.get_breadcrumb(),
    }
    
    return render(request, 'student/distance_education_subcategory_detail.html', context)


@never_cache
@login_required(login_url='main_app:user_login')
def distance_education_page_detail(request, card_slug, subcategory_path, page_slug):
    """Student: Display full page content"""
    card = get_object_or_404(DistanceEducationCard, slug=card_slug, is_active=True)
    
    path_parts = subcategory_path.strip('/').split('/')
    current_slug = path_parts[-1]
    
    subcategory = get_object_or_404(
        DistanceEducationSubCategory,
        slug=current_slug,
        is_active=True
    )
    
    page = get_object_or_404(
        DistanceEducationPage,
        sub_category=subcategory,
        slug=page_slug,
        is_active=True
    )
    
    page.increment_views()
    
    related_pages = subcategory.content_pages.filter(
        is_active=True
    ).exclude(id=page.id).order_by('order')[:5]
    
    context = {
        'card': card,
        'subcategory': subcategory,
        'page': page,
        'related_pages': related_pages,
        'breadcrumb': subcategory.get_breadcrumb(),
    }
    
    return render(request, 'student/distance_education_page_detail.html', context)



# ==================== ONLINE EDUCATION - NESTED STRUCTURE ====================

from .models import OnlineEducationCard, OnlineEducationSubCategory, OnlineEducationPage
from .forms import OnlineEducationSubCategoryForm, OnlineEducationPageForm
from django.db.models import Count

# ==================== ADMIN: SUBCATEGORIES BY CARD ====================
@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_subcategories(request, card_id):
    """List all TOP-LEVEL subcategories under a specific card"""
    card = get_object_or_404(OnlineEducationCard, id=card_id)
    
    subcategories = OnlineEducationSubCategory.objects.filter(
        parent_card=card,
        parent_subcategory__isnull=True
    ).annotate(
        children_count=Count('children')
    ).order_by('order', 'title')
    
    context = {
        'card': card,
        'subcategories': subcategories,
    }
    
    return render(request, 'admin/online_education_subcategories.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_nested_subcategories(request, parent_id):
    """List all child subcategories under a parent subcategory"""
    parent = get_object_or_404(OnlineEducationSubCategory, id=parent_id)
    
    subcategories = OnlineEducationSubCategory.objects.filter(
        parent_subcategory=parent
    ).annotate(
        children_count=Count('children')
    ).order_by('order', 'title')
    
    breadcrumb = parent.get_breadcrumb() if hasattr(parent, 'get_breadcrumb') else []
    
    context = {
        'parent': parent,
        'subcategories': subcategories,
        'breadcrumb': breadcrumb,
    }
    
    return render(request, 'admin/online_education_nested_subcategories.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_nested_subcategory_add(request, parent_id):
    """Add a new subcategory under either a Card or another Subcategory"""
    parent_card = None
    parent_subcategory = None
    
    # Check if it's a subcategory
    try:
        parent_subcategory = OnlineEducationSubCategory.objects.get(id=parent_id)
        parent_card = parent_subcategory.get_root_card()
    except OnlineEducationSubCategory.DoesNotExist:
        # If not a subcategory, then it must be a card
        try:
            parent_card = OnlineEducationCard.objects.get(id=parent_id)
        except OnlineEducationCard.DoesNotExist:
            messages.error(request, "Invalid parent ID")
            return redirect('main_app:admin_online_education_cards_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug', '').strip()
        description = request.POST.get('description', '')
        
        # ✅ NEW: Get Country, State & Course
        target_country_id = request.POST.get('target_country')
        student_state_id = request.POST.get('student_state')
        course = request.POST.get('course')
        
        icon_image = request.FILES.get('icon_image')
        icon_url = request.POST.get('icon_url', '')
        icon_color = request.POST.get('icon_color', '#007bff')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # Auto-generate slug if empty
        if not slug:
            from django.utils.text import slugify
            slug = slugify(title)
        
        # ✅ Handle Country & State
        target_country = None
        student_state = None
        
        if target_country_id:
            try:
                target_country = Country.objects.get(pk=target_country_id)
            except Country.DoesNotExist:
                pass
        
        if student_state_id:
            try:
                student_state = State.objects.get(pk=student_state_id)
            except State.DoesNotExist:
                pass
        
        # Create subcategory
        new_subcategory = OnlineEducationSubCategory.objects.create(
            parent_card=parent_card if not parent_subcategory else None,
            parent_subcategory=parent_subcategory,
            title=title,
            slug=slug,
            description=description,
            target_country=target_country,  # ✅ NEW
            student_state=student_state,    # ✅ NEW
            course=course if course else None,  # ✅ NEW
            icon_image=icon_image,
            icon_url=icon_url,
            icon_color=icon_color,
            order=order or 0,
            is_active=is_active,
            created_by=request.user
        )
        
        messages.success(request, f"✓ Subcategory '{title}' added successfully!")
        
        # Redirect back
        if parent_subcategory:
            return redirect('main_app:admin_online_education_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_online_education_subcategories', card_id=parent_card.id)
    
    # Build breadcrumb
    breadcrumb = []
    if parent_subcategory:
        breadcrumb = parent_subcategory.get_breadcrumb()
    elif parent_card:
        breadcrumb = [{'id': parent_card.id, 'title': parent_card.title}]
    
    # ✅ Pass Countries, States & Courses to template
    context = {
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'card_id': parent_card.id if parent_card else None,
        'parent_id': parent_subcategory.id if parent_subcategory else None,
        'countries': Country.objects.filter(is_active=True).order_by('name'),  # ✅ NEW
        'states': State.objects.filter(is_active=True).order_by('name'),       # ✅ NEW
        'courses': UserRegistration.COURSE_CHOICES,                            # ✅ NEW
    }
    
    return render(request, 'admin/online_education_subcategory_form.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_subcategory_edit(request, subcategory_id):
    """Edit an existing subcategory"""
    subcategory = get_object_or_404(OnlineEducationSubCategory, id=subcategory_id)
    parent_card = subcategory.get_root_card()
    parent_subcategory = subcategory.parent_subcategory
    
    if request.method == 'POST':
        subcategory.title = request.POST.get('title')
        slug = request.POST.get('slug', '').strip()
        subcategory.slug = slug if slug else slugify(subcategory.title)
        subcategory.description = request.POST.get('description', '')
        subcategory.icon_url = request.POST.get('icon_url', '')
        subcategory.icon_color = request.POST.get('icon_color', '#007bff')
        subcategory.order = request.POST.get('order', 0)
        subcategory.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('icon_image'):
            subcategory.icon_image = request.FILES['icon_image']
        
        subcategory.save()
        
        messages.success(request, f"Subcategory '{subcategory.title}' updated successfully!")
        
        if parent_subcategory:
            return redirect('main_app:admin_online_education_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_online_education_subcategories', card_id=parent_card.id)
    
    breadcrumb = subcategory.get_breadcrumb() if hasattr(subcategory, 'get_breadcrumb') else []
    
    context = {
        'form': {'instance': subcategory},
        'subcategory': subcategory,
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'is_edit': True,
    }
    
    return render(request, 'admin/online_education_subcategory_form.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_subcategory_delete(request, subcategory_id):
    """Delete a subcategory"""
    subcategory = get_object_or_404(OnlineEducationSubCategory, id=subcategory_id)
    parent_card = subcategory.get_root_card()
    parent_subcategory = subcategory.parent_subcategory
    
    if subcategory.children.exists():
        messages.error(request, f"Cannot delete '{subcategory.title}' because it has child subcategories!")
        if parent_subcategory:
            return redirect('main_app:admin_online_education_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_online_education_subcategories', card_id=parent_card.id)
    
    title = subcategory.title
    subcategory.delete()
    
    messages.success(request, f"Subcategory '{title}' deleted successfully!")
    
    if parent_subcategory:
        return redirect('main_app:admin_online_education_nested_subcategories', parent_id=parent_subcategory.id)
    else:
        return redirect('main_app:admin_online_education_subcategories', card_id=parent_card.id)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_pages_by_subcategory(request, subcategory_id):
    """View content pages for a subcategory"""
    subcategory = get_object_or_404(OnlineEducationSubCategory, pk=subcategory_id)
    pages = subcategory.content_pages.all().order_by('order')
    
    context = {
        'subcategory': subcategory,
        'pages': pages,
        'breadcrumb': subcategory.get_breadcrumb(),
    }
    return render(request, 'admin/online_education_pages_list.html', context)


@never_cache
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_page_add(request, subcategory_id):
    """Add content page for subcategory"""
    subcategory = get_object_or_404(OnlineEducationSubCategory, pk=subcategory_id)
    
    if request.method == 'POST':
        form = OnlineEducationPageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.sub_category = subcategory
            page.created_by = request.user
            
            # Auto-generate slug if not provided
            if not page.slug:
                from django.utils.text import slugify
                page.slug = slugify(page.title)
            
            page.save()
            messages.success(request, 'Page added successfully!')
            return redirect('main_app:admin_online_education_pages_by_subcategory', subcategory_id=subcategory_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OnlineEducationPageForm()
    
    context = {
        'form': form,
        'subcategory': subcategory,
    }
    return render(request, 'admin/online_education_page_form.html', context)


# ==================== STUDENT: FRONTEND VIEWS ====================


from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@never_cache
@login_required(login_url='main_app:user_login')
def online_education_card_detail(request, card_slug):
    """
    Student: Display main card with its subcategories
    ✅ FILTERED by user's Country, State & Course
    """
    
    # Get the card
    card = get_object_or_404(OnlineEducationCard, slug=card_slug, is_active=True)
    
    # ✅ Get student's registration info
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
        user_country = user_registration.country
        user_state = user_registration.state
        user_course = user_registration.course
    except UserRegistration.DoesNotExist:
        # If no registration found, show all subcategories
        user_country = None
        user_state = None
        user_course = None
    
    # ✅ BUILD SMART FILTER QUERY
    # Base filter: Only active, top-level subcategories under this card
    filter_query = Q(
        parent_card=card,
        parent_subcategory__isnull=True,
        is_active=True
    )
    
    # ✅ Country Filter
    # Show if: No country set (available to all) OR matches user's country
    if user_country:
        filter_query &= (Q(target_country__isnull=True) | Q(target_country=user_country))
    
    # ✅ State Filter
    # Show if: No state set (available to all) OR matches user's state
    if user_state:
        filter_query &= (Q(student_state__isnull=True) | Q(student_state=user_state))
    
    # ✅ Course Filter
    # Show if: No course set (available to all) OR matches user's course
    if user_course:
        filter_query &= (Q(course__isnull=True) | Q(course='') | Q(course=user_course))
    
    # Get filtered subcategories
    subcategories = OnlineEducationSubCategory.objects.filter(filter_query).order_by('order')
    
    context = {
        'card': card,
        'subcategories': subcategories,
        'user_country': user_country,
        'user_state': user_state,
        'user_course': user_course,
        # ✅ Add debug info (optional - remove in production)
        'total_subcategories': card.sub_categories.filter(
            is_active=True, 
            parent_subcategory__isnull=True
        ).count(),
        'filtered_count': subcategories.count(),
    }
    
    return render(request, 'student/online_education_card_detail.html', context)


@never_cache
@login_required(login_url='main_app:user_login')
def online_education_subcategory_detail(request, card_slug, subcategory_path):
    """Student: Display subcategory with children or pages"""
    card = get_object_or_404(OnlineEducationCard, slug=card_slug, is_active=True)
    
    path_parts = subcategory_path.strip('/').split('/')
    
    current_subcategory = None
    for slug in path_parts:
        if current_subcategory is None:
            current_subcategory = get_object_or_404(
                OnlineEducationSubCategory,
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            current_subcategory = get_object_or_404(
                OnlineEducationSubCategory,
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
    
    children = current_subcategory.get_children()
    pages = current_subcategory.content_pages.filter(is_active=True).order_by('order')
    current_path = subcategory_path.rstrip('/')
    
    context = {
        'card': card,
        'subcategory': current_subcategory,
        'children': children,
        'pages': pages,
        'current_path': current_path,
        'breadcrumb': current_subcategory.get_breadcrumb(),
    }
    
    return render(request, 'student/online_education_subcategory_detail.html', context)


@never_cache
@login_required(login_url='main_app:user_login')
def online_education_page_detail(request, card_slug, subcategory_path, page_slug):
    """Student: Display full page content"""
    card = get_object_or_404(OnlineEducationCard, slug=card_slug, is_active=True)
    
    path_parts = subcategory_path.strip('/').split('/')
    current_slug = path_parts[-1]
    
    subcategory = get_object_or_404(
        OnlineEducationSubCategory,
        slug=current_slug,
        is_active=True
    )
    
    page = get_object_or_404(
        OnlineEducationPage,
        sub_category=subcategory,
        slug=page_slug,
        is_active=True
    )
    
    page.increment_views()
    
    related_pages = subcategory.content_pages.filter(
        is_active=True
    ).exclude(id=page.id).order_by('order')[:5]
    
    context = {
        'card': card,
        'subcategory': subcategory,
        'page': page,
        'related_pages': related_pages,
        'breadcrumb': subcategory.get_breadcrumb(),
    }
    
    return render(request, 'student/online_education_page_detail.html', context)



  


#
# views.py - Management Quota Views

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import (
    ManagementQuotaCollege, ManagementQuotaApplication,
    ManagementQuotaNotification, ManagementQuotaSeatAllocation,
    UserRegistration, College
)

# Admin check function
def is_admin(user):
    return user.is_staff or user.is_superuser


# ==================== STUDENT VIEWS ====================

@login_required
def management_quota_admission(request):
    """Student management quota dashboard"""
    
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
    except UserRegistration.DoesNotExist:
        messages.error(request, 'Please complete your registration first.')
        return redirect('student_registration')
    
    # Get all active management quota colleges
    management_colleges = ManagementQuotaCollege.objects.filter(
        is_active=True,
        accepts_applications=True
    ).select_related('college', 'college__state', 'college__country')
    
    # Get student's applications
    applications = ManagementQuotaApplication.objects.filter(
        student=user_registration
    ).select_related('college__college').order_by('-applied_at')
    
    # Handle application submission
    if request.method == 'POST' and 'submit_application' in request.POST:
        college_id = request.POST.get('college_id')
        course_name = request.POST.get('course_name')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', user_registration.whatsapp_mobile)
        tenth_marks = request.POST.get('tenth_marks')
        twelfth_marks = request.POST.get('twelfth_marks')
        exam_score = request.POST.get('exam_score')
        
        # Validate files
        tenth_file = request.FILES.get('tenth_marksheet')
        twelfth_file = request.FILES.get('twelfth_marksheet')
        exam_file = request.FILES.get('exam_scorecard')
        
        if not college_id or not tenth_file or not twelfth_file:
            messages.error(request, 'Please fill all required fields.')
            return redirect('management_quota_admission')
        
        try:
            mq_college = ManagementQuotaCollege.objects.get(id=college_id, is_active=True)
            
            # Check if already applied
            if ManagementQuotaApplication.objects.filter(
                student=user_registration,
                college=mq_college
            ).exists():
                messages.warning(request, 'You have already applied to this college.')
                return redirect('management_quota_admission')
            
            # Create application
            application = ManagementQuotaApplication.objects.create(
                student=user_registration,
                college=mq_college,
                course_name=course_name,
                full_name=full_name,
                email=email,
                phone=phone,
                tenth_marks=float(tenth_marks),
                twelfth_marks=float(twelfth_marks),
                entrance_exam_score=float(exam_score) if exam_score else None,
                tenth_marksheet=tenth_file,
                twelfth_marksheet=twelfth_file,
                exam_scorecard=exam_file if exam_file else None
            )
            
            # Create notification
            ManagementQuotaNotification.objects.create(
                student=user_registration,
                application=application,
                notification_type='submitted',
                title='Application Submitted',
                message=f'Your application for {mq_college.college.name} has been submitted successfully.'
            )
            
            messages.success(request, 'Application submitted successfully!')
            
        except ManagementQuotaCollege.DoesNotExist:
            messages.error(request, 'College not found or not accepting applications.')
        except Exception as e:
            messages.error(request, f'Error submitting application: {str(e)}')
        
        return redirect('main_app:management_quota_admission')
    
    context = {
        'management_colleges': management_colleges,
        'applications': applications,
        'user_registration': user_registration,
    }
    
    return render(request, 'student/management_quota_admission.html', context)


@login_required
def student_notifications(request):
    """Student notifications page"""
    
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
    except UserRegistration.DoesNotExist:
        messages.error(request, 'Please complete your registration first.')
        return redirect('student_registration')
    
    # Get filter from query parameter
    filter_type = request.GET.get('filter', 'all')
    
    # Get all notifications for this student
    notifications = ManagementQuotaNotification.objects.filter(
        student=user_registration
    ).select_related('application__college__college').order_by('-created_at')
    
    # Apply filter
    if filter_type == 'submitted':
        notifications = notifications.filter(notification_type='submitted')
    elif filter_type == 'approved':
        notifications = notifications.filter(notification_type='approved')
    elif filter_type == 'rejected':
        notifications = notifications.filter(notification_type='rejected')
    elif filter_type == 'waitlist':
        notifications = notifications.filter(notification_type='waitlist')
    
    # Mark as read when viewed
    ManagementQuotaNotification.objects.filter(
        student=user_registration,
        is_read=False
    ).update(is_read=True)
    
    # Count statistics
    all_notifs = ManagementQuotaNotification.objects.filter(
        student=user_registration
    )
    
    # Count applications by status
    applications = ManagementQuotaApplication.objects.filter(
        student=user_registration
    )
    
    pending_count = applications.filter(status='pending').count()
    approved_count = applications.filter(status='approved').count()
    rejected_count = applications.filter(status='rejected').count()
    
    context = {
        'notifications': notifications,
        'total_notifications': all_notifs.count(),
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'current_filter': filter_type,
    }
    
    return render(request, 'student/notifications.html', context)


# ==================== ADMIN VIEWS ====================

@user_passes_test(is_admin)
def admin_management_quota_colleges(request):
    """Admin: Manage management quota colleges"""
    
    colleges = ManagementQuotaCollege.objects.select_related('college').all()
    
    if request.method == 'POST' and 'save_college' in request.POST:
        college_id = request.POST.get('college_id')
        
        try:
            college_obj = College.objects.get(id=request.POST.get('college'))
            
            if college_id:
                mq_college = ManagementQuotaCollege.objects.get(id=college_id)
            else:
                if ManagementQuotaCollege.objects.filter(college=college_obj).exists():
                    messages.error(request, 'Management quota entry already exists for this college.')
                    return redirect('admin_management_quota_colleges')
                mq_college = ManagementQuotaCollege(college=college_obj)
            
            mq_college.management_seats_available = int(request.POST.get('management_seats_available'))
            mq_college.courses_offered = request.POST.get('courses_offered')
            mq_college.fee_structure = request.POST.get('fee_structure', '')
            mq_college.eligibility_criteria = request.POST.get('eligibility_criteria', '')
            mq_college.contact_person = request.POST.get('contact_person', '')
            mq_college.contact_email = request.POST.get('contact_email', '')
            mq_college.contact_phone = request.POST.get('contact_phone', '')
            mq_college.is_active = 'is_active' in request.POST
            mq_college.accepts_applications = 'accepts_applications' in request.POST
            mq_college.save()
            
            messages.success(request, 'Management quota college saved successfully!')
            return redirect('admin_management_quota_colleges')
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    if request.method == 'POST' and 'delete_college' in request.POST:
        college_id = request.POST.get('college_id')
        try:
            ManagementQuotaCollege.objects.get(id=college_id).delete()
            messages.success(request, 'Management quota college deleted!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        return redirect('admin_management_quota_colleges')
    
    context = {
        'colleges': colleges,
        'all_colleges': College.objects.all(),
    }
    
    return render(request, 'admin/management_quota_colleges.html', context)


@user_passes_test(is_admin)
def admin_management_quota_applications(request):
    """Admin: List and manage applications"""
    
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    college_filter = request.GET.get('college', '')
    
    applications = ManagementQuotaApplication.objects.select_related(
        'student', 'college', 'reviewed_by'
    ).all()
    
    if search:
        applications = applications.filter(
            Q(student__name__icontains=search) |
            Q(student__email__icontains=search) |
            Q(full_name__icontains=search)
        )
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    if college_filter:
        applications = applications.filter(college_id=college_filter)
    
    total_applications = applications.count()
    pending_count = applications.filter(status='pending').count()
    approved_count = applications.filter(status='approved').count()
    rejected_count = applications.filter(status='rejected').count()
    
    colleges = ManagementQuotaCollege.objects.select_related('college')
    
    context = {
        'applications': applications,
        'colleges': colleges,
        'total_applications': total_applications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    
    return render(request, 'admin/management_quota_applications.html', context)


@user_passes_test(is_admin)
def admin_view_application_detail(request, app_id):
    """Admin: View detailed application"""
    
    application = get_object_or_404(ManagementQuotaApplication, id=app_id)
    
    if request.method == 'POST' and 'update_status' in request.POST:
        status = request.POST.get('status')
        remarks = request.POST.get('remarks', '')
        
        if status in ['approved', 'rejected', 'waitlist']:
            application.mark_as_reviewed(request.user, status, remarks)
            
            notification_types = {
                'approved': ('approved', 'Application Approved'),
                'rejected': ('rejected', 'Application Rejected'),
                'waitlist': ('waitlist', 'Added to Waitlist'),
            }
            
            notif_type, notif_title = notification_types[status]
            ManagementQuotaNotification.objects.create(
                student=application.student,
                application=application,
                notification_type=notif_type,
                title=notif_title,
                message=f'Your application for {application.college.college.name} status: {status}'
            )
            
            messages.success(request, f'Application {status}!')
            return redirect('main_app:admin_management_quota_applications')
    
    context = {
        'application': application,
    }
    
    return render(request, 'admin/management_quota_application_detail.html', context)


@user_passes_test(is_admin)
def admin_management_quota_notifications(request):
    """Admin: View and manage notifications"""
    
    search = request.GET.get('search', '')
    notif_type = request.GET.get('type', '')
    read_filter = request.GET.get('read', '')
    
    notifications = ManagementQuotaNotification.objects.select_related(
        'student', 'application'
    ).all()
    
    if search:
        notifications = notifications.filter(
            Q(student__name__icontains=search) |
            Q(title__icontains=search) |
            Q(message__icontains=search)
        )
    
    if notif_type:
        notifications = notifications.filter(notification_type=notif_type)
    
    if read_filter:
        notifications = notifications.filter(is_read=(read_filter == 'read'))
    
    total = notifications.count()
    unread_count = notifications.filter(is_read=False).count()
    
    # Get approved applications for allocation form
    approved_apps = ManagementQuotaApplication.objects.filter(
        status='approved'
    ).exclude(
        seat_allocation__isnull=False
    ).select_related('student', 'college__college')
    
    # Handle create allocation
    if request.method == 'POST' and 'create_allocation' in request.POST:
        try:
            app_id = request.POST.get('application_id')
            application = ManagementQuotaApplication.objects.get(id=app_id)
            
            if ManagementQuotaSeatAllocation.objects.filter(application=application).exists():
                messages.error(request, 'Seat already allocated for this application.')
                return redirect('admin_management_quota_notifications')
            
            roll_number = request.POST.get('roll_number')
            seat_number = request.POST.get('seat_number')
            allotment_date = request.POST.get('allotment_date')
            
            ManagementQuotaSeatAllocation.objects.create(
                application=application,
                allocation_roll_number=roll_number,
                seat_number=seat_number,
                allotment_date=allotment_date,
                status='allotted'
            )
            
            messages.success(request, 'Seat allocated successfully!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return redirect('admin_management_quota_notifications')
    
    context = {
        'notifications': notifications,
        'total': total,
        'unread_count': unread_count,
        'approved_apps': approved_apps,
    }
    
    return render(request, 'admin/management_quota_notifications.html', context)


@user_passes_test(is_admin)
def admin_management_quota_seat_allocation(request):
    """Admin: Manage seat allocations"""
    
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    allocations = ManagementQuotaSeatAllocation.objects.select_related(
        'application__student', 'application__college'
    ).all()
    
    if search:
        allocations = allocations.filter(
            Q(allocation_roll_number__icontains=search) |
            Q(application__student__name__icontains=search)
        )
    
    if status_filter:
        allocations = allocations.filter(status=status_filter)
    
    context = {
        'allocations': allocations,
    }
    
    return render(request, 'admin/management_quota_seat_allocation.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import StudentCardPurchase

def admin_counselling_india_payments(request):
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    # Base queryset with related data
    payments = StudentCardPurchase.objects.select_related('student', 'card').all()
    
    # Apply status filter
    if status_filter != 'all':
        payments = payments.filter(payment_status=status_filter)
    
    # Apply search filter
    if search_query:
        payments = payments.filter(
            Q(student__name__icontains=search_query) |
            Q(student__email__icontains=search_query) |
            Q(transaction_id__icontains=search_query) |
            Q(card__title__icontains=search_query)
        )
    
    # Payment status counts for dashboard
    stats = {
        'total': StudentCardPurchase.objects.count(),
        'pending': StudentCardPurchase.objects.filter(payment_status='pending').count(),
        'completed': StudentCardPurchase.objects.filter(payment_status='completed').count(),
        'failed': StudentCardPurchase.objects.filter(payment_status='failed').count(),
    }
    
    context = {
        'payments': payments,
        'stats': stats,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'admin/admin_counselling_india_payments.html', context)


def approve_payment(request, payment_id):
    """Approve a pending payment"""
    if request.method == 'POST':
        payment = get_object_or_404(StudentCardPurchase, id=payment_id)
        
        if payment.payment_status == 'pending':
            payment.payment_status = 'completed'
            payment.payment_completed_at = timezone.now()
            payment.save()
            messages.success(request, f"Payment approved for {payment.student.name}")
        else:
            messages.warning(request, "Payment is not in pending status")
    
    return redirect('main_app:admin_counselling_india_payments')


def reject_payment(request, payment_id):
    """Reject a pending payment"""
    if request.method == 'POST':
        payment = get_object_or_404(StudentCardPurchase, id=payment_id)
        
        if payment.payment_status == 'pending':
            payment.payment_status = 'failed'
            payment.save()
            messages.success(request, f"Payment rejected for {payment.student.name}")
        else:
            messages.warning(request, "Payment is not in pending status")
    
    return redirect('main_app:admin_counselling_india_payments')