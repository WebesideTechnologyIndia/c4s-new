from django import forms
from .models import HomeSectionCard, CollegeCounsellingCard

class HomeSectionCardForm(forms.ModelForm):
    """Form for Home Section Cards"""
    
    class Meta:
        model = HomeSectionCard
        fields = ['title_line1', 'title_line2', 'card_image', 'image_url', 
                  'redirect_link', 'border_color', 'title_color', 'order', 'is_active']
        
        widgets = {
            'title_line1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CAREER COUNSELLING'
            }),
            'title_line2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., SERVICES'
            }),
            'card_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://img.icons8.com/...'
            }),
            'redirect_link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/career-counselling/'
            }),
            'border_color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#ff6b35'
            }),
            'title_color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#ff6b35'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class CollegeCounsellingCardForm(forms.ModelForm):
    """Form for College Counselling Cards"""
    
    class Meta:
        model = CollegeCounsellingCard
        fields = ['title', 'description', 'card_image', 'image_url', 
                  'redirect_link', 'border_color', 'order', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Admission India'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short description about this service',
                'rows': 3
            }),
            'card_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.png'
            }),
            'redirect_link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/admission-india/'
            }),
            'border_color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

# forms.py mein YE FORM ADD KARO

from .models import CareerCounsellingService

class CareerCounsellingServiceForm(forms.ModelForm):
    class Meta:
        model = CareerCounsellingService
        fields = ['title', 'description', 'svg_icon', 'redirect_link', 'border_color', 'order', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Career Counselling For 1st To 5th Class'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'svg_icon': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Paste SVG code here'}),
            'redirect_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/career-class-1-5/'}),
            'border_color': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



# forms.py mein YE FORM ADD KARO

from .models import AdmissionIndiaCard

class AdmissionIndiaCardForm(forms.ModelForm):
    """Form for Admission India Cards"""
    
    class Meta:
        model = AdmissionIndiaCard
        fields = ['title', 'feature_1', 'feature_2', 'feature_3', 'feature_4', 
                  'redirect_link', 'border_gradient_start', 'border_gradient_end', 
                  'order', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., ALL INDIA STATE WISE COUNSELLING'
            }),
            'feature_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Feature 1'
            }),
            'feature_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Feature 2'
            }),
            'feature_3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Feature 3'
            }),
            'feature_4': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Feature 4'
            }),
            'redirect_link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/counselling-services-all-india/'
            }),
            'border_gradient_start': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#ED651C'
            }),
            'border_gradient_end': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#F4800C'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


from .models import AllIndiaServiceCard

class AllIndiaServiceCardForm(forms.ModelForm):
    """Form for All India Service Cards"""
    
    class Meta:
        model = AllIndiaServiceCard
        fields = ['title', 'card_image', 'image_url', 'redirect_link', 'category_class', 'order', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., COLLEGE COMPARISON'
            }),
            'card_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/icon.png'
            }),
            'redirect_link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/college-comparison/'
            }),
            'category_class': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

from django import forms
from .models import (
    ProfessionalCounsellingCard,
    StudentDocument,
    ChoiceFilling,
    CounsellingStatus,
    DoubtSession,
    Complaint
)

# ==================== ADMIN FORMS ====================

class ProfessionalCounsellingCardForm(forms.ModelForm):
    """Form for Professional Counselling Cards"""
    
    class Meta:
        model = ProfessionalCounsellingCard
        fields = ['title', 'description', 'card_image', 'image_url', 'section_id', 'border_color', 'order', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Upload Documents for Professional Counselling'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short description',
                'rows': 3
            }),
            'card_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/icon.png'
            }),
            'section_id': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('documents', 'Documents Upload'),
                ('choices', 'Choice Filling'),
                ('status', 'Counselling Status'),
                ('doubts', 'Doubt Sessions'),
                ('complaints', 'Complaint Desk'),
            ]),
            'border_color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# ==================== STUDENT FORMS ====================

class StudentDocumentForm(forms.ModelForm):
    """Form for uploading documents"""
    
    class Meta:
        model = StudentDocument
        fields = ['document_type', 'document_file']
        
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'document_file': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }


class ChoiceFillingForm(forms.ModelForm):
    """Form for choice filling"""
    
    class Meta:
        model = ChoiceFilling
        fields = ['preference_number', 'college_name', 'course_name']
        
        widgets = {
            'preference_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '#',
                'min': '1'
            }),
            'college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter college name'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
        }


class DoubtSessionForm(forms.ModelForm):
    """Form for submitting doubts"""
    
    class Meta:
        model = DoubtSession
        fields = ['subject', 'doubt_description']
        
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),
            'doubt_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your doubt...',
                'rows': 4
            }),
        }


class ComplaintForm(forms.ModelForm):
    """Form for submitting complaints"""
    
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'complaint_subject', 'complaint_description', 'priority']
        
        widgets = {
            'complaint_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint type'
            }),
            'complaint_subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),
            'complaint_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your complaint...',
                'rows': 4
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# ==================== ADMIN RESPONSE FORMS ====================

class DocumentApprovalForm(forms.ModelForm):
    """Form for document approval/rejection"""
    
    class Meta:
        model = StudentDocument
        fields = ['status', 'admin_remarks']
        
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'admin_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Admin remarks (optional)'
            }),
        }


class DoubtResponseForm(forms.ModelForm):
    """Form for responding to doubts"""
    
    class Meta:
        model = DoubtSession
        fields = ['response', 'status']
        
        widgets = {
            'response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your response...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class ComplaintResponseForm(forms.ModelForm):
    """Form for responding to complaints"""
    
    class Meta:
        model = Complaint
        fields = ['admin_response', 'status']
        
        widgets = {
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your response...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class CounsellingStatusForm(forms.ModelForm):
    """Form for updating counselling status"""
    
    class Meta:
        model = CounsellingStatus
        fields = ['application_submitted', 'documents_verified', 'choice_filling_completed', 
                  'seat_allotment_status', 'current_stage']
        
        widgets = {
            'application_submitted': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'documents_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'choice_filling_completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'seat_allotment_status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Seat Allocated - ABC College'
            }),
            'current_stage': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

from .models import *
class AdmissionAbroadCardForm(forms.ModelForm):
    """Form for Admission Abroad Cards"""
    
    class Meta:
        model = AdmissionAbroadCard
        fields = ['title', 'description', 'card_image', 'image_url', 'redirect_link', 'border_color', 'order', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., COUNTRIES NAME'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short description',
                'rows': 3
            }),
            'card_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/icon.png'
            }),
            'redirect_link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/countries/'
            }),
            'border_color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# ==================== DISTANCE EDUCATION FORM ====================
class DistanceEducationCardForm(forms.ModelForm):
    class Meta:
        model = DistanceEducationCard
        fields = ['title', 'slug', 'description', 'card_image', 'image_url', 
                  'border_color', 'redirect_link', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'border_color': forms.TextInput(attrs={'type': 'color'}),
        }


# ==================== ONLINE EDUCATION FORMS ====================
class OnlineEducationCardForm(forms.ModelForm):
    class Meta:
        model = OnlineEducationCard
        fields = ['title', 'slug', 'description', 'card_image', 'image_url', 
                  'redirect_link', 'border_color', 'order', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to auto-generate'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'border_color': forms.TextInput(attrs={'type': 'color'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

# 
# forms.py mein OnlineEducationSubCategoryForm update karo:

from django import forms
from .models import OnlineEducationSubCategory, Country, State, UserRegistration
# 
class OnlineEducationSubCategoryForm(forms.ModelForm):
    COURSE_CHOICES = UserRegistration.COURSE_CHOICES
     
    class Meta:
        model = OnlineEducationSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description',
                  'target_country', 'student_state', 'course',  # ✅ NEW
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'icon_color': forms.TextInput(attrs={'type': 'color'}),
            'target_country': forms.Select(attrs={'class': 'form-control'}),
            'student_state': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set country queryset
        self.fields['target_country'].queryset = Country.objects.filter(is_active=True).order_by('name')
        self.fields['target_country'].required = False
        
        # Set state queryset
        self.fields['student_state'].queryset = State.objects.filter(is_active=True).order_by('name')
        self.fields['student_state'].required = False
#         
#         # Add course choices
        self.fields['course'].widget = forms.Select(
            attrs={'class': 'form-control'},
            choices=[('', 'All Courses')] + list(self.COURSE_CHOICES)
        )
        self.fields['course'].required = False




from ckeditor_uploader.widgets import CKEditorUploadingWidget

class OnlineEducationPageForm(forms.ModelForm):
    class Meta:
        model = OnlineEducationPage
        fields = ['title', 'slug', 'summary', 'content', 'featured_image', 
                  'featured_image_url', 'meta_description', 'meta_keywords', 
                  'order', 'is_active', 'is_featured']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Best Online Courses for Data Science 2025'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'best-online-courses-data-science-2025'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of the page'
            }),
            'content': CKEditorUploadingWidget(),  # CKEditor widget
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO meta description'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'keyword1, keyword2, keyword3'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django import forms
from .models import Country, State, UserRegistration

# ==================== COUNTRY FORM ====================
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'code', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., India'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., IN'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==================== STATE FORM ====================
class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['country', 'name', 'code', 'is_active']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Haryana'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., HR'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


from django import forms
from .models import Country, State, UserRegistration


from django import forms
from .models import Country, State, UserRegistration

from django import forms
from .models import UserRegistration, Country, State

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = UserRegistration
        fields = ['name', 'father_name', 'mobile', 'whatsapp_mobile', 
                  'email', 'course', 'country', 'state', 'city']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter father's name"
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number'
            }),
            'whatsapp_mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter WhatsApp number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'course': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select your course'
            }),
            'country': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_country'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_state'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
        }
    
    def __init__(self, *args, country_filter='all', **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply country filter
        if country_filter == 'india_only':
            self.fields['country'].queryset = Country.objects.filter(name='India')
        elif country_filter == 'exclude_india':
            self.fields['country'].queryset = Country.objects.exclude(name='India')
        else:
            self.fields['country'].queryset = Country.objects.all()
        
        # Initially empty states
        self.fields['state'].queryset = State.objects.none()
        
        # If editing existing data, load states
        if self.instance.pk and self.instance.country:
            self.fields['state'].queryset = State.objects.filter(
                country=self.instance.country
            )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data


from django import forms
from .models import SubCategory, ContentPage

# forms.py mein UPDATE karo

from django import forms
from .models import SubCategory, State, UserRegistration

class SubCategoryForm(forms.ModelForm):
    # Get course choices from UserRegistration model
    COURSE_CHOICES = UserRegistration.COURSE_CHOICES
    
    class Meta:
        model = SubCategory
        fields = ['parent_card', 'title', 'slug', 'description', 'state', 'course',
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        
        widgets = {
            'parent_card': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Engineering Colleges'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'engineering-colleges'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            
            # NEW: State & Course dropdowns
            'state': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            
            'icon_image': forms.FileInput(attrs={'class': 'form-control'}),
            'icon_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/icon.png'}),
            'icon_color': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set state queryset - only active states
        self.fields['state'].queryset = State.objects.filter(is_active=True).order_by('name')
        self.fields['state'].required = False  # Optional field
        
        # Add course choices
        self.fields['course'].widget = forms.Select(
            attrs={'class': 'form-control'},
            choices=[('', 'All Courses')] + list(self.COURSE_CHOICES)
        )
        self.fields['course'].required = False  # Optional field


# ==================== CONTENT PAGE FORM ====================
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import ContentPage, Country, State, UserRegistration

class ContentPageForm(forms.ModelForm):
    # Explicitly define country, state, and course fields
    country = forms.ModelChoiceField(
        queryset=Country.objects.filter(is_active=True),
        required=False,
        empty_label="--- Select Country ---",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_country'})
    )
    
    state = forms.ModelChoiceField(
        queryset=State.objects.none(),  # Will be populated dynamically
        required=False,
        empty_label="--- Select State ---",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_state'})
    )
    
    course = forms.ChoiceField(
        choices=[('', '--- Select Course ---')] + UserRegistration.COURSE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_course'})
    )
    
    class Meta:
        model = ContentPage
        fields = ['sub_category', 'country', 'state', 'course', 'title', 'slug', 'summary', 
                  'content', 'featured_image', 'featured_image_url', 'meta_description', 
                  'meta_keywords', 'order', 'is_active', 'is_featured']
        
        widgets = {
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Top 10 Engineering Colleges'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'top-10-engineering-colleges'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary'}),
            'content': CKEditorUploadingWidget(),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SEO description'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'keyword1, keyword2'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize state queryset based on selected country
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(
                    country_id=country_id, 
                    is_active=True
                ).order_by('name')
            except (ValueError, TypeError):
                self.fields['state'].queryset = State.objects.none()
        elif self.instance.pk and self.instance.country:
            # For edit form
            self.fields['state'].queryset = State.objects.filter(
                country=self.instance.country, 
                is_active=True
            ).order_by('name')
            
#  forms.py mein UPDATE karo

class AdmissionAbroadSubCategoryForm(forms.ModelForm):
    class Meta:
        model = AdmissionAbroadSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description',
                  'target_country', 'student_state', 'course',  # ✅ YE ADD KARO
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        
        widgets = {
            'parent_card': forms.Select(attrs={'class': 'form-control'}),
            'parent_subcategory': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # ✅ NEW FIELDS
            'target_country': forms.Select(attrs={'class': 'form-control'}),
            'student_state': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            
            'icon_image': forms.FileInput(attrs={'class': 'form-control'}),
            'icon_url': forms.URLInput(attrs={'class': 'form-control'}),
            'icon_color': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    # ✅ ADD THIS METHOD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make fields optional
        self.fields['target_country'].required = False
        self.fields['student_state'].required = False
        self.fields['course'].required = False
        self.fields['parent_card'].required = False
        self.fields['parent_subcategory'].required = False
        
        # Filter active countries and states
        self.fields['target_country'].queryset = Country.objects.filter(is_active=True).order_by('name')
        self.fields['student_state'].queryset = State.objects.filter(is_active=True).order_by('name')
        
        # Add "All" option for dropdowns
        self.fields['target_country'].empty_label = "-- All Countries --"
        self.fields['student_state'].empty_label = "-- All States --"
        
        # ✅ Course dropdown with choices from UserRegistration
        course_choices = [('', '-- All Courses --')] + list(UserRegistration.COURSE_CHOICES)
        self.fields['course'] = forms.ChoiceField(
            choices=course_choices,
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )


from ckeditor_uploader.widgets import CKEditorUploadingWidget


from main_app.models import UserRegistration  # Import karo

class AdmissionAbroadPageForm(forms.ModelForm):
    # Course field with choices from UserRegistration
    course = forms.ChoiceField(
        choices=[('', '--- Select Course ---')] + UserRegistration.COURSE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = AdmissionAbroadPage
        fields = ['sub_category', 'country', 'state', 'course', 'title', 'slug', 
                  'summary', 'content', 'featured_image', 'featured_image_url', 
                  'order', 'is_active', 'is_featured']
        
        widgets = {
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control', 'id': 'id_country'}),
            'state': forms.Select(attrs={'class': 'form-control', 'id': 'id_state'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Study in USA - Complete Guide 2025'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'study-in-usa-guide-2025'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary of the page'}),
            'content': CKEditorUploadingWidget(),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Country dropdown - only active countries
        self.fields['country'].queryset = Country.objects.filter(is_active=True)
        self.fields['country'].empty_label = "--- Select Country ---"
        
        # State dropdown - filter by country if country is selected
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(
                    country_id=country_id, is_active=True
                ).order_by('name')
            except (ValueError, TypeError):
                self.fields['state'].queryset = State.objects.none()
        elif self.instance.pk and self.instance.country:
            self.fields['state'].queryset = State.objects.filter(
                country=self.instance.country, is_active=True
            ).order_by('name')
        else:
            self.fields['state'].queryset = State.objects.none()
        
        self.fields['state'].empty_label = "--- Select State ---"


# forms.py mein add karo

# forms.py mein AdmissionAbroadSubCategoryForm UPDATE karo

from django import forms
from .models import AdmissionAbroadSubCategory, Country, State, UserRegistration

class AdmissionAbroadSubCategoryForm(forms.ModelForm):
    # Get course choices from UserRegistration model
    COURSE_CHOICES = UserRegistration.COURSE_CHOICES
    
    class Meta:
        model = AdmissionAbroadSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description',
                  'target_country', 'student_state', 'course',  # ✅ NEW FIELDS
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        
        widgets = {
            'parent_card': forms.Select(attrs={'class': 'form-control'}),
            'parent_subcategory': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Engineering Universities in Russia'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'engineering-russia'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            
            # ✅ NEW: Country, State & Course dropdowns
            'target_country': forms.Select(attrs={'class': 'form-control'}),
            'student_state': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            
            'icon_image': forms.FileInput(attrs={'class': 'form-control'}),
            'icon_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/icon.png'}),
            'icon_color': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set country queryset - only active countries
        self.fields['target_country'].queryset = Country.objects.filter(is_active=True).order_by('name')
        self.fields['target_country'].required = False  # Optional field
        
        # Set state queryset - only active states (student's home state)
        self.fields['student_state'].queryset = State.objects.filter(is_active=True).order_by('name')
        self.fields['student_state'].required = False  # Optional field
        
        # Add course choices
        self.fields['course'].widget = forms.Select(
            attrs={'class': 'form-control'},
            choices=[('', 'All Courses')] + list(self.COURSE_CHOICES)
        )
        self.fields['course'].required = False  # Optional field


from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import AdmissionAbroadPage, Country, State, UserRegistration

class AdmissionAbroadPageForm(forms.ModelForm):
    # Explicitly define fields with proper configuration
    country = forms.ModelChoiceField(
        queryset=Country.objects.filter(is_active=True),
        required=False,
        empty_label="--- Select Country ---",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_country'})
    )
    
    state = forms.ModelChoiceField(
        queryset=State.objects.none(),  # Will be populated dynamically
        required=False,
        empty_label="--- Select State ---",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_state'})
    )
    
    course = forms.ChoiceField(
        choices=[('', '--- Select Course ---')] + UserRegistration.COURSE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_course'})
    )
    
    class Meta:
        model = AdmissionAbroadPage
        fields = ['sub_category', 'country', 'state', 'course', 'title', 'slug', 
                  'summary', 'content', 'featured_image', 'featured_image_url', 
                  'order', 'is_active', 'is_featured']
        
        widgets = {
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Study in USA - Complete Guide 2025'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'study-in-usa-guide-2025'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Brief summary of the page'
            }),
            'content': CKEditorUploadingWidget(),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://example.com/image.jpg'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize state queryset based on selected country
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(
                    country_id=country_id, 
                    is_active=True
                ).order_by('name')
            except (ValueError, TypeError):
                self.fields['state'].queryset = State.objects.none()
        elif self.instance.pk and self.instance.country:
            # For edit form
            self.fields['state'].queryset = State.objects.filter(
                country=self.instance.country, 
                is_active=True
            ).order_by('name')


from .models import DistanceEducationSubCategory, DistanceEducationPage


# forms.py mein DistanceEducationSubCategoryForm UPDATE karo

from django import forms
from .models import DistanceEducationSubCategory, Country, State, UserRegistration

class DistanceEducationSubCategoryForm(forms.ModelForm):
    COURSE_CHOICES = UserRegistration.COURSE_CHOICES
    
    class Meta:
        model = DistanceEducationSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description',
                  'target_country', 'student_state', 'course',  # ✅ NEW
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'icon_color': forms.TextInput(attrs={'type': 'color'}),
            'target_country': forms.Select(attrs={'class': 'form-control'}),
            'student_state': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set country queryset
        self.fields['target_country'].queryset = Country.objects.filter(is_active=True).order_by('name')
        self.fields['target_country'].required = False
        
        # Set state queryset
        self.fields['student_state'].queryset = State.objects.filter(is_active=True).order_by('name')
        self.fields['student_state'].required = False
        
        # Add course choices
        self.fields['course'].widget = forms.Select(
            attrs={'class': 'form-control'},
            choices=[('', 'All Courses')] + list(self.COURSE_CHOICES)
        )
        self.fields['course'].required = False



from ckeditor_uploader.widgets import CKEditorUploadingWidget

class DistanceEducationPageForm(forms.ModelForm):
    class Meta:
        model = DistanceEducationPage
        fields = ['title', 'slug', 'summary', 'content', 'featured_image', 
                  'featured_image_url', 'meta_description', 'meta_keywords', 
                  'order', 'is_active', 'is_featured']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Distance MBA Programs 2025'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'distance-mba-programs-2025'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of the page'
            }),
            'content': CKEditorUploadingWidget(),  # CKEditor widget
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO meta description'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'keyword1, keyword2, keyword3'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }