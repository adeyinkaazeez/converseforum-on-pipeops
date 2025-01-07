from django import template
from ..models import *
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
import markdown
from django.shortcuts import render, get_object_or_404, redirect


register = template.Library()


@register.simple_tag
def total_published_posts():
    return Business_Articles.published.count()

@register.simple_tag
def total_draft_posts():
    return Business_Articles.draft.count()

@register.simple_tag
def total_posts():
    return Business_Articles.published.count() + Business_Articles.draft.count()

@register.simple_tag
def comment_per_post():
    return Business_Articles.objects.annotate(number_of_comments=Count('business_article_comments'))

@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Business_Articles.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Business_Articles.published.annotate(
    total_comments=Count('business_article_comments')).order_by('-total_comments', '-publish')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def post_comments():
     
    return Business_Articles.published.annotate(
    total_comments=Count('business_article_comments')).order_by('-total_comments')