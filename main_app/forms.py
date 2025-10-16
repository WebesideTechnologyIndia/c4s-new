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


class OnlineEducationSubCategoryForm(forms.ModelForm):
    class Meta:
        model = OnlineEducationSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description', 
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'icon_color': forms.TextInput(attrs={'type': 'color'}),
        }


class OnlineEducationPageForm(forms.ModelForm):
    class Meta:
        model = OnlineEducationPage
        fields = ['title', 'slug', 'summary', 'content', 'featured_image', 
                  'featured_image_url', 'meta_description', 'meta_keywords', 
                  'order', 'is_active', 'is_featured']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10}),
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


# ==================== USER REGISTRATION FORM ====================
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Create Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model = UserRegistration
        fields = ['name', 'father_name', 'mobile', 'whatsapp_mobile', 'email', 
                  'course', 'country', 'state', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'whatsapp_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control', 'id': 'id_country'}),
            'state': forms.Select(attrs={'class': 'form-control', 'id': 'id_state'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.filter(is_active=True)
        self.fields['state'].queryset = State.objects.none()
        
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id, is_active=True)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.states.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match!")
        
        return cleaned_data
    
from django import forms
from .models import SubCategory, ContentPage

# ==================== SUB CATEGORY FORM ====================
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['parent_card', 'title', 'slug', 'description', 'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        
        widgets = {
            'parent_card': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Engineering Colleges'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'engineering-colleges'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'icon_image': forms.FileInput(attrs={'class': 'form-control'}),
            'icon_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/icon.png'}),
            'icon_color': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==================== CONTENT PAGE FORM ====================
class ContentPageForm(forms.ModelForm):
    class Meta:
        model = ContentPage
        fields = ['sub_category', 'title', 'slug', 'summary', 'content', 'featured_image', 
                  'featured_image_url', 'meta_description', 'meta_keywords', 'order', 'is_active', 'is_featured']
        
        widgets = {
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Top 10 Engineering Colleges'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'top-10-engineering-colleges'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'placeholder': 'Full page content (HTML supported)'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SEO description'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'keyword1, keyword2'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# forms.py mein add karo

class AdmissionAbroadSubCategoryForm(forms.ModelForm):
    class Meta:
        model = AdmissionAbroadSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description', 
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        
        widgets = {
            'parent_card': forms.Select(attrs={'class': 'form-control'}),
            'parent_subcategory': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon_image': forms.FileInput(attrs={'class': 'form-control'}),
            'icon_url': forms.URLInput(attrs={'class': 'form-control'}),
            'icon_color': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AdmissionAbroadPageForm(forms.ModelForm):
    class Meta:
        model = AdmissionAbroadPage
        fields = ['sub_category', 'title', 'slug', 'summary', 'content', 
                  'featured_image', 'featured_image_url', 'order', 'is_active', 'is_featured']
        
        widgets = {
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }




# forms.py mein add karo

class AdmissionAbroadSubCategoryForm(forms.ModelForm):
    class Meta:
        model = AdmissionAbroadSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description', 
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        
        widgets = {
            'parent_card': forms.Select(attrs={'class': 'form-control'}),
            'parent_subcategory': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon_image': forms.FileInput(attrs={'class': 'form-control'}),
            'icon_url': forms.URLInput(attrs={'class': 'form-control'}),
            'icon_color': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AdmissionAbroadPageForm(forms.ModelForm):
    class Meta:
        model = AdmissionAbroadPage
        fields = ['sub_category', 'title', 'slug', 'summary', 'content', 
                  'featured_image', 'featured_image_url', 'order', 'is_active', 'is_featured']
        
        widgets = {
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from .models import DistanceEducationSubCategory, DistanceEducationPage

class DistanceEducationSubCategoryForm(forms.ModelForm):
    class Meta:
        model = DistanceEducationSubCategory
        fields = ['parent_card', 'parent_subcategory', 'title', 'slug', 'description', 
                  'icon_image', 'icon_url', 'icon_color', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'icon_color': forms.TextInput(attrs={'type': 'color'}),
        }

class DistanceEducationPageForm(forms.ModelForm):
    class Meta:
        model = DistanceEducationPage
        fields = ['title', 'slug', 'summary', 'content', 'featured_image', 
                  'featured_image_url', 'meta_description', 'meta_keywords', 
                  'order', 'is_active', 'is_featured']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }