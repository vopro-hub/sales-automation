"""Check the slug if it already exist"""

from django.utils.text import slugify
from core.models import Tenant

def generate_unique_tenant_slug(brand_name):
    base_slug = slugify(brand_name)
    slug = base_slug
    counter = 1

    while Tenant.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
