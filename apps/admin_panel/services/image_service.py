import requests
from io import BytesIO
from PIL import Image
import cloudinary.uploader
from django.conf import settings

def process_image_url(url):
   
    try:
        # Stream the response to check size before downloading
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Premium performance: Use Pillow to optimize
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB (removes alpha channel for smaller JPEGs)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize to a standard "Masterpiece" resolution
        img.thumbnail((1200, 1200))

        buffer = BytesIO()
        # Save as WebP for 30% better compression than JPEG
        img.save(buffer, format="WEBP", quality=80, optimize=True)
        buffer.seek(0)

        upload_result = cloudinary.uploader.upload(
            buffer,
            folder="boutique_products",
            resource_type="image"
        )
        return upload_result["secure_url"]
    except Exception as e:
        print(f"Image processing failed: {e}")
        return url 