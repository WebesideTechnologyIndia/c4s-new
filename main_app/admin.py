from django.contrib import admin
from .models import (
    HomeSectionCard, CollegeCounsellingCard, CareerCounsellingService,
    AdmissionIndiaCard, AllIndiaServiceCard, ProfessionalCounsellingCard,
    StudentDocument, ChoiceFilling, CounsellingStatus, DoubtSession, Complaint,
    AdmissionAbroadCard, DistanceEducationCard, DistanceEducationSubCategory,
    DistanceEducationPage, OnlineEducationCard, OnlineEducationSubCategory,
    OnlineEducationPage, Country, State, UserRegistration, College,
    CollegeComparison, StateWiseCounsellingUpdate, SubCategory, ContentPage,
    AdmissionAbroadSubCategory, AdmissionAbroadPage, StudentCardPurchase,
    ManagementQuotaCollege, ManagementQuotaApplication, ManagementQuotaNotification,
    ManagementQuotaSeatAllocation
)


# ==================== HOME SECTION CARDS ====================
@admin.register(HomeSectionCard)
class HomeSectionCardAdmin(admin.ModelAdmin):
    list_display = ['title_line1', 'title_line2', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title_line1', 'title_line2']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'id']
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ==================== COLLEGE COUNSELLING ====================
@admin.register(CollegeCounsellingCard)
class CollegeCounsellingCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'border_color', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'border_color', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'id']


# ==================== CAREER COUNSELLING ====================
@admin.register(CareerCounsellingService)
class CareerCounsellingServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'border_color', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'border_color', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'id']


# ==================== ADMISSION INDIA ====================
@admin.register(AdmissionIndiaCard)
class AdmissionIndiaCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'card_type', 'price', 'order', 'is_active', 'created_at']
    list_filter = ['card_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active', 'card_type']
    ordering = ['order', 'id']


# ==================== ALL INDIA SERVICE ====================
@admin.register(AllIndiaServiceCard)
class AllIndiaServiceCardAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'category_class', 'is_active', 'created_at']
    list_filter = ['is_active', 'category_class', 'created_at']
    search_fields = ['title']
    list_editable = ['is_active']
    ordering = ['order', 'id']
    prepopulated_fields = {'redirect_link': ('title',)}


# ==================== PROFESSIONAL COUNSELLING ====================
@admin.register(ProfessionalCounsellingCard)
class ProfessionalCounsellingCardAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'section_id', 'border_color', 'is_active']
    list_filter = ['is_active', 'border_color', 'section_id']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    list_display_links = ['order', 'title']
    ordering = ['order', 'id']


# ==================== STUDENT DOCUMENTS ====================
@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'document_type', 'status', 'uploaded_at']
    list_filter = ['status', 'document_type', 'uploaded_at']
    search_fields = ['student__username', 'student__email']
    list_editable = ['status']
    readonly_fields = ['uploaded_at', 'updated_at']


# ==================== CHOICE FILLING ====================
@admin.register(ChoiceFilling)
class ChoiceFillingAdmin(admin.ModelAdmin):
    list_display = ['student', 'preference_number', 'college_name', 'course_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['student__username', 'college_name', 'course_name']
    ordering = ['student', 'preference_number']


# ==================== COUNSELLING STATUS ====================
@admin.register(CounsellingStatus)
class CounsellingStatusAdmin(admin.ModelAdmin):
    list_display = ['student', 'current_stage', 'application_submitted', 'documents_verified', 'choice_filling_completed']
    list_filter = ['current_stage', 'application_submitted', 'documents_verified']
    search_fields = ['student__username']
    readonly_fields = ['last_updated']


# ==================== DOUBTS ====================
@admin.register(DoubtSession)
class DoubtSessionAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__username', 'subject', 'doubt_description']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']


# ==================== COMPLAINTS ====================
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['student', 'complaint_subject', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['student__username', 'complaint_subject', 'complaint_description']
    list_editable = ['status', 'priority']
    readonly_fields = ['created_at', 'updated_at']


# ==================== ADMISSION ABROAD ====================
@admin.register(AdmissionAbroadCard)
class AdmissionAbroadCardAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'slug', 'border_color', 'is_active', 'created_at']
    list_filter = ['is_active', 'border_color', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    list_display_links = ['order', 'title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'id']


@admin.register(AdmissionAbroadSubCategory)
class AdmissionAbroadSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_card', 'parent_subcategory', 'target_country', 'student_state', 'course', 'order', 'is_active']
    list_filter = ['is_active', 'target_country', 'student_state', 'course']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'id']


@admin.register(AdmissionAbroadPage)
class AdmissionAbroadPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_category', 'is_active', 'is_featured', 'views_count', 'created_at']
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'summary', 'content']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']


# ==================== DISTANCE EDUCATION ====================
@admin.register(DistanceEducationCard)
class DistanceEducationCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']


@admin.register(DistanceEducationSubCategory)
class DistanceEducationSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_card', 'parent_subcategory', 'target_country', 'student_state', 'course', 'order', 'is_active']
    list_filter = ['is_active', 'target_country', 'student_state', 'course']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']


@admin.register(DistanceEducationPage)
class DistanceEducationPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_category', 'is_active', 'is_featured', 'views_count', 'created_at']
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'summary', 'content']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']


# ==================== ONLINE EDUCATION ====================
@admin.register(OnlineEducationCard)
class OnlineEducationCardAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'slug', 'border_color', 'is_active', 'created_at']
    list_filter = ['is_active', 'border_color', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    list_display_links = ['order', 'title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'id']


@admin.register(OnlineEducationSubCategory)
class OnlineEducationSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_card', 'parent_subcategory', 'target_country', 'student_state', 'course', 'order', 'is_active']
    list_filter = ['is_active', 'target_country', 'student_state', 'course']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']


@admin.register(OnlineEducationPage)
class OnlineEducationPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_category', 'is_active', 'is_featured', 'views_count', 'created_at']
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'summary', 'content']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']


# ==================== COUNTRY & STATE ====================
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    list_editable = ['is_active']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'code', 'is_active', 'created_at']
    list_filter = ['country', 'is_active', 'created_at']
    search_fields = ['name', 'code']
    list_editable = ['is_active']


# ==================== USER REGISTRATION ====================
@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'course', 'country', 'state', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'course', 'country', 'state', 'created_at']
    search_fields = ['name', 'email', 'mobile', 'father_name']
    list_editable = ['is_verified']
    readonly_fields = ['password', 'created_at', 'updated_at']


# ==================== COLLEGE ====================
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'state', 'city', 'ranking', 'tuition_fees', 'is_active']
    list_filter = ['country', 'state', 'is_active', 'created_at']
    search_fields = ['name', 'city', 'courses_offered']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']


# ==================== COLLEGE COMPARISON ====================
@admin.register(CollegeComparison)
class CollegeComparisonAdmin(admin.ModelAdmin):
    list_display = ['comparison_title', 'country', 'state', 'colleges_count', 'status', 'created_at']
    list_filter = ['status', 'country', 'state', 'created_at']
    search_fields = ['comparison_title', 'comparison_summary']
    list_editable = ['status']
    filter_horizontal = ['colleges']
    readonly_fields = ['created_at', 'updated_at']


# ==================== STATE WISE COUNSELLING ====================
@admin.register(StateWiseCounsellingUpdate)
class StateWiseCounsellingUpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'state', 'status', 'is_new', 'order', 'last_updated', 'created_at']
    list_filter = ['status', 'state', 'is_new', 'created_at']
    search_fields = ['title', 'description', 'external_link']
    list_editable = ['order', 'status', 'is_new']
    ordering = ['state', 'order', '-created_at']


# ==================== SUB CATEGORY ====================
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_card', 'parent_subcategory', 'state', 'course', 'order', 'is_active']
    list_filter = ['is_active', 'state', 'course', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'id']


# ==================== CONTENT PAGE ====================
@admin.register(ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_category', 'is_active', 'is_featured', 'views_count', 'created_at']
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'summary', 'content']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']


# ==================== STUDENT CARD PURCHASE ====================
@admin.register(StudentCardPurchase)
class StudentCardPurchaseAdmin(admin.ModelAdmin):
    list_display = ['student', 'card', 'amount', 'payment_status', 'transaction_id', 'purchased_at']
    list_filter = ['payment_status', 'purchased_at']
    search_fields = ['student__name', 'card__title', 'transaction_id']
    list_editable = ['payment_status']
    readonly_fields = ['purchased_at', 'payment_completed_at']


# ==================== MANAGEMENT QUOTA ====================
@admin.register(ManagementQuotaCollege)
class ManagementQuotaCollegeAdmin(admin.ModelAdmin):
    list_display = ['college', 'management_seats_available', 'seats_filled', 'seats_remaining', 'is_active', 'accepts_applications']
    list_filter = ['is_active', 'accepts_applications', 'created_at']
    search_fields = ['college__name', 'contact_person', 'contact_email']
    list_editable = ['is_active', 'accepts_applications']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ManagementQuotaApplication)
class ManagementQuotaApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'college', 'course_name', 'status', 'get_average_marks', 'applied_at']
    list_filter = ['status', 'applied_at', 'reviewed_at']
    search_fields = ['student__name', 'college__college__name', 'course_name', 'full_name', 'email']
    list_editable = ['status']
    readonly_fields = ['applied_at', 'reviewed_at', 'updated_at']
    
    def get_average_marks(self, obj):
        return f"{obj.get_average_marks():.2f}%"
    get_average_marks.short_description = 'Avg Marks'


@admin.register(ManagementQuotaNotification)
class ManagementQuotaNotificationAdmin(admin.ModelAdmin):
    list_display = ['student', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['student__name', 'title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']


@admin.register(ManagementQuotaSeatAllocation)
class ManagementQuotaSeatAllocationAdmin(admin.ModelAdmin):
    list_display = ['allocation_roll_number', 'application', 'seat_number', 'status', 'allotment_date', 'joining_date']
    list_filter = ['status', 'allotment_date', 'joining_date']
    search_fields = ['allocation_roll_number', 'seat_number', 'application__student__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']