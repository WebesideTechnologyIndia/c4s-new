# admin.py mein YE ADD KAR

from django.contrib import admin
from .models import AdmissionIndiaCard, StudentCardPurchase

# ==================== ADMISSION INDIA CARD ADMIN ====================
@admin.register(AdmissionIndiaCard)
class AdmissionIndiaCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'card_type', 'price', 'order', 'is_active', 'created_at')
    list_filter = ('card_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order', 'id')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'card_type', 'price')
        }),
        ('Features', {
            'fields': ('feature_1', 'feature_2', 'feature_3', 'feature_4'),
            'classes': ('collapse',)
        }),
        ('Styling', {
            'fields': ('border_gradient_start', 'border_gradient_end'),
            'classes': ('collapse',)
        }),
        ('Redirect & Display', {
            'fields': ('redirect_link', 'order', 'is_active')
        }),
        ('Meta Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Naya record banate time
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ==================== STUDENT CARD PURCHASE ADMIN ====================
@admin.register(StudentCardPurchase)
class StudentCardPurchaseAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'card_title', 'amount', 'payment_status', 'purchased_at', 'is_purchased_badge')
    list_filter = ('payment_status', 'purchased_at', 'card')
    search_fields = ('student__name', 'student__email', 'card__title', 'transaction_id')
    ordering = ('-purchased_at',)
    readonly_fields = ('purchased_at', 'payment_completed_at', 'transaction_id')
    
    fieldsets = (
        ('Student & Card Info', {
            'fields': ('student', 'card')
        }),
        ('Payment Details', {
            'fields': ('amount', 'payment_status', 'payment_method', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('purchased_at', 'payment_completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Custom columns - readable names
    def student_name(self, obj):
        return f"{obj.student.name} ({obj.student.email})"
    student_name.short_description = "Student"
    
    def card_title(self, obj):
        return obj.card.title
    card_title.short_description = "Card"
    
    def is_purchased_badge(self, obj):
        if obj.is_purchased:
            return "✓ Purchased"
        return "✗ Pending"
    is_purchased_badge.short_description = "Status"
    
    # Make search more efficient
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct
    
    # Prevent manual creation (sirf payment gateway se create hona chahiye)
    def has_add_permission(self, request):
        return False  # Admin manually add nahi kar sakta
    
    # Allow deletion for admin
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser