from django.db import migrations, models
from django.utils.text import slugify

def generate_unique_slugs(apps, schema_editor):
    """Generate unique slugs for existing cards"""
    AdmissionAbroadCard = apps.get_model('main_app', 'AdmissionAbroadCard')
    
    for card in AdmissionAbroadCard.objects.all():
        base_slug = slugify(card.title)
        slug = base_slug
        counter = 1
        
        # Ensure uniqueness
        while AdmissionAbroadCard.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        card.slug = slug
        card.save(update_fields=['slug'])
        print(f"Generated slug: {card.title} -> {slug}")

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_admissionabroadsubcategory_admissionabroadpage_and_more'),  # ✅ CORRECT
    ]

    operations = [
        # Step 1: Add slug field (nullable first)
        migrations.AddField(
            model_name='admissionabroadcard',
            name='slug',
            field=models.SlugField(max_length=200, null=True, blank=True),
        ),
        
        # Step 2: Generate slugs for existing data
        migrations.RunPython(generate_unique_slugs, migrations.RunPython.noop),
        
        # Step 3: Make slug unique and non-nullable
        migrations.AlterField(
            model_name='admissionabroadcard',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]