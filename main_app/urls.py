# urls.py - CORRECT ORDERING (NO DUPLICATES)

from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # ==================== PUBLIC PAGES ====================
    path('', views.home_view, name='home'),
    path('college-admission-counselling-services/', views.college_counselling_view, name='college_counselling'),
    path('career-counselling/', views.career_counselling_view, name='career_counselling'),
    
    # ==================== USER AUTHENTICATION ====================
    path('register/', views.user_register_view, name='user_register'),
    path('login/', views.user_login_view, name='user_login'),
    path('logout/', views.user_logout_view, name='user_logout'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    
    # ==================== PUBLIC VIEWS (LOGIN REQUIRED) ====================
    path('admission-india/', views.admission_india_services_view, name='admission_india_services'),
    path('counselling-services-all-india/', views.all_india_services_view, name='all_india_services'),
    path('professional-counselling-by-experts/', views.student_dashboard_view, name='student_dashboard'),
    path('admission-abroad/', views.admission_abroad_view, name='admission_abroad'),
    path('distance-education/', views.distance_education_view, name='distance_education'),
    path('online-education/', views.online_education_view, name='online_education'),
    path('college-comparision/', views.student_comparisons_list, name='student_comparisons_list'),
    path('college-comparison/<int:pk>/', views.student_comparison_detail, name='student_comparison_detail'),
    path('state-wise-counselling-updates/', views.state_wise_counselling_updates, name='state_wise_counselling_updates'),
    
    # ==================== ADMIN DASHBOARD ====================
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # ==================== ADMIN: HOME CARDS ====================
    path('admin-dashboard/home-cards/', views.admin_cards_list, name='admin_cards_list'),
    path('admin-dashboard/home-cards/add/', views.admin_card_add, name='admin_card_add'),
    path('admin-dashboard/home-cards/edit/<int:card_id>/', views.admin_card_edit, name='admin_card_edit'),
    path('admin-dashboard/home-cards/delete/<int:card_id>/', views.admin_card_delete, name='admin_card_delete'),
    
    # ==================== ADMIN: COUNSELLING CARDS ====================
    path('admin-dashboard/counselling-cards/', views.admin_counselling_cards_list, name='admin_counselling_cards_list'),
    path('admin-dashboard/counselling-cards/add/', views.admin_counselling_card_add, name='admin_counselling_card_add'),
    path('admin-dashboard/counselling-cards/edit/<int:card_id>/', views.admin_counselling_card_edit, name='admin_counselling_card_edit'),
    path('admin-dashboard/counselling-cards/delete/<int:card_id>/', views.admin_counselling_card_delete, name='admin_counselling_card_delete'),
    
    # ==================== ADMIN: CAREER SERVICES ====================
    path('admin-dashboard/career-services/', views.admin_career_services_list, name='admin_career_services_list'),
    path('admin-dashboard/career-services/add/', views.admin_career_service_add, name='admin_career_service_add'),
    path('admin-dashboard/career-services/edit/<int:service_id>/', views.admin_career_service_edit, name='admin_career_service_edit'),
    path('admin-dashboard/career-services/delete/<int:service_id>/', views.admin_career_service_delete, name='admin_career_service_delete'),
    
    # ==================== ADMIN: ADMISSION INDIA CARDS ====================
    path('admin-dashboard/admission-cards/', views.admin_admission_cards_list, name='admin_admission_cards_list'),
    path('admin-dashboard/admission-cards/add/', views.admin_admission_card_add, name='admin_admission_card_add'),
    path('admin-dashboard/admission-cards/edit/<int:card_id>/', views.admin_admission_card_edit, name='admin_admission_card_edit'),
    path('admin-dashboard/admission-cards/delete/<int:card_id>/', views.admin_admission_card_delete, name='admin_admission_card_delete'),
    
    # ==================== ADMIN: ALL INDIA SERVICE CARDS ====================
    path('admin-dashboard/all-india-cards/', views.admin_all_india_cards_list, name='admin_all_india_cards_list'),
    path('admin-dashboard/all-india-cards/add/', views.admin_all_india_card_add, name='admin_all_india_card_add'),
    path('admin-dashboard/all-india-cards/edit/<int:card_id>/', views.admin_all_india_card_edit, name='admin_all_india_card_edit'),
    path('admin-dashboard/all-india-cards/delete/<int:card_id>/', views.admin_all_india_card_delete, name='admin_all_india_card_delete'),
    
    # ==================== ADMIN: PROFESSIONAL COUNSELLING CARDS ====================
    path('admin-dashboard/pro-counselling-cards/', views.admin_pro_counselling_cards_list, name='admin_pro_counselling_cards_list'),
    path('admin-dashboard/pro-counselling-cards/add/', views.admin_pro_counselling_card_add, name='admin_pro_counselling_card_add'),
    path('admin-dashboard/pro-counselling-cards/edit/<int:card_id>/', views.admin_pro_counselling_card_edit, name='admin_pro_counselling_card_edit'),
    path('admin-dashboard/pro-counselling-cards/delete/<int:card_id>/', views.admin_pro_counselling_card_delete, name='admin_pro_counselling_card_delete'),
    
    # ==================== ADMIN: DISTANCE EDUCATION CARDS ====================
    path('admin-dashboard/distance-education-cards/', views.admin_distance_education_cards_list, name='admin_distance_education_cards_list'),
    path('admin-dashboard/distance-education-cards/add/', views.admin_distance_education_card_add, name='admin_distance_education_card_add'),
    path('admin-dashboard/distance-education-cards/edit/<int:card_id>/', views.admin_distance_education_card_edit, name='admin_distance_education_card_edit'),
    path('admin-dashboard/distance-education-cards/delete/<int:card_id>/', views.admin_distance_education_card_delete, name='admin_distance_education_card_delete'),
    
    # ==================== ADMIN: ONLINE EDUCATION CARDS ====================
    path('admin-dashboard/online-education-cards/', views.admin_online_education_cards_list, name='admin_online_education_cards_list'),
    path('admin-dashboard/online-education-cards/add/', views.admin_online_education_card_add, name='admin_online_education_card_add'),
    path('admin-dashboard/online-education-cards/edit/<int:card_id>/', views.admin_online_education_card_edit, name='admin_online_education_card_edit'),
    path('admin-dashboard/online-education-cards/delete/<int:card_id>/', views.admin_online_education_card_delete, name='admin_online_education_card_delete'),
    
    # ==================== ADMIN: ADMISSION ABROAD CARDS ====================
    path('admin-dashboard/admission-abroad-cards/', views.admin_admission_abroad_cards_list, name='admin_admission_abroad_cards_list'),
    path('admin-dashboard/admission-abroad-cards/add/', views.admin_admission_abroad_card_add, name='admin_admission_abroad_card_add'),
    path('admin-dashboard/admission-abroad-cards/edit/<int:card_id>/', views.admin_admission_abroad_card_edit, name='admin_admission_abroad_card_edit'),
    path('admin-dashboard/admission-abroad-cards/delete/<int:card_id>/', views.admin_admission_abroad_card_delete, name='admin_admission_abroad_card_delete'),
    
    # ==================== ADMIN: STUDENTS & DOCUMENTS ====================
    path('admin-dashboard/students/', views.admin_students_list, name='admin_students_list'),
    path('admin-dashboard/students/<int:student_id>/', views.admin_student_detail, name='admin_student_detail'),
    path('admin-dashboard/students/<int:student_id>/update-status/', views.admin_update_status, name='admin_update_status'),
    path('admin-dashboard/documents/', views.admin_documents_list, name='admin_documents_list'),
    path('admin-dashboard/documents/<int:doc_id>/review/', views.admin_document_review, name='admin_document_review'),
    path('admin-dashboard/doubts/', views.admin_doubts_list, name='admin_doubts_list'),
    path('admin-dashboard/doubts/<int:doubt_id>/respond/', views.admin_doubt_respond, name='admin_doubt_respond'),
    path('admin-dashboard/complaints/', views.admin_complaints_list, name='admin_complaints_list'),
    path('admin-dashboard/complaints/<int:complaint_id>/respond/', views.admin_complaint_respond, name='admin_complaint_respond'),
    
    # ==================== ADMIN: COUNTRIES & STATES ====================
    path('admin-dashboard/countries/', views.admin_countries_list, name='admin_countries_list'),
    path('admin-dashboard/countries/add/', views.admin_country_add, name='admin_country_add'),
    path('admin-dashboard/countries/edit/<int:country_id>/', views.admin_country_edit, name='admin_country_edit'),
    path('admin-dashboard/countries/delete/<int:country_id>/', views.admin_country_delete, name='admin_country_delete'),
    path('admin-dashboard/states/', views.admin_states_list, name='admin_states_list'),
    path('admin-dashboard/states/add/', views.admin_state_add, name='admin_state_add'),
    path('admin-dashboard/states/edit/<int:state_id>/', views.admin_state_edit, name='admin_state_edit'),
    path('admin-dashboard/states/delete/<int:state_id>/', views.admin_state_delete, name='admin_state_delete'),
    
    # ==================== ADMIN: COLLEGES ====================
    path('admin/colleges/', views.admin_colleges_list, name='admin_colleges_list'),
    path('admin/colleges/add/', views.admin_college_add, name='admin_college_add'),
    path('admin/colleges/edit/<int:pk>/', views.admin_college_edit, name='admin_college_edit'),
    path('admin/colleges/delete/<int:pk>/', views.admin_college_delete, name='admin_college_delete'),
    
    # ==================== ADMIN: COMPARISONS ====================
    path('admin/comparisons/', views.admin_comparisons_list, name='admin_comparisons_list'),
    path('admin/comparisons/add/', views.admin_comparison_add, name='admin_comparison_add'),
    path('admin/comparisons/edit/<int:pk>/', views.admin_comparison_edit, name='admin_comparison_edit'),
    path('admin/comparisons/delete/<int:pk>/', views.admin_comparison_delete, name='admin_comparison_delete'),
    
    # ==================== ADMIN: STATE COUNSELLING UPDATES ====================
    path('admin/state-counselling-updates/', views.admin_state_counselling_list, name='admin_state_counselling_list'),
    path('admin/state-counselling-updates/add/', views.admin_state_counselling_add, name='admin_state_counselling_add'),
    path('admin/state-counselling-updates/edit/<int:pk>/', views.admin_state_counselling_edit, name='admin_state_counselling_edit'),
    path('admin/state-counselling-updates/delete/<int:pk>/', views.admin_state_counselling_delete, name='admin_state_counselling_delete'),
    
    # ==================== ADMIN: ALL INDIA SUB-CATEGORIES & PAGES ====================
    path('admin/sub-categories/', views.admin_sub_categories_list, name='admin_sub_categories_list'),
    path('admin/sub-categories/add/', views.admin_sub_category_add, name='admin_sub_category_add'),
    path('admin/sub-categories/edit/<int:pk>/', views.admin_sub_category_edit, name='admin_sub_category_edit'),
    path('admin/sub-categories/delete/<int:pk>/', views.admin_sub_category_delete, name='admin_sub_category_delete'),
    path('admin/content-pages/', views.admin_content_pages_list, name='admin_content_pages_list'),
    path('admin/content-pages/add/', views.admin_content_page_add, name='admin_content_page_add'),
    path('admin/content-pages/edit/<int:pk>/', views.admin_content_page_edit, name='admin_content_page_edit'),
    path('admin/content-pages/delete/<int:pk>/', views.admin_content_page_delete, name='admin_content_page_delete'),
    path('admin/all-india-cards/<int:card_id>/sub-categories/', views.admin_sub_categories_by_card, name='admin_sub_categories_by_card'),
    path('admin/all-india-cards/<int:card_id>/sub-categories/add/', views.admin_sub_category_add_for_card, name='admin_sub_category_add_for_card'),
    path('admin/sub-categories/<int:subcategory_id>/pages/', views.admin_content_pages_by_subcategory, name='admin_content_pages_by_subcategory'),
    path('admin/sub-categories/<int:subcategory_id>/pages/add/', views.admin_content_page_add_for_subcategory, name='admin_content_page_add_for_subcategory'),
    path('admin/subcategory/<int:parent_subcategory_id>/children/', views.admin_nested_subcategories, name='admin_nested_subcategories'),
    path('admin/subcategory/<int:parent_subcategory_id>/add-child/', views.admin_nested_subcategory_add, name='admin_nested_subcategory_add'),
    
    # ==================== ADMIN: ADMISSION ABROAD SUB-CATEGORIES & PAGES ====================
    path('admin/admission-abroad/<int:card_id>/subcategories/', views.admin_admission_abroad_subcategories, name='admin_admission_abroad_subcategories'),
    path('admin/admission-abroad/subcategory/<int:parent_id>/children/', views.admin_admission_abroad_nested_subcategories, name='admin_admission_abroad_nested_subcategories'),
    path('admin/admission-abroad/subcategory/<int:parent_id>/add/', views.admin_admission_abroad_nested_subcategory_add, name='admin_admission_abroad_nested_subcategory_add'),
    path('admin/admission-abroad/subcategory/<int:subcategory_id>/edit/', views.admin_admission_abroad_subcategory_edit, name='admin_admission_abroad_subcategory_edit'),
    path('admin/admission-abroad/subcategory/<int:subcategory_id>/delete/', views.admin_admission_abroad_subcategory_delete, name='admin_admission_abroad_subcategory_delete'),
    path('admin/admission-abroad/subcategory/<int:subcategory_id>/pages/', views.admin_admission_abroad_pages_by_subcategory, name='admin_admission_abroad_pages_by_subcategory'),
    path('admin/admission-abroad/subcategory/<int:subcategory_id>/pages/add/', views.admin_admission_abroad_page_add, name='admin_admission_abroad_page_add'),
    
    # ==================== AJAX ====================
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    
    # ==================== STUDENT: ADMISSION ABROAD NAVIGATION (SPECIFIC URLS FIRST) ====================
    path('admission-abroad/<str:card_slug>/', views.admission_abroad_card_detail, name='admission_abroad_card_detail'),
    path('admission-abroad/<str:card_slug>/<path:subcategory_path>/', views.admission_abroad_subcategory_detail, name='admission_abroad_subcategory_detail'),
    path('admission-abroad/<str:card_slug>/<path:subcategory_path>/<str:page_slug>/', views.admission_abroad_page_detail, name='admission_abroad_page_detail'),
    
    # ==================== STUDENT: ALL INDIA SERVICES NAVIGATION (CATCH-ALL - MUST BE LAST) ====================
    path('<str:card_slug>/', views.card_detail_view, name='card_detail_view'),
    path('<str:card_slug>/<path:subcategory_path>/', views.subcategory_detail_view, name='subcategory_detail_view'),
    path('<str:card_slug>/<path:subcategory_path>/<str:page_slug>/', views.page_detail_view, name='page_detail_view'),
]