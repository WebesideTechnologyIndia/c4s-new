from django.db import models
from django.contrib.auth.models import User

class HomeSectionCard(models.Model):
    """Model for managing home page service cards"""
    
    # Card Content
    title_line1 = models.CharField(max_length=100, help_text="First line (REQUIRED - e.g., CAREER COUNSELLING)")
    title_line2 = models.CharField(max_length=100, blank=True, help_text="Second line (OPTIONAL - e.g., SERVICES)")
    
    # Image - Admin can upload ya URL paste kar sakta hai
    card_image = models.ImageField(upload_to='home_cards/', blank=True, null=True, help_text="Upload image")
    image_url = models.URLField(max_length=500, blank=True, help_text="OR paste image URL (Icons8, etc)")
    
    # Link/Redirect
    redirect_link = models.CharField(max_length=500, blank=True, help_text="Card click pe kaha redirect ho?")
    
    # Styling
    border_color = models.CharField(max_length=7, default="#ff6b35", help_text="Border color (hex code)")
    title_color = models.CharField(max_length=7, default="#ff6b35", help_text="Title color (hex code)")
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order (0, 1, 2...)")
    is_active = models.BooleanField(default=True, help_text="Show on homepage?")
    
    # Meta Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Home Section Card"
        verbose_name_plural = "Home Section Cards"
    
    def __str__(self):
        if self.title_line2:
            return f"{self.title_line1} - {self.title_line2}"
        return self.title_line1
    
    def get_image(self):
        """Returns image URL - uploaded ya external"""
        if self.card_image:
            return self.card_image.url
        return self.image_url if self.image_url else 'https://via.placeholder.com/100'


class CollegeCounsellingCard(models.Model):
    """Model for College Admission Counselling Services Page Cards"""
    
    BORDER_COLOR_CHOICES = [
        ('#f39c12', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#2ecc71', 'Green'),
        ('#3498db', 'Blue'),
    ]
    
    # Card Content
    title = models.CharField(max_length=100, help_text="Card title (e.g., Admission India)")
    description = models.TextField(max_length=200, help_text="Short description")
    
    # Image
    card_image = models.ImageField(upload_to='counselling_cards/', blank=True, null=True, help_text="Upload image")
    image_url = models.URLField(max_length=500, blank=True, help_text="OR paste image URL")
    
    # Link/Redirect
    redirect_link = models.CharField(max_length=500, blank=True, help_text="Card click pe kaha redirect ho?")
    
    # Styling
    border_color = models.CharField(max_length=7, default="#f39c12", choices=BORDER_COLOR_CHOICES, help_text="Border color")
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order (0, 1, 2...)")
    is_active = models.BooleanField(default=True, help_text="Show on counselling page?")
    
    # Meta Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "College Counselling Card"
        verbose_name_plural = "College Counselling Cards"
    
    def __str__(self):
        return self.title
    
    def get_image(self):
        """Returns image URL - uploaded ya external"""
        if self.card_image:
            return self.card_image.url
        return self.image_url if self.image_url else 'https://via.placeholder.com/100'
    

# models.py mein YE MODEL ADD KARO (existing models ke NEECHE)

class CareerCounsellingService(models.Model):
    """Model for Career Counselling Services Page"""
    
    BORDER_COLOR_CHOICES = [
        ('#f39c12', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#9b59b6', 'Purple'),
        ('#2ecc71', 'Green'),
        ('#3498db', 'Blue'),
    ]
    
    title = models.CharField(max_length=150, help_text="Service title")
    description = models.TextField(max_length=200, help_text="Short description")
    
    # SVG Icon (text field for SVG code)
    svg_icon = models.TextField(blank=True, help_text="Paste SVG code here")
    
    redirect_link = models.CharField(max_length=500, blank=True, help_text="Redirect URL")
    border_color = models.CharField(max_length=7, default="#f39c12", choices=BORDER_COLOR_CHOICES)
    
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Career Counselling Service"
        verbose_name_plural = "Career Counselling Services"
    
    def __str__(self):
        return self.title
    
# models.py mein YE MODEL ADD KARO
class AdmissionIndiaCard(models.Model):
    """Model for Admission India Services Page Cards"""
    
    CARD_TYPE_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
    ]
    
    # Card Content
    title = models.CharField(max_length=200, help_text="Card title (e.g., ALL INDIA STATE WISE COUNSELLING)")
    
    # Features (4 items)
    feature_1 = models.CharField(max_length=100, default="State wise Updates", help_text="Feature 1")
    feature_2 = models.CharField(max_length=100, default="Verified Information", help_text="Feature 2")
    feature_3 = models.CharField(max_length=100, default="Real time Information", help_text="Feature 3")
    feature_4 = models.CharField(max_length=100, default="Expert Counselling", help_text="Feature 4")
    
    # Link/Redirect
    redirect_link = models.CharField(max_length=500, blank=True, help_text="Card click pe kaha redirect ho?")
    
    # Payment Settings
    card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES, default='free', help_text="Free ya Paid?")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Price (agar paid hai to yaha likho)")
    description = models.TextField(blank=True, help_text="Card ke baare mein description")
    
    # Styling
    border_gradient_start = models.CharField(max_length=7, default="#ED651C", help_text="Gradient start color")
    border_gradient_end = models.CharField(max_length=7, default="#F4800C", help_text="Gradient end color")
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order (0, 1, 2...)")
    is_active = models.BooleanField(default=True, help_text="Show on page?")
    
    # Meta Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Admission India Card"
        verbose_name_plural = "Admission India Cards"
    
    def __str__(self):
        return f"{self.title} - {self.get_card_type_display()}"




class AllIndiaServiceCard(models.Model):
    """Model for All India State Wise Counselling Services Page"""
    
    CATEGORY_CHOICES = [
        ('cat-1', 'Orange'),
        ('cat-2', 'Red'),
        ('cat-3', 'Yellow'),
        ('cat-4', 'Green'),
        ('cat-5', 'Blue'),
        ('cat-6', 'Purple'),
        ('cat-7', 'Pink'),
        ('cat-8', 'Teal'),
        ('cat-9', 'Indigo'),
        ('cat-10', 'Cyan'),
    ]
    
    # Card Content
    title = models.CharField(max_length=200, help_text="Service title (e.g., COLLEGE COMPARISON)")
    
    # Icon/Image
    card_image = models.ImageField(upload_to='all_india_services/', blank=True, null=True, help_text="Upload icon/image")
    image_url = models.URLField(max_length=500, blank=True, help_text="OR paste image URL")
    
    # Link/Redirect
    redirect_link = models.CharField(max_length=500, blank=True, help_text="Card click pe kaha redirect ho?")
    
    # Category Color
    category_class = models.CharField(max_length=20, default='cat-1', choices=CATEGORY_CHOICES, help_text="Card color category")
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order (1, 2, 3...)")
    is_active = models.BooleanField(default=True, help_text="Show on page?")
    
    # Meta Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "All India Service Card"
        verbose_name_plural = "All India Service Cards"
    
    def __str__(self):
        return f"{self.order}. {self.title}"
    
    def get_image(self):
        """Returns image URL - uploaded ya external"""
        if self.card_image:
            return self.card_image.url
        return self.image_url if self.image_url else 'https://via.placeholder.com/100'
    
    def get_slug(self):
        """Extract slug from redirect_link"""
        # Example: redirect_link = "/rti/" → slug = "rti"
        slug = self.redirect_link.strip('/').split('/')[-1]
        return slug if slug else 'card'
    
    def get_absolute_url(self):
        """Get card detail URL"""
        return f"/{self.get_slug()}/"
    


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==================== PROFESSIONAL COUNSELLING CARD MODEL ====================
class ProfessionalCounsellingCard(models.Model):
    """Cards displayed on Professional Counselling page"""
    
    BORDER_COLOR_CHOICES = [
        ('#f39c12', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#2ecc71', 'Green'),
        ('#9b59b6', 'Purple'),
        ('#3498db', 'Blue'),
    ]
    
    title = models.CharField(max_length=200, help_text="Card title")
    description = models.TextField(max_length=300, help_text="Card description")
    
    # Icon/Image
    card_image = models.ImageField(upload_to='counselling_cards/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    
    # Redirect (internal section)
    section_id = models.CharField(max_length=50, help_text="Section ID (documents, choices, status, doubts, complaints)")
    
    # Styling
    border_color = models.CharField(max_length=7, default='#f39c12', choices=BORDER_COLOR_CHOICES)
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Professional Counselling Card"
        verbose_name_plural = "Professional Counselling Cards"
    
    def __str__(self):
        return f"{self.order}. {self.title}"
    
    def get_image(self):
        if self.card_image:
            return self.card_image.url
        return self.image_url if self.image_url else 'https://via.placeholder.com/100'


# ==================== STUDENT DOCUMENT MODEL ====================
class StudentDocument(models.Model):
    """Documents uploaded by students"""
    
    DOCUMENT_TYPE_CHOICES = [
        # Mandatory
        ('PHOTO', 'PHOTO *'),
        ('SIGNATURE', 'SIGNATURE *'),
        ('10TH', '10TH MARKSHEET *'),
        ('12TH', '12TH MARKSHEET *'),
        ('FAMILY_ID', 'FAMILY ID * (Haryana Students)'),
        ('MIGRATION', 'MIGRATION CERTIFICATE *'),
        ('CHARACTER_CERTIFICATE', 'CHARACTER CERTIFICATE *'),
        ('AADHAR_CARD', 'AADHAR CARD *'),
        ('COMPETITIVE_EXAM_ADMIT_CARD', 'COMPETITIVE EXAM ADMIT CARD *'),
        ('COMPETITIVE_EXAM_RESULT_CARD', 'COMPETITIVE EXAM RESULT CARD *'),
        
        # Optional
        ('INCOME_CERTIFICATE', 'INCOME CERTIFICATE'),
        ('DOMICILE', 'DOMICILE CERTIFICATE'),
        ('BIRTH_CERTIFICATE', 'BIRTH CERTIFICATE'),
        
        # Caste Certificates
        ('SC', 'SC - Scheduled Caste Certificate'),
        ('ST', 'ST - Scheduled Tribe Certificate'),
        ('OBC', 'OBC - Other Backward Class Certificate'),
        ('BC_A', 'BC-A - Backward Class A Certificate'),
        ('BC_B', 'BC-B - Backward Class B Certificate'),
        ('PH', 'PH - Physically Handicapped Certificate'),
        ('ESM', 'ESM - Ex-Serviceman Certificate'),
        ('EWS', 'EWS - Economically Weaker Section Certificate'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_file = models.FileField(upload_to='student_documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ['student', 'document_type']
    
    def __str__(self):
        return f"{self.student.username} - {self.document_type}"


# ==================== CHOICE FILLING MODEL ====================
class ChoiceFilling(models.Model):
    """Student's college and course preferences"""
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='choices')
    preference_number = models.IntegerField()
    college_name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['preference_number']
        unique_together = ['student', 'preference_number']
    
    def __str__(self):
        return f"{self.student.username} - Pref {self.preference_number}"


# ==================== COUNSELLING STATUS MODEL ====================
class CounsellingStatus(models.Model):
    """Track student's counselling process"""
    
    STAGE_CHOICES = [
        ('registration', 'Registration Completed'),
        ('documents_upload', 'Documents Upload in Progress'),
        ('documents_verification', 'Documents Under Verification'),
        ('choice_filling', 'Choice Filling in Progress'),
        ('seat_allotment', 'Waiting for Seat Allotment'),
        ('seat_allocated', 'Seat Allocated'),
        ('admission_completed', 'Admission Completed'),
    ]
    
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='counselling_status')
    
    application_submitted = models.BooleanField(default=False)
    documents_verified = models.BooleanField(default=False)
    choice_filling_completed = models.BooleanField(default=False)
    
    seat_allotment_status = models.CharField(max_length=100, default='Pending')
    current_stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='registration')
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.current_stage}"


# ==================== DOUBT SESSION MODEL ====================
class DoubtSession(models.Model):
    """Student doubts and queries"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts')
    subject = models.CharField(max_length=200)
    doubt_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response = models.TextField(blank=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_doubts')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.subject}"


# ==================== COMPLAINT MODEL ====================
class Complaint(models.Model):
    """Student complaints"""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.CharField(max_length=100)
    complaint_subject = models.CharField(max_length=200)
    complaint_description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_response = models.TextField(blank=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_complaints')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.complaint_subject}"
    


class AdmissionAbroadCard(models.Model):
    """Model for Admission Abroad Services Page"""
    
    BORDER_COLOR_CHOICES = [
        ('#f39c12', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#3498db', 'Blue'),
        ('#2ecc71', 'Green'),
    ]
    
    # Card Content
    title = models.CharField(max_length=200, help_text="Service title")
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # ✅ ADD THIS
    description = models.TextField(max_length=300, help_text="Short description")
    
    # Icon/Image
    card_image = models.ImageField(upload_to='admission_abroad/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    
    # Link/Redirect (keep for backward compatibility)
    redirect_link = models.CharField(max_length=500, blank=True)
    
    # Styling
    border_color = models.CharField(max_length=7, default='#f39c12', choices=BORDER_COLOR_CHOICES)
    
    # Display
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Admission Abroad Card"
        verbose_name_plural = "Admission Abroad Cards"
    
    def __str__(self):
        return f"{self.order}. {self.title}"
    
    def save(self, *args, **kwargs):
        # ✅ Auto-generate slug from title
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_image(self):
        if self.card_image:
            return self.card_image.url
        return self.image_url if self.image_url else 'https://via.placeholder.com/100'
# models.py mein ye add karo


# ==================== DISTANCE EDUCATION MODEL ====================
class DistanceEducationCard(models.Model):
    """Distance Education service cards"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # ✅ ADD THIS
    description = models.TextField(blank=True)
    card_image = models.ImageField(upload_to='distance_education/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    border_color = models.CharField(max_length=20, default='#3498db')
    redirect_link = models.CharField(max_length=500, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Distance Education Card"
        verbose_name_plural = "Distance Education Cards"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    # ✅ ADD THIS METHOD
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_image(self):
        """Return image URL"""
        if self.card_image:
            return self.card_image.url
        elif self.image_url:
            return self.image_url
        return '/static/img/default-card.png'
# ==================== DISTANCE EDUCATION NESTED STRUCTURE ====================

class DistanceEducationSubCategory(models.Model):
    """Nested subcategories for Distance Education (infinite levels)"""
    parent_card = models.ForeignKey(
        DistanceEducationCard, 
        on_delete=models.CASCADE, 
        related_name='sub_categories',
        null=True, 
        blank=True
    )
    parent_subcategory = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='children',
        null=True, 
        blank=True
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
     # ✅ NEW FIELDS - Country, State & Course Filter
    target_country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='distance_education_subcategories',
                                      help_text="Target country (for international programs)")
    student_state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='distance_education_sub_categories',
                                     help_text="Student's home state (leave blank for all states)")
    course = models.CharField(max_length=100, blank=True, null=True,
                             help_text="Select course (leave blank for all courses)")
    
    # Icon options
    icon_image = models.ImageField(upload_to='distance_education/icons/', blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    icon_color = models.CharField(max_length=20, default='#007bff')
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Distance Education Sub-Category"
        verbose_name_plural = "Distance Education Sub-Categories"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_icon(self):
        """Return icon image or URL"""
        if self.icon_image:
            return self.icon_image.url
        elif self.icon_url:
            return self.icon_url
        return '/static/img/default-icon.png'
    
    def get_children(self):
        """Get all child subcategories"""
        return self.children.filter(is_active=True).order_by('order')
    
    def has_children(self):
        """Check if has child subcategories"""
        return self.children.filter(is_active=True).exists()
    
    def get_breadcrumb(self):
        """Get breadcrumb trail"""
        breadcrumb = []
        current = self
        while current:
            breadcrumb.insert(0, {'id': current.id, 'title': current.title})
            current = current.parent_subcategory
        return breadcrumb
    
    def get_root_card(self):
        """Get the root card by traversing up"""
        current = self
        while current.parent_subcategory:
            current = current.parent_subcategory
        return current.parent_card


class DistanceEducationPage(models.Model):
    """Content pages for Distance Education subcategories"""
    sub_category = models.ForeignKey(
        DistanceEducationSubCategory,
        on_delete=models.CASCADE,
        related_name='content_pages'
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    summary = models.TextField(blank=True)
    content = models.TextField()
    
    # SEO & Images
    featured_image = models.ImageField(upload_to='distance_education/pages/', blank=True, null=True)
    featured_image_url = models.URLField(blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Distance Education Page"
        verbose_name_plural = "Distance Education Pages"
        ordering = ['order', 'title']
        unique_together = ['sub_category', 'slug']
    
    def __str__(self):
        return f"{self.sub_category.title} - {self.title}"
    
    def get_featured_image(self):
        """Return featured image or URL"""
        if self.featured_image:
            return self.featured_image.url
        elif self.featured_image_url:
            return self.featured_image_url
        return None
    
    def increment_views(self):
        """Increment page views"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

# ==================== ONLINE EDUCATION MODEL ====================


class OnlineEducationCard(models.Model):
    """Model for Online Education Services Page"""
    
    BORDER_COLOR_CHOICES = [
        ('#f39c12', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#3498db', 'Blue'),
        ('#2ecc71', 'Green'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # ✅ ADD THIS
    description = models.TextField(max_length=300)
    
    card_image = models.ImageField(upload_to='online_education/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    
    redirect_link = models.CharField(max_length=500, blank=True)
    border_color = models.CharField(max_length=7, default='#f39c12', choices=BORDER_COLOR_CHOICES)
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Online Education Card"
        verbose_name_plural = "Online Education Cards"
    
    def __str__(self):
        return f"{self.order}. {self.title}"
    
    # ✅ ADD THIS METHOD
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_image(self):
        if self.card_image:
            return self.card_image.url
        return self.image_url if self.image_url else 'https://via.placeholder.com/100'


# ✅ ADD NEW MODELS
# models.py mein OnlineEducationSubCategory UPDATE karo

class OnlineEducationSubCategory(models.Model):
    """Nested subcategories for Online Education (infinite levels)"""
    parent_card = models.ForeignKey(
        OnlineEducationCard, 
        on_delete=models.CASCADE, 
        related_name='sub_categories',
        null=True, 
        blank=True
    )
    parent_subcategory = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='children',
        null=True, 
        blank=True
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    # ✅ NEW FIELDS - Country, State & Course Filter
    target_country = models.ForeignKey(
        'Country', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='online_education_subcategories',
        help_text="Target country (for international programs)"
    )
    student_state = models.ForeignKey(
        'State', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='online_education_sub_categories',
        help_text="Student's home state (leave blank for all states)"
    )
    course = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Select course (leave blank for all courses)"
    )
    
    # Icon options
    icon_image = models.ImageField(upload_to='online_education/icons/', blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    icon_color = models.CharField(max_length=20, default='#007bff')
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Online Education Sub-Category"
        verbose_name_plural = "Online Education Sub-Categories"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_icon(self):
        if self.icon_image:
            return self.icon_image.url
        elif self.icon_url:
            return self.icon_url
        return '/static/img/default-icon.png'
    
    def get_children(self):
        """Get all active children"""
        return self.children.filter(is_active=True).order_by('order')
    
    def has_children(self):
        """Check if has child subcategories"""
        return self.children.filter(is_active=True).exists()
    
    def get_breadcrumb(self):
        """Get breadcrumb trail"""
        breadcrumb = []
        current = self
        while current:
            breadcrumb.insert(0, {'id': current.id, 'title': current.title})
            current = current.parent_subcategory
        return breadcrumb
    
    def get_root_card(self):
        """Get the root card by traversing up"""
        current = self
        while current.parent_subcategory:
            current = current.parent_subcategory
        return current.parent_card
    
    # ✅ NEW METHOD - Check if visible to user
    def is_visible_to_user(self, user_registration):
        """
        Check if this subcategory should be visible to the given user
        based on their country, state, and course
        """
        if not user_registration:
            return True  # Show all if no registration
        
        # Check country filter
        if self.target_country:
            if self.target_country != user_registration.country:
                return False
        
        # Check state filter
        if self.student_state:
            if self.student_state != user_registration.state:
                return False
        
        # Check course filter
        if self.course:
            if self.course != user_registration.course:
                return False
        
        return True  # All filters passed
    
    
class OnlineEducationPage(models.Model):
    """Content pages for Online Education subcategories"""
    sub_category = models.ForeignKey(
        OnlineEducationSubCategory,
        on_delete=models.CASCADE,
        related_name='content_pages'
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    summary = models.TextField(blank=True)
    content = models.TextField()
    
    # SEO & Images
    featured_image = models.ImageField(upload_to='online_education/pages/', blank=True, null=True)
    featured_image_url = models.URLField(blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Online Education Page"
        verbose_name_plural = "Online Education Pages"
        ordering = ['order', 'title']
        unique_together = ['sub_category', 'slug']
    
    def __str__(self):
        return f"{self.sub_category.title} - {self.title}"
    
    def get_featured_image(self):
        if self.featured_image:
            return self.featured_image.url
        elif self.featured_image_url:
            return self.featured_image_url
        return None
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])




from django.db import models
from django.contrib.auth.models import User

# ==================== COUNTRY MODEL ====================
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # IN, US, UK
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ==================== STATE MODEL ====================
class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)  # HR, UP, CA
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('country', 'name')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.country.name})"


# ==================== USER REGISTRATION MODEL ====================
class UserRegistration(models.Model):
    COURSE_CHOICES = [
        ('B.TECH', 'B.TECH'),
        ('MBBS', 'MBBS'),
        ('B.COM', 'B.COM'),
        ('BBA', 'BBA'),
        ('BCA', 'BCA'),
        ('BSC NURSING', 'BSC NURSING'),
        ('BAMS', 'BAMS'),
        ('LLB [ 5 YEARS ]', 'LLB [ 5 YEARS ]'),
        ('MBA', 'MBA'),
        ('BSC COMP SCIENCE', 'BSC COMP SCIENCE'),
        ('B.PHARMA', 'B.PHARMA'),
        ('D.PHARMA', 'D.PHARMA'),
        ('ANM', 'ANM'),
        ('GNM', 'GNM'),
        ('BDS', 'BDS'),
        ('BSC BIOTECH', 'BSC BIOTECH'),
        ('B.TECH BIOTECH', 'B.TECH BIOTECH'),
        ('B.ED', 'B.ED'),
        ('MCA', 'MCA'),
        ('PHD', 'PHD'),
        ('M.COM', 'M.COM'),
        ('BA JMC', 'BA JMC'),
        ('BSC PCM', 'BSC PCM'),
        ('BSC CHEMISTRY', 'BSC CHEMISTRY'),
        ('BSC PHYSICS', 'BSC PHYSICS'),
        ('BSC MATHEMATICS', 'BSC MATHEMATICS'),
        ('BA CORE', 'BA CORE'),
        ('BA PSYCOLOGY', 'BA PSYCOLOGY'),
        ('BPT', 'BPT'),
        ('BUMS', 'BUMS'),
        ('BHMS', 'BHMS'),
        ('BSC OPERATION THEATER', 'BSC OPERATION THEATER'),
        ('HOTEL MANAGEMENT', 'HOTEL MANAGEMENT'),
        ('BSC ZOOLOGY', 'BSC ZOOLOGY'),
        ('BSC FOOD TECHNOLOGY', 'BSC FOOD TECHNOLOGY'),
        ('BSC ANIMATION AND MULTIMEDIA', 'BSC ANIMATION AND MULTIMEDIA'),
        ('BA SOCIAL WORK', 'BA SOCIAL WORK'),
        ('B.DESIGN', 'B.DESIGN'),
        ('BMS', 'BMS'),
        ('B.ARCH', 'B.ARCH'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15,unique=True)
    whatsapp_mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    
    # Foreign Keys
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100)
    
    # Password fields
    password = models.CharField(max_length=128)
    
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "User Registration"
        verbose_name_plural = "User Registrations"


#  ==================== COLLEGE MODEL ====================
class College(models.Model):
    """Colleges database"""
    
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='colleges')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='colleges')
    city = models.CharField(max_length=100)
    
    ranking = models.IntegerField(null=True, blank=True)
    tuition_fees = models.DecimalField(max_digits=10, decimal_places=2)
    courses_offered = models.TextField(help_text="Comma separated courses")
    facilities = models.TextField(blank=True)
    
    # Images
    college_image = models.ImageField(upload_to='colleges/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    
    website = models.URLField(max_length=500, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['country', 'state', 'name']
        verbose_name = "College"
        verbose_name_plural = "Colleges"
    
    def __str__(self):
        return f"{self.name} - {self.state.name}, {self.country.name}"
    
    def get_image(self):
        if self.college_image:
            return self.college_image.url
        return self.image_url if self.image_url else 'https://via.placeholder.com/300x200'


# ==================== COLLEGE COMPARISON MODEL (UPDATED) ====================
class CollegeComparison(models.Model):
    """College Comparisons created by Admin - Support Multiple Colleges"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    comparison_title = models.CharField(max_length=255, help_text="e.g., Top Engineering Colleges in Haryana")
    
    # CHANGE: ManyToMany for multiple colleges
    colleges = models.ManyToManyField(College, related_name='comparisons', help_text="Select 2 or more colleges to compare")
    
    # Filter fields - ye match karega UserRegistration ke country/state se
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='comparisons')
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True, related_name='comparisons')
    
    # Comparison details
    comparison_summary = models.TextField(blank=True, help_text="Short summary of comparison")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_comparisons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "College Comparison"
        verbose_name_plural = "College Comparisons"
    
    def __str__(self):
        return f"{self.comparison_title} ({self.country.name})"
    
    def get_colleges_list(self):
        """Return list of colleges in this comparison"""
        return self.colleges.all()
    
    def colleges_count(self):
        """Return number of colleges in comparison"""
        return self.colleges.count()
    

# ==================== STATE WISE COUNSELLING UPDATE MODEL ====================
class StateWiseCounsellingUpdate(models.Model):
    """Links to external state counselling websites"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    ICON_COLOR_CHOICES = [
        ('#ED651C', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#2ecc71', 'Green'),
        ('#3498db', 'Blue'),
        ('#9b59b6', 'Purple'),
        ('#f39c12', 'Yellow'),
        ('#1abc9c', 'Teal'),
    ]
    
    # State Info
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='counselling_updates')
    title = models.CharField(max_length=200, help_text="e.g., Haryana NEET Counselling 2025")
    description = models.TextField(max_length=300, blank=True, help_text="Short description about the counselling")
    
    # External Link
    external_link = models.URLField(max_length=500, help_text="External counselling website URL")
    
    # Icon/Image
    icon_image = models.ImageField(upload_to='counselling_updates/', blank=True, null=True, help_text="Upload icon")
    icon_url = models.URLField(max_length=500, blank=True, help_text="OR paste icon URL")
    icon_color = models.CharField(max_length=7, default='#ED651C', choices=ICON_COLOR_CHOICES, help_text="Icon background color")
    
    # Additional Info
    last_updated = models.DateField(blank=True, null=True, help_text="Last update date")
    is_new = models.BooleanField(default=False, help_text="Show 'NEW' badge?")
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['state', 'order', '-created_at']
        verbose_name = "State Wise Counselling Update"
        verbose_name_plural = "State Wise Counselling Updates"
    
    def __str__(self):
        return f"{self.state.name} - {self.title}"
    
    def get_icon(self):
        """Returns icon URL - uploaded ya external"""
        if self.icon_image:
            return self.icon_image.url
        return self.icon_url if self.icon_url else 'https://via.placeholder.com/100'
    

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



# In your SubCategory model in models.py, REPLACE the entire class with this:

# models.py mein SubCategory model UPDATE karo

class SubCategory(models.Model):
    """Sub-categories - UNLIMITED NESTING support"""
    
    ICON_COLOR_CHOICES = [
        ('#f39c12', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#2ecc71', 'Green'),
        ('#3498db', 'Blue'),
        ('#9b59b6', 'Purple'),
    ]
    
    # Parent References
    parent_card = models.ForeignKey('AllIndiaServiceCard', on_delete=models.CASCADE, 
                                    related_name='sub_categories', null=True, blank=True)
    parent_subcategory = models.ForeignKey('self', on_delete=models.CASCADE, 
                                          related_name='children', null=True, blank=True)
    
    # Sub-Category Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=300, blank=True)
    
    # ✅ NEW FIELDS - State & Course Filter
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='sub_categories',
                              help_text="Select state (leave blank for all states)")
    course = models.CharField(max_length=100, blank=True, null=True,
                             help_text="Select course (leave blank for all courses)")
    
    # Icon/Image
    icon_image = models.ImageField(upload_to='sub_categories/', blank=True, null=True)
    icon_url = models.URLField(max_length=500, blank=True)
    icon_color = models.CharField(max_length=7, default='#f39c12', choices=ICON_COLOR_CHOICES)
    
    # Display Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"
    
    def __str__(self):
        if self.parent_subcategory:
            return f"{self.parent_subcategory.title} → {self.title}"
        return f"{self.parent_card.title} → {self.title}"
    
    # Rest of your existing methods...
    
    def get_icon(self):
        if self.icon_image:
            return self.icon_image.url
        return self.icon_url if self.icon_url else 'https://via.placeholder.com/100'
    
    def has_children(self):
        """Check if has child subcategories"""
        return self.children.filter(is_active=True).exists()
    
    def get_children(self):
        """Get all active children"""
        return self.children.filter(is_active=True).order_by('order')
    
    def pages_count(self):
        """Get pages count"""
        return self.content_pages.filter(is_active=True).count()
    
    def get_breadcrumb(self):
        """
        Get ONLY the subcategory chain WITHOUT the parent card
        Returns list: [parent_subcategory, ..., self]
        """
        path = [self]
        current = self.parent_subcategory
        
        # Navigate up through parent subcategories ONLY
        while current:
            path.insert(0, current)
            current = current.parent_subcategory
        
        return path
    
    def get_full_path(self):
        """Get URL path: engineering/government/delhi"""
        path = [self.slug]
        current = self.parent_subcategory
        
        while current:
            path.insert(0, current.slug)
            current = current.parent_subcategory
        
        return '/'.join(path)
    

# ==================== CONTENT PAGE MODEL (Level 3) ====================
class ContentPage(models.Model):
    """Individual content pages under SubCategory"""
    
    # Parent Sub-Category
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='content_pages')
    
    # Page Info
    title = models.CharField(max_length=300, help_text="e.g., Top 10 Engineering Colleges in India")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # Content
    summary = models.TextField(max_length=500, blank=True, help_text="Short summary (optional)")
    content = models.TextField(help_text="Full page content (HTML supported)")
    
    # Featured Image
    featured_image = models.ImageField(upload_to='content_pages/', blank=True, null=True)
    featured_image_url = models.URLField(max_length=500, blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma separated keywords")
    
    # Display Settings
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show as featured content?")
    
    # Stats
    views_count = models.IntegerField(default=0, help_text="Page view count")
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['sub_category', 'order', '-created_at']
        verbose_name = "Content Page"
        verbose_name_plural = "Content Pages"
        unique_together = ['sub_category', 'slug']
    
    def __str__(self):
        return f"{self.sub_category.title} → {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_featured_image(self):
        if self.featured_image:
            return self.featured_image.url
        return self.featured_image_url if self.featured_image_url else 'https://via.placeholder.com/800x400'
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


# models.py mein ye add karo
# **DELETE THE SECOND DEFINITION** - Keep only ONE copy of AdmissionAbroadSubCategory and AdmissionAbroadPage


# The duplicate appears around line 450-550 in your file
# You have:
# 1. First definition: lines ~320-380
# 2. Second definition: lines ~450-550 (DELETE THIS ONE)


# Here's the SINGLE correct version of AdmissionAbroadSubCategory:


# models.py mein AdmissionAbroadSubCategory UPDATE karo

class AdmissionAbroadSubCategory(models.Model):
    """Sub-categories for Admission Abroad - UNLIMITED NESTING"""
    
    ICON_COLOR_CHOICES = [
        ('#f39c12', 'Orange'),
        ('#e74c3c', 'Red'),
        ('#2ecc71', 'Green'),
        ('#3498db', 'Blue'),
        ('#9b59b6', 'Purple'),
    ]
    
    # Parent References
    parent_card = models.ForeignKey('AdmissionAbroadCard', on_delete=models.CASCADE, 
                                    related_name='sub_categories', null=True, blank=True)
    parent_subcategory = models.ForeignKey('self', on_delete=models.CASCADE, 
                                          related_name='children', null=True, blank=True)
    
    # Sub-Category Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=300, blank=True)
    
    # ✅ NEW FIELDS - Country, State & Course Filter
    target_country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='admission_abroad_subcategories',
                                      help_text="Target country (e.g., Russia, USA)")
    student_state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='admission_abroad_sub_categories',
                                     help_text="Student's home state (leave blank for all states)")
    course = models.CharField(max_length=100, blank=True, null=True,
                             help_text="Select course (leave blank for all courses)")
    
    # Icon/Image
    icon_image = models.ImageField(upload_to='admission_abroad_sub/', blank=True, null=True)
    icon_url = models.URLField(max_length=500, blank=True)
    icon_color = models.CharField(max_length=7, default='#f39c12', choices=ICON_COLOR_CHOICES)
    
    # Display Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Admission Abroad Sub Category"
        verbose_name_plural = "Admission Abroad Sub Categories"
    
    def __str__(self):
        if self.parent_subcategory:
            return f"{self.parent_subcategory.title} → {self.title}"
        return f"{self.parent_card.title} → {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_icon(self):
        if self.icon_image:
            return self.icon_image.url
        return self.icon_url if self.icon_url else 'https://via.placeholder.com/100'
    
    def has_children(self):
        return self.children.filter(is_active=True).exists()
    
    def get_children(self):
        return self.children.filter(is_active=True).order_by('order')
    
    def get_root_card(self):
        if self.parent_card:
            return self.parent_card
        elif self.parent_subcategory:
            return self.parent_subcategory.get_root_card()
        return None
    
    def get_breadcrumb(self):
        breadcrumb = []
        current = self
        
        while current:
            breadcrumb.insert(0, {'id': current.id, 'title': current.title})
            current = current.parent_subcategory
        
        root_card = self.get_root_card()
        if root_card:
            breadcrumb.insert(0, {'id': root_card.id, 'title': root_card.title})
        
        return breadcrumb
    
    def get_full_path(self):
        path = [self.slug]
        current = self.parent_subcategory
        
        while current:
            path.insert(0, current.slug)
            current = current.parent_subcategory
        
        return '/'.join(path)
    


# Same for AdmissionAbroadPage - Keep only ONE copy
class AdmissionAbroadPage(models.Model):
    """Content pages for Admission Abroad"""
    
    # Parent Sub-Category
    sub_category = models.ForeignKey(AdmissionAbroadSubCategory, on_delete=models.CASCADE, 
                                     related_name='content_pages')
    
    # Page Info
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # Content
    summary = models.TextField(max_length=500, blank=True)
    content = models.TextField(help_text="Full page content (HTML supported)")
    
    # Featured Image
    featured_image = models.ImageField(upload_to='admission_abroad_pages/', blank=True, null=True)
    featured_image_url = models.URLField(max_length=500, blank=True)
    
    # Display Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Stats
    views_count = models.IntegerField(default=0)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['sub_category', 'order', '-created_at']
        
    def __str__(self):
        return f"{self.sub_category.title} → {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class AdmissionAbroadPage(models.Model):
    """Content pages for Admission Abroad"""
    
    # Parent Sub-Category
    sub_category = models.ForeignKey(AdmissionAbroadSubCategory, on_delete=models.CASCADE, 
                                     related_name='content_pages')
    
    # Page Info
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # Content
    summary = models.TextField(max_length=500, blank=True)
    content = models.TextField(help_text="Full page content (HTML supported)")
    
    # Featured Image
    featured_image = models.ImageField(upload_to='admission_abroad_pages/', blank=True, null=True)
    featured_image_url = models.URLField(max_length=500, blank=True)
    
    # Display Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Stats
    views_count = models.IntegerField(default=0)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['sub_category', 'order', '-created_at']
        
    def __str__(self):
        return f"{self.sub_category.title} → {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ==================== STUDENT CARD PURCHASE MODEL ====================
class StudentCardPurchase(models.Model):
    """Model to track student card purchases"""
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    student = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='card_purchases')
    card = models.ForeignKey(AdmissionIndiaCard, on_delete=models.CASCADE, related_name='purchases')
    
    # Payment Info
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Transaction Details
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, help_text="Credit Card, UPI, etc.")
    
    # Timestamps
    purchased_at = models.DateTimeField(auto_now_add=True)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'card')  # Ek student ek card sirf ek bar kharid sakta hai
        verbose_name = "Student Card Purchase"
        verbose_name_plural = "Student Card Purchases"
        ordering = ['-purchased_at']
    
    def __str__(self):
        return f"{self.student.name} - {self.card.title}"
    
    @property
    def is_purchased(self):
        """Check agar card successfully purchased hai"""
        return self.payment_status == 'completed'


# Add these models to your existing models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ==================== MANAGEMENT QUOTA COLLEGE MODEL ====================
class ManagementQuotaCollege(models.Model):
    """Colleges offering management quota seats"""
    
    college = models.OneToOneField(College, on_delete=models.CASCADE, related_name='management_quota')
    management_seats_available = models.IntegerField(default=0, help_text="Number of management quota seats")
    courses_offered = models.TextField(help_text="Comma-separated list of courses available")
    fee_structure = models.TextField(blank=True, help_text="Fee details for management quota")
    eligibility_criteria = models.TextField(blank=True)
    
    # Contact
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    accepts_applications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Management Quota College"
        verbose_name_plural = "Management Quota Colleges"
    
    def __str__(self):
        return f"{self.college.name} - Management Quota"
    
    def seats_filled(self):
        """Get number of approved applications"""
        return self.applications.filter(status='approved').count()
    
    def seats_remaining(self):
        """Get remaining seats"""
        return self.management_seats_available - self.seats_filled()


# ==================== MANAGEMENT QUOTA APPLICATION MODEL ====================
class ManagementQuotaApplication(models.Model):
    """Student applications for management quota"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlist', 'Waitlist'),
    ]
    
    # Relationships
    student = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='management_quota_applications')
    college = models.ForeignKey(ManagementQuotaCollege, on_delete=models.CASCADE, related_name='applications')
    
    # Application Details
    course_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # Academic Details
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_marks = models.DecimalField(max_digits=5, decimal_places=2)
    entrance_exam_score = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Documents
    tenth_marksheet = models.FileField(upload_to='management_quota/tenth/')
    twelfth_marksheet = models.FileField(upload_to='management_quota/twelfth/')
    exam_scorecard = models.FileField(upload_to='management_quota/exam/', null=True, blank=True)
    
    # Status & Admin Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_mq_applications')
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['student', 'college']  # One application per student per college
        verbose_name = "Management Quota Application"
        verbose_name_plural = "Management Quota Applications"
    
    def __str__(self):
        return f"{self.student.name} - {self.college.college.name}"
    
    def get_average_marks(self):
        """Calculate average of 10th and 12th marks"""
        return (float(self.tenth_marks) + float(self.twelfth_marks)) / 2
    
    def mark_as_reviewed(self, admin_user, action, remarks=""):
        """Mark application as reviewed"""
        self.status = action
        self.admin_remarks = remarks
        self.reviewed_by = admin_user
        self.reviewed_at = timezone.now()
        self.save()


# ==================== MANAGEMENT QUOTA NOTIFICATION MODEL ====================
class ManagementQuotaNotification(models.Model):
    """Notifications for students about their applications"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('submitted', 'Application Submitted'),
        ('approved', 'Application Approved'),
        ('rejected', 'Application Rejected'),
        ('waitlist', 'Added to Waitlist'),
        ('document_required', 'Additional Documents Required'),
    ]
    
    student = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='mq_notifications')
    application = models.ForeignKey(ManagementQuotaApplication, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.name} - {self.title}"


# ==================== MANAGEMENT QUOTA SEAT ALLOCATION MODEL ====================
class ManagementQuotaSeatAllocation(models.Model):
    """Seat allocation for approved applicants"""
    
    allocation_choices = [
        ('allotted', 'Seat Allotted'),
        ('joined', 'Student Joined'),
        ('not_joined', 'Student Did Not Join'),
    ]
    
    application = models.OneToOneField(ManagementQuotaApplication, on_delete=models.CASCADE, related_name='seat_allocation')
    allocation_roll_number = models.CharField(max_length=50, unique=True)
    
    seat_number = models.CharField(max_length=50)
    allotment_date = models.DateField()
    joining_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=allocation_choices, default='allotted')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Management Quota Seat Allocation"
        verbose_name_plural = "Management Quota Seat Allocations"
    
    def __str__(self):
        return f"Roll: {self.allocation_roll_number} - {self.application.student.name}"