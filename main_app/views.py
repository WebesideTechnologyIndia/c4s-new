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


def user_logout_view(request):
    """Universal Logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('main_app:user_login')


# ✅ ALIAS: admin_login aur admin_logout same hain user_login ke
admin_login_view = user_login_view
admin_logout_view = user_logout_view


# ==================== ADMISSION INDIA (LOGIN REQUIRED) ====================

@login_required(login_url='main_app:user_login')
def admission_india_services_view(request):
    """Admission India Services Page - LOGIN REQUIRED (Normal Users)"""
    # Agar admin hai to admin dashboard bhej do
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins can access from admin panel.')
        return redirect('main_app:admin_dashboard')
    
    cards = AdmissionIndiaCard.objects.filter(is_active=True)
    context = {'cards': cards}
    return render(request, 'admission_india_services.html', context)


# ==================== ADMIN LOGIN/LOGOUT ====================


# ==================== ADMIN DASHBOARD ====================

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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_cards_list(request):
    """List all HOME SECTION cards"""
    cards = HomeSectionCard.objects.all()
    context = {'cards': cards}
    return render(request, 'admin/cards_list.html', context)


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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_counselling_cards_list(request):
    """List all COLLEGE COUNSELLING cards"""
    cards = CollegeCounsellingCard.objects.all()
    context = {'cards': cards, 'card_type': 'counselling'}
    return render(request, 'admin/counselling_cards_list.html', context)


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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_career_services_list(request):
    """List all Career Services"""
    services = CareerCounsellingService.objects.all()
    return render(request, 'admin/career_services_list.html', {'services': services})


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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_cards_list(request):
    """List all Admission India cards"""
    cards = AdmissionIndiaCard.objects.all()
    return render(request, 'admin/admission_cards_list.html', {'cards': cards})


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

@login_required(login_url='main_app:user_login')
def all_india_services_view(request):
    """All India State Wise Counselling Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins can access from admin panel.')
        return redirect('main_app:admin_dashboard')
    
    cards = AllIndiaServiceCard.objects.filter(is_active=True)
    context = {'cards': cards}
    return render(request, 'all_india_services.html', context)


# ==================== ADMIN VIEWS ====================

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_all_india_cards_list(request):
    """List all All India Service cards"""
    cards = AllIndiaServiceCard.objects.all()
    return render(request, 'admin/all_india_cards_list.html', {'cards': cards})


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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_pro_counselling_cards_list(request):
    """List all Professional Counselling Cards"""
    cards = ProfessionalCounsellingCard.objects.all()
    return render(request, 'admin/pro_counselling_cards_list.html', {'cards': cards})


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

@login_required(login_url='main_app:user_login')
def distance_education_view(request):
    """Distance Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = DistanceEducationCard.objects.filter(is_active=True)
    return render(request, 'distance_education.html', {'cards': cards})


# ADMIN - Distance Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_cards_list(request):
    cards = DistanceEducationCard.objects.all()
    return render(request, 'admin/distance_education_cards_list.html', {'cards': cards})

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

@login_required(login_url='main_app:user_login')
def online_education_view(request):
    """Online Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = OnlineEducationCard.objects.filter(is_active=True)
    return render(request, 'online_education.html', {'cards': cards})


# ADMIN - Online Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_cards_list(request):
    cards = OnlineEducationCard.objects.all()
    return render(request, 'admin/online_education_cards_list.html', {'cards': cards})

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

@login_required(login_url='main_app:user_login')
def distance_education_view(request):
    """Distance Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = DistanceEducationCard.objects.filter(is_active=True)
    return render(request, 'distance_education.html', {'cards': cards})


# ADMIN - Distance Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_distance_education_cards_list(request):
    cards = DistanceEducationCard.objects.all()
    return render(request, 'admin/distance_education_cards_list.html', {'cards': cards})

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

@login_required(login_url='main_app:user_login')
def online_education_view(request):
    """Online Education Page - LOGIN REQUIRED"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    cards = OnlineEducationCard.objects.filter(is_active=True)
    return render(request, 'online_education.html', {'cards': cards})


# ADMIN - Online Education
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_online_education_cards_list(request):
    cards = OnlineEducationCard.objects.all()
    return render(request, 'admin/online_education_cards_list.html', {'cards': cards})

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


# ==================== USER REGISTRATION ====================
def user_register_view(request):
    """User Registration with Country/State"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('main_app:admin_dashboard')
        return redirect('main_app:admission_india_services')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save registration
            registration = form.save(commit=False)
            registration.password = make_password(form.cleaned_data['password'])
            registration.save()
            
            # Create Django User
            user = User.objects.create_user(
                username=registration.email,
                email=registration.email,
                password=form.cleaned_data['password']
            )
            registration.user = user
            registration.save()
            
            # Auto login
            login(request, user)
            messages.success(request, f'Welcome {registration.name}! Registration successful.')
            return redirect('main_app:admission_india_services')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user/register.html', {'form': form})


# ==================== ADMIN - COUNTRIES ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_countries_list(request):
    countries = Country.objects.all()
    return render(request, 'admin/countries_list.html', {'countries': countries})

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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_country_delete(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    if request.method == 'POST':
        country.delete()
        messages.success(request, 'Country deleted!')
        return redirect('main_app:admin_countries_list')
    return render(request, 'admin/country_delete.html', {'country': country})


# ==================== ADMIN - STATES ====================
@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_states_list(request):
    states = State.objects.all()
    return render(request, 'admin/states_list.html', {'states': states})

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

# ==================== ADMIN: COLLEGES LIST ====================
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


# ==================== ADMIN: ADD COLLEGE ====================
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


# ==================== ADMIN: EDIT COLLEGE ====================
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

# ==================== ADMIN: DELETE COLLEGE ====================
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


# ==================== ADMIN: COMPARISONS LIST ====================
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
# ==================== ADMIN: ADD COMPARISON (UPDATED) ====================
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


# ==================== ADMIN: EDIT COMPARISON (UPDATED) ====================
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


# ==================== STUDENT: VIEW COMPARISON DETAIL (UPDATED) ====================
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


# ==================== ADMIN: DELETE COMPARISON ====================
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

# ==================== ADMIN: STATE COUNSELLING UPDATES LIST ====================
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


# ==================== ADMIN: ADD STATE COUNSELLING UPDATE ====================
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


# ==================== ADMIN: EDIT STATE COUNSELLING UPDATE ====================
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


# ==================== ADMIN: DELETE STATE COUNSELLING UPDATE ====================
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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_categories_list(request):
    """Admin dashboard - All sub-categories list"""
    sub_categories = SubCategory.objects.all().order_by('parent_card', 'order')
    
    context = {
        'sub_categories': sub_categories,
    }
    return render(request, 'admin/sub_categories_list.html', context)


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


@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_category_edit(request, pk):
    """Admin dashboard - Edit sub-category"""
    sub_category = get_object_or_404(SubCategory, pk=pk)
    
    if request.method == 'POST':
        sub_category.parent_card_id = request.POST.get('parent_card')
        sub_category.title = request.POST.get('title')
        sub_category.slug = request.POST.get('slug')
        sub_category.description = request.POST.get('description')
        sub_category.icon_url = request.POST.get('icon_url')
        sub_category.icon_color = request.POST.get('icon_color')
        sub_category.order = request.POST.get('order') or 0
        sub_category.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('icon_image'):
            sub_category.icon_image = request.FILES.get('icon_image')
        
        sub_category.save()
        
        messages.success(request, "Sub-category updated successfully!")
        return redirect('main_app:admin_sub_categories_list')
    
    parent_cards = AllIndiaServiceCard.objects.filter(is_active=True).order_by('title')
    
    context = {
        'sub_category': sub_category,
        'parent_cards': parent_cards,
    }
    return render(request, 'admin/sub_category_edit.html', context)


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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_pages_list(request):
    """Admin dashboard - All content pages list"""
    pages = ContentPage.objects.all().select_related('sub_category__parent_card').order_by('sub_category', 'order')
    
    context = {
        'pages': pages,
    }
    return render(request, 'admin/content_pages_list.html', context)


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


@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_page_edit(request, pk):
    """Admin dashboard - Edit content page"""
    page = get_object_or_404(ContentPage, pk=pk)
    
    if request.method == 'POST':
        page.sub_category_id = request.POST.get('sub_category')
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
    
    sub_categories = SubCategory.objects.filter(is_active=True).select_related('parent_card').order_by('parent_card', 'title')
    
    context = {
        'page': page,
        'sub_categories': sub_categories,
    }
    return render(request, 'admin/content_page_edit.html', context)


@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_page_delete(request, pk):
    """Admin dashboard - Delete content page"""
    page = get_object_or_404(ContentPage, pk=pk)
    title = page.title
    page.delete()
    
    messages.success(request, f"Page '{title}' deleted successfully!")
    return redirect('main_app:admin_content_pages_list')


# ==================== ADMIN: SUB-CATEGORIES BY CARD ====================
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


@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_sub_category_add_for_card(request, card_id):
    """Admin dashboard - Add sub-category for specific card"""
    parent_card = get_object_or_404(AllIndiaServiceCard, pk=card_id)
    
    if request.method == 'POST':
        # Same as admin_sub_category_add but parent_card is pre-selected
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        icon_url = request.POST.get('icon_url')
        icon_color = request.POST.get('icon_color')
        order = request.POST.get('order') or 0
        is_active = request.POST.get('is_active') == 'on'
        
        icon_image = request.FILES.get('icon_image')
        
        try:
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
            return redirect('main_app:admin_sub_categories_by_card', card_id=card_id)
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    context = {
        'parent_card': parent_card,
    }
    return render(request, 'admin/sub_category_add.html', context)


# ==================== ADMIN: CONTENT PAGES BY SUB-CATEGORY ====================
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


@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_content_page_add_for_subcategory(request, subcategory_id):
    """Admin dashboard - Add page for specific sub-category"""
    sub_category = get_object_or_404(SubCategory, pk=subcategory_id)
    
    if request.method == 'POST':
        # Same as admin_content_page_add but sub_category is pre-selected
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
            return redirect('main_app:admin_content_pages_by_subcategory', subcategory_id=subcategory_id)
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    context = {
        'sub_category': sub_category,
    }

    return render(request, 'admin/content_page_add.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AllIndiaServiceCard, SubCategory, ContentPage

# ==================== STUDENT: CARD DETAIL (SUB-CATEGORIES LIST) ====================
@login_required(login_url='main_app:user_login')
def card_detail_view(request, card_slug):
    """
    Student side - Show sub-categories for a card
    URL: /all-india-services/rti/
    """
    # Check if admin
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admins should use admin panel.')
        return redirect('main_app:admin_dashboard')
    
    # Get card by slug or redirect_link
    card = get_object_or_404(AllIndiaServiceCard, 
                            redirect_link__icontains=card_slug, 
                            is_active=True)
    
    # Get all active sub-categories for this card
    sub_categories = SubCategory.objects.filter(
        parent_card=card, 
        is_active=True
    ).order_by('order')
    
    context = {
        'card': card,
        'sub_categories': sub_categories,
    }
    return render(request, 'student/card_detail.html', context)


# ==================== STUDENT: SUB-CATEGORY DETAIL (PAGES LIST) ====================
@login_required(login_url='main_app:user_login')
def subcategory_detail_view(request, card_slug, subcategory_path):
    """
    Shows:
    - Child subcategories (if exist) OR
    - Pages (if no children)
    """
    
    # Get card
    card = get_object_or_404(AllIndiaServiceCard, 
                            redirect_link__icontains=card_slug, 
                            is_active=True)
    
    # Parse path: "engineering/government/delhi"
    slugs = subcategory_path.strip('/').split('/')
    current_slug = slugs[-1]  # Last slug
    
    # Get current subcategory
    sub_category = get_object_or_404(SubCategory, 
                                     slug=current_slug, 
                                     is_active=True)
    
    # Check: Does it have child subcategories?
    children = sub_category.children.filter(is_active=True).order_by('order')
    
    if children.exists():
        # ✅ Show child subcategories
        context = {
            'card': card,
            'sub_category': sub_category,
            'sub_categories': children,  # Child subcategories
            'breadcrumb': sub_category.get_breadcrumb(),
        }
        return render(request, 'student/card_detail.html', context)  # Reuse same template
    else:
        # ✅ Show pages (no more children)
        pages = ContentPage.objects.filter(
            sub_category=sub_category, 
            is_active=True
        ).order_by('order')
        
        context = {
            'card': card,
            'sub_category': sub_category,
            'pages': pages,
            'breadcrumb': sub_category.get_breadcrumb(),
        }
        return render(request, 'student/subcategory_detail.html', context)
    

# ==================== STUDENT: PAGE DETAIL (FULL CONTENT) ====================
@login_required(login_url='main_app:user_login')
def page_detail_view(request, card_slug, subcategory_slug, page_slug):



    """
    Student side - Show full page content
    URL: /all-india-services/rti/documents/how-to-file-rti/
    """
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main_app:admin_dashboard')
    
    # Get card, sub-category, and page
    card = get_object_or_404(AllIndiaServiceCard, 
                            redirect_link__icontains=card_slug, 
                            is_active=True)
    
    sub_category = get_object_or_404(SubCategory, 
                                     parent_card=card,
                                     slug=subcategory_slug, 
                                     is_active=True)
    
    page = get_object_or_404(ContentPage, 
                            sub_category=sub_category,
                            slug=page_slug, 
                            is_active=True)
    
    # Increment view count
    page.increment_views()
    
    # Get related pages (same sub-category)
    related_pages = ContentPage.objects.filter(
        sub_category=sub_category,
        is_active=True
    ).exclude(id=page.id).order_by('order')[:5]
    
    context = {
        'card': card,
        'sub_category': sub_category,
        'page': page,
        'related_pages': related_pages,
    }
    return render(request, 'student/page_detail.html', context)



# views.py mein YE VIEWS ADD KARO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import AllIndiaServiceCard, SubCategory, ContentPage

# Helper function (if not already present)
def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


# ==================== NESTED SUBCATEGORIES VIEW ====================
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


# ==================== ADD NESTED SUBCATEGORY ====================
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
# Update your existing admin_sub_categories_by_card view
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


# ==================== STUDENT VIEWS (UPDATED) ====================
@login_required(login_url='main_app:user_login')
def subcategory_detail_view(request, card_slug, subcategory_path):
    """
    Student side - Navigate through nested subcategories
    URL examples:
    - /rti/engineering/
    - /rti/engineering/government/
    - /rti/engineering/government/delhi/
    """
    # Get card
    card = get_object_or_404(AllIndiaServiceCard, 
                            redirect_link__icontains=card_slug, 
                            is_active=True)
    
    # Parse nested path
    slugs = subcategory_path.strip('/').split('/')
    
    # Navigate through the path to find current subcategory
    current_subcategory = None
    for slug in slugs:
        if current_subcategory is None:
            # First level - find under card
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_card=card,
                parent_subcategory__isnull=True,
                is_active=True
            )
        else:
            # Nested level - find under parent
            current_subcategory = get_object_or_404(
                SubCategory,
                slug=slug,
                parent_subcategory=current_subcategory,
                is_active=True
            )
    
    # Check if has children
    children = current_subcategory.get_children()
    
    # ✅ SAHI - Related name use kar: content_pages
    pages = current_subcategory.content_pages.filter(is_active=True).order_by('order')
    
    if children.exists():
        # Show child subcategories AND pages both
        context = {
            'card': card,
            'sub_category': current_subcategory,
            'sub_categories': children,
            'pages': pages,  # ✅ Dono dikhengi - subcategories aur pages
            'breadcrumb': current_subcategory.get_breadcrumb(),
        }
        return render(request, 'student/subcategory_children.html', context)
    else:
        # Show pages only (leaf node)
        context = {
            'card': card,
            'sub_category': current_subcategory,
            'pages': pages,
            'breadcrumb': current_subcategory.get_breadcrumb(),
        }
        return render(request, 'student/subcategory_pages.html', context)



# abroad india 


# views.py mein add karo

# Admin - Sub-categories by Card
# Add these views to your views.py (REPLACE the incomplete admission abroad section at the bottom)

from .models import AdmissionAbroadCard, AdmissionAbroadSubCategory, AdmissionAbroadPage
from .forms import AdmissionAbroadCardForm, AdmissionAbroadSubCategoryForm, AdmissionAbroadPageForm

# ==================== PUBLIC VIEW (LOGIN REQUIRED) ====================

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

@login_required(login_url='main_app:admin_login')
@user_passes_test(is_admin_or_staff, login_url='main_app:user_login')
def admin_admission_abroad_cards_list(request):
    """List all Admission Abroad cards"""
    cards = AdmissionAbroadCard.objects.all().order_by('order')
    return render(request, 'admin/admission_abroad_cards_list.html', {'cards': cards})


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


# ==================== ADMIN: NESTED SUBCATEGORIES ====================
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


# ==================== ADMIN: ADD CONTENT PAGE FOR SUBCATEGORY ====================

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
        form = AdmissionAbroadPageForm()
    
    context = {
        'form': form,
        'subcategory': subcategory,
    }
    return render(request, 'admin/admission_abroad_page_form.html', context)


# ==================== STUDENT: FRONTEND VIEWS ====================

@login_required(login_url='main_app:user_login')
def admission_abroad_card_detail(request, card_slug):
    """Student: Display main card with its subcategories"""
    card = get_object_or_404(AdmissionAbroadCard, 
                            slug=card_slug, 
                            is_active=True)
    
    subcategories = card.sub_categories.filter(
        is_active=True, 
        parent_subcategory__isnull=True
    ).order_by('order')
    
    context = {
        'card': card,
        'subcategories': subcategories,
    }
    return render(request, 'student/admission_abroad_card_detail.html', context)


@login_required(login_url='main_app:user_login')
def admission_abroad_subcategory_detail(request, card_slug, subcategory_path):
    """Student: Display subcategory with children or pages"""
    card = get_object_or_404(AdmissionAbroadCard, slug=card_slug, is_active=True)
    
    # Parse nested path
    path_parts = subcategory_path.strip('/').split('/')
    current_slug = path_parts[-1]
    
    # Get subcategory
    subcategory = get_object_or_404(
        AdmissionAbroadSubCategory,
        slug=current_slug,
        is_active=True
    )
    
    # Check if has children
    children = subcategory.get_children()
    pages = subcategory.content_pages.filter(is_active=True).order_by('order')
    
    context = {
        'card': card,
        'subcategory': subcategory,
        'children': children,
        'pages': pages,
        'breadcrumb': subcategory.get_breadcrumb(),
    }
    
    return render(request, 'student/admission_abroad_subcategory_detail.html', context)


@login_required(login_url='main_app:user_login')
def admission_abroad_page_detail(request, card_slug, subcategory_path, page_slug):
    """Student: Display full page content"""
    card = get_object_or_404(AdmissionAbroadCard, slug=card_slug, is_active=True)
    
    # Get subcategory
    path_parts = subcategory_path.strip('/').split('/')
    current_slug = path_parts[-1]
    
    subcategory = get_object_or_404(
        AdmissionAbroadSubCategory,
        slug=current_slug,
        is_active=True
    )
    
    # Get page
    page = get_object_or_404(
        AdmissionAbroadPage,
        sub_category=subcategory,
        slug=page_slug,
        is_active=True
    )
    
    # Increment views
    page.increment_views()
    
    # Related pages
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


@login_required(login_url='main_app:admin_login')
def admin_admission_abroad_nested_subcategory_add(request, parent_id):
    """
    Add a new subcategory under either a Card or another Subcategory
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
        icon_image = request.FILES.get('icon_image')
        icon_url = request.POST.get('icon_url', '')
        icon_color = request.POST.get('icon_color', '#007bff')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # Auto-generate slug if empty
        if not slug:
            slug = slugify(title)
        
        # Create subcategory
        subcategory = AdmissionAbroadSubCategory.objects.create(
            parent_card=parent_card,
            parent_subcategory=parent_subcategory,
            title=title,
            slug=slug,
            description=description,
            icon_image=icon_image,
            icon_url=icon_url,
            icon_color=icon_color,
            order=order or 0,
            is_active=is_active
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
    
    context = {
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'card_id': parent_card.id if parent_card else None,  # ✅ Added
        'parent_id': parent_subcategory.id if parent_subcategory else None,  # ✅ Added
        'form': {'initial': {  # ✅ Added initial values
            'parent_card': parent_card,
            'parent_subcategory': parent_subcategory,
        }},
    }
    
    return render(request, 'admin/admission_abroad_subcategory_form.html', context)


@login_required(login_url='main_app:admin_login')
def admin_admission_abroad_subcategory_edit(request, subcategory_id):
    """
    Edit an existing subcategory
    """
    subcategory = get_object_or_404(AdmissionAbroadSubCategory, id=subcategory_id)
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
        
        # Handle image upload
        if request.FILES.get('icon_image'):
            subcategory.icon_image = request.FILES['icon_image']
        
        subcategory.save()
        
        messages.success(request, f"Subcategory '{subcategory.title}' updated successfully!")
        
        # Redirect back to appropriate list
        if parent_subcategory:
            return redirect('main_app:admin_admission_abroad_nested_subcategories', parent_id=parent_subcategory.id)
        else:
            return redirect('main_app:admin_admission_abroad_subcategories', card_id=parent_card.id)
    
    # Build breadcrumb
    breadcrumb = subcategory.get_breadcrumb() if hasattr(subcategory, 'get_breadcrumb') else []
    
    context = {
        'form': {'instance': subcategory},
        'subcategory': subcategory,
        'parent_card': parent_card,
        'parent_subcategory': parent_subcategory,
        'breadcrumb': breadcrumb,
        'is_edit': True,
    }
    
    return render(request, 'admin/admission_abroad_subcategory_form.html', context)


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