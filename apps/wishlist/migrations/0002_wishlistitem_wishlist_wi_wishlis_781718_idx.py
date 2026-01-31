

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_created_at_alter_product_price_and_more'),
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='wishlistitem',
            index=models.Index(fields=['wishlist', 'product'], name='wishlist_wi_wishlis_781718_idx'),
        ),
    ]
