from django import template
from ..models import Business
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from queryset_sequence import QuerySetSequence


register = template.Library()


                                          
@register.simple_tag
def comment_per_post():
    return Business.objects.annotate(number_of_comments=Count('business_comments'))

@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Business.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}



@register.simple_tag
def get_most_commented_posts(count=5):
    return Business.published.annotate(
    total_comments= Count('business_comments')).order_by('-total_comments', '-publish')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def post_comments():
     
    return Business.published.annotate(
    total_comments=Count('business_comments')).order_by('-total_comments')