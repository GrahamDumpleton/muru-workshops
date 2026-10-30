from django.db import migrations

NAMES = ["Teapot", "Mug", "Tea towel"]


def add_products(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    Product.objects.bulk_create(Product(name=name) for name in NAMES)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]

    operations = [migrations.RunPython(add_products, migrations.RunPython.noop)]
