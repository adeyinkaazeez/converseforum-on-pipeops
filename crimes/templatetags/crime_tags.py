from django import template
from ..models import *
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
import markdown
from django.shortcuts import render, get_object_or_404, redirect


register = template.Library()


@register.simple_tag
def total_published_posts():
    return Crimes.published.count()

@register.simple_tag
def total_draft_posts():
    return Crimes.draft.count()

@register.simple_tag
def total_posts():
    return Crimes.published.count() + Crimes.draft.count()

@register.simple_tag
def comment_per_post():
    return Crimes.objects.annotate(number_of_comments=Count('crime_comments'))

@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Crimes.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Crimes.published.annotate(
    total_comments=Count('crime_comments')).order_by('-total_comments', '-publish')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def post_comments():
     
    return Crimes.published.annotate(
    total_comments=Count('crime_comments')).order_by('-total_comments')