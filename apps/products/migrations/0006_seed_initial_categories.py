from django.db import migrations
from django.utils.text import slugify

def seed_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    categories_to_add = [
        "Fashion",
        "Food & Grocery",
        "Crafts & Art",
        "Beauty & Health",
        "Home & Living"
    ]
    for cat_name in categories_to_add:
        # Custom save() methods are NOT called during migrations. We must provide the slug manually.
        Category.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_productimage_image'),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
