# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from .models import HomeSectionCard

# @admin.register(HomeSectionCard)
# class HomeSectionCardAdmin(admin.ModelAdmin):
#     list_display = ['title_line1', 'title_line2', 'order', 'is_active', 'created_at']
#     list_filter = ['is_active', 'created_at']
#     search_fields = ['title_line1', 'title_line2']
#     list_editable = ['order', 'is_active']
    
#     fieldsets = (
#         ('Card Content', {
#             'fields': ('title_line1', 'title_line2')
#         }),
#         ('Image Settings', {
#             'fields': ('card_image', 'image_url'),
#             'description': 'Upload image YA paste URL (dono mein se ek use karo)'
#         }),
#         ('Link & Colors', {
#             'fields': ('redirect_link', 'border_color', 'title_color')
#         }),
#         ('Display Settings', {
#             'fields': ('order', 'is_active')
#         }),
#     )
    
#     readonly_fields = ['created_at', 'updated_at', 'created_by']
    
#     def save_model(self, request, obj, form, change):
#         if not change:  # New object
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)

# from django.contrib import admin
# from .models import College, CollegeComparison, Country, State
# # ... other imports

# # ==================== COLLEGE COMPARISON ADMIN (UPDATED) ====================
# @admin.register(CollegeComparison)
# class CollegeComparisonAdmin(admin.ModelAdmin):
#     list_display = ['comparison_title', 'get_colleges_display', 'country', 'state', 'colleges_count', 'status', 'created_by', 'created_at']
#     list_filter = ['country', 'state', 'status', 'created_at']
#     search_fields = ['comparison_title', 'country__name', 'state__name']
#     ordering = ['-created_at']
#     filter_horizontal = ('colleges',)  # Nice UI for ManyToMany selection
    
#     fieldsets = (
#         ('Comparison Info', {
#             'fields': ('comparison_title', 'comparison_summary')
#         }),
#         ('Colleges to Compare', {
#             'fields': ('colleges',),
#             'description': 'Select multiple colleges to compare (minimum 2 required)'
#         }),
#         ('Target Location (Filter)', {
#             'fields': ('country', 'state'),
#             'description': 'Students from this location will see this comparison'
#         }),
#         ('Status', {
#             'fields': ('status',)
#         }),
#     )
    
#     def get_colleges_display(self, obj):
#         """Display colleges in list view"""
#         colleges = obj.colleges.all()
#         if colleges.count() == 0:
#             return "No colleges selected"
#         elif colleges.count() <= 3:
#             return " vs ".join([c.name for c in colleges])
#         else:
#             return f"{colleges.count()} colleges"
#     get_colleges_display.short_description = 'Colleges'
    
#     def save_model(self, request, obj, form, change):
#         if not change:  # New object
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)
    
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         """Filter active colleges only"""
#         if db_field.name == "colleges":
#             kwargs["queryset"] = College.objects.filter(is_active=True).order_by('country', 'state', 'name')
#         return super().formfield_for_manytomany(db_field, request, **kwargs)

# from .models import StateWiseCounsellingUpdate

# # ==================== STATE WISE COUNSELLING UPDATE ADMIN ====================
# @admin.register(StateWiseCounsellingUpdate)
# class StateWiseCounsellingUpdateAdmin(admin.ModelAdmin):
#     list_display = ['title', 'state', 'external_link_short', 'is_new', 'status', 'order', 'created_at']
#     list_filter = ['state', 'status', 'is_new', 'created_at']
#     search_fields = ['title', 'state__name', 'description']
#     ordering = ['state', 'order', '-created_at']
    
#     fieldsets = (
#         ('State & Title', {
#             'fields': ('state', 'title', 'description')
#         }),
#         ('External Link', {
#             'fields': ('external_link',),
#             'description': 'Link to the state counselling website'
#         }),
#         ('Icon/Image', {
#             'fields': ('icon_image', 'icon_url', 'icon_color')
#         }),
#         ('Additional Info', {
#             'fields': ('last_updated', 'is_new')
#         }),
#         ('Display Settings', {
#             'fields': ('order', 'status')
#         }),
#     )
    
#     def external_link_short(self, obj):
#         """Display shortened link"""
#         if len(obj.external_link) > 50:
#             return obj.external_link[:50] + '...'
#         return obj.external_link
#     external_link_short.short_description = 'External Link'
    
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)

# from django.contrib import admin
# from .models import SubCategory, ContentPage

# # ==================== SUB CATEGORY ADMIN ====================
# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ['title', 'parent_card', 'pages_count', 'order', 'is_active', 'created_at']
#     list_filter = ['parent_card', 'is_active', 'created_at']
#     search_fields = ['title', 'description', 'parent_card__title']
#     prepopulated_fields = {'slug': ('title',)}
#     ordering = ['parent_card', 'order']
    
#     fieldsets = (
#         ('Parent Card', {
#             'fields': ('parent_card',)
#         }),
#         ('Sub-Category Info', {
#             'fields': ('title', 'slug', 'description')
#         }),
#         ('Icon/Image', {
#             'fields': ('icon_image', 'icon_url', 'icon_color')
#         }),
#         ('Display Settings', {
#             'fields': ('order', 'is_active')
#         }),
#     )
    
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)


# # ==================== CONTENT PAGE ADMIN ====================
# @admin.register(ContentPage)
# class ContentPageAdmin(admin.ModelAdmin):
#     list_display = ['title', 'sub_category', 'is_featured', 'views_count', 'order', 'is_active', 'created_at']
#     list_filter = ['sub_category__parent_card', 'sub_category', 'is_active', 'is_featured', 'created_at']
#     search_fields = ['title', 'summary', 'content', 'sub_category__title']
#     prepopulated_fields = {'slug': ('title',)}
#     ordering = ['sub_category', 'order', '-created_at']
    
#     fieldsets = (
#         ('Parent Sub-Category', {
#             'fields': ('sub_category',)
#         }),
#         ('Page Info', {
#             'fields': ('title', 'slug', 'summary')
#         }),
#         ('Content', {
#             'fields': ('content',),
#             'description': 'Use HTML for rich formatting'
#         }),
#         ('Featured Image', {
#             'fields': ('featured_image', 'featured_image_url')
#         }),
#         ('SEO', {
#             'fields': ('meta_description', 'meta_keywords'),
#             'classes': ('collapse',)
#         }),
#         ('Display Settings', {
#             'fields': ('order', 'is_active', 'is_featured')
#         }),
#         ('Stats', {
#             'fields': ('views_count',),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)