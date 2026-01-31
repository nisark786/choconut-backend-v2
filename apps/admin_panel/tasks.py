from celery import shared_task
from apps.products.models.product_model import Product
from .services.image_service import process_image_url

@shared_task
def upload_product_image_task(product_id, image_url):
    try:
        product = Product.objects.get(id=product_id)
        
        if "cloudinary" not in product.image:
            new_url = process_image_url(image_url)
            product.image = new_url
            product.save(update_fields=['image'])
    except Product.DoesNotExist:
        pass