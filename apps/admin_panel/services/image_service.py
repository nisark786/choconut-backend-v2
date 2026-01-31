import requests
from io import BytesIO
from PIL import Image
import cloudinary.uploader
from django.conf import settings

def process_image_url(url):
   
    try:
 
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

    
        img = Image.open(BytesIO(response.content))
        
        
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

    
        img.thumbnail((1200, 1200))

        buffer = BytesIO()
       
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