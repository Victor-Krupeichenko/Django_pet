from django import template
from blog.models import Category
from django.db.models import Count
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag("_inc/post_by_category.html")
def get_categories():
    """View category and count posts for category"""
    categories = cache.get("categories")
    if not categories:
        categories = Category.objects.filter(post__is_publish=True).annotate(cnt=Count("post"))
        cache.set("categories", categories, 60)
    context = {
        "categories": categories
    }
    return context
