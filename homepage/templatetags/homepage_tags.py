from django import template
from django.shortcuts import render, redirect
from django.http import HttpResponse
from newss.models import Political
from business.models import Business
from crimes.models import Crimes
from entertainments.models import Entertainments
from internationals.models import Internationals
from educations.models import Educations
from sciences.models import Science_AND_Techs
from sports.models import Sports
from health_articles.models import Healths
from political_articles.models import Political_Articless
from happening.models import Happenings
from innovations.models import Innovative_Articles
from lifestyles.models import Lifestyle_Articles
from religions.models import Religion_Articles
from sport_articles.models import Sport_Articles
from cultures.models import Cultures
from foods.models import Foods
from business__articles.models import Business_Articles
from howtos.models import Howtos
from celeb.models import Celeb
from loves.models import Loves
from campuss.models import Campuss
from personalitys.models import Personalities
from events.models import Events

from queryset_sequence import QuerySetSequence
from functools import reduce
from itertools import chain
from django.db.models import Count, Q

register = template.Library()

@register.simple_tag
def show_latest_posts(count=4):
    latest_posts = reduce(QuerySetSequence, [Crimes.published.select_related('author').order_by('-publish'), Business.published.select_related('author').order_by('-publish'),
                                         Political.published.select_related('author').order_by('-publish'), Entertainments.published.select_related('author').order_by('-publish'),
                                         Internationals.published.select_related('author').order_by('-publish'),Educations.published.select_related('author').order_by('-publish'),
                                         Science_AND_Techs.published.select_related('author').order_by('-publish'), Sports.published.select_related('author').order_by('-publish'),
                                         Healths.published.select_related('author').order_by('-publish'), Political_Articless.published.select_related('author').order_by('-publish'),
                                         Happenings.published.select_related('author').order_by('-publish'), Innovative_Articles.published.select_related('author').order_by('-publish'),
                                         Lifestyle_Articles.published.select_related('author').order_by('-publish'), Religion_Articles.published.select_related('author').order_by('-publish'),
                                         Sport_Articles.published.select_related('author').order_by('-publish'), Cultures.published.select_related('author').order_by('-publish'),
                                         Foods.published.select_related('author').order_by('-publish'), Business_Articles.published.select_related('author').order_by('-publish'),
                                         Howtos.published.select_related('author').order_by('-publish'), Celeb.published.select_related('author').order_by('-publish'),
                                         Loves.published.select_related('author').order_by('-publish'), Campuss.published.select_related('author').order_by('-publish'),
                                         Personalities.published.select_related('author').order_by('-publish'), Events.published.select_related('author').order_by('-publish') ]).order_by('-publish')[:count]
    
    return latest_posts

@register.simple_tag
def get_most_commented_posts(count=10):
    most_commented = reduce(QuerySetSequence, [Crimes.published.annotate(total_comments=Count('crime_comments')).order_by('-total_comments', '-publish'),
                                               Business.published.annotate(total_comments=Count('business_comments')).order_by('-total_comments', '-publish'),
                                               Political.published.annotate(total_comments=Count('politics_comments')).order_by('-total_comments', '-publish'),
                                               Entertainments.published.annotate(total_comments=Count('entertainment_comments')).order_by('-total_comments', '-publish'),
                                               Educations.published.annotate(total_comments=Count('education_comments')).order_by('-total_comments', '-publish'),
                                               Healths.published.annotate(total_comments=Count('health_comments')).order_by('-total_comments', '-publish'),
                                               Political_Articless.published.annotate(total_comments=Count('political_comments')).order_by('-total_comments', '-publish'),
                                               Happenings.published.annotate(total_comments=Count('happenings_comments')).order_by('-total_comments', '-publish'),
                                               Innovative_Articles.published.annotate(total_comments=Count('innovation_comments')).order_by('-total_comments', '-publish'),
                                               Lifestyle_Articles.published.annotate(total_comments=Count('lifestyle_comments')).order_by('-total_comments', '-publish'),
                                               Religion_Articles.published.annotate(total_comments=Count('religion_comments')).order_by('-total_comments', '-publish'),
                                               Sport_Articles.published.annotate(total_comments=Count('sports_comments')).order_by('-total_comments', '-publish'),
                                               Cultures.published.annotate(total_comments=Count('culture_comments')).order_by('-total_comments', '-publish'),
                                               Foods.published.annotate(total_comments=Count('food_comments')).order_by('-total_comments', '-publish'),
                                               Business_Articles.published.annotate(total_comments=Count('business_article_comments')).order_by('-total_comments', '-publish'),
                                               Howtos.published.annotate(total_comments=Count('howto_comments')).order_by('-total_comments', '-publish'),
                                               Celeb.published.annotate(total_comments=Count('celebrity_comments')).order_by('-total_comments', '-publish'),
                                               Loves.published.annotate(total_comments=Count('love_comments')).order_by('-total_comments', '-publish'),
                                               Campuss.published.annotate(total_comments=Count('campus_comments')).order_by('-total_comments', '-publish'),
                                               Personalities.published.annotate(total_comments=Count('personality_comments')).order_by('-total_comments', '-publish'),
                                               Events.published.annotate(total_comments=Count('event_comments')).order_by('-total_comments', '-publish')]).order_by('-total_comments', '-publish')[:count]
    
    return most_commented


    


@register.simple_tag
def total_published_posts():
    return  Crimes.published.count() + Business.published.count() + Political.published.count()+ Entertainments.published.count()+Internationals.published.count()+Educations.published.count() +\
                                         Science_AND_Techs.published.count()+ Sports.published.count()+\
                                         Healths.published.count() + Political_Articless.published.count()+\
                                         Happenings.published.count() + Innovative_Articles.published.count()+\
                                         Lifestyle_Articles.published.count()+ Religion_Articles.published.count()+\
                                         Sport_Articles.published.count()+ Cultures.published.count()+\
                                         Foods.published.count()+ Business_Articles.published.count()+\
                                         Howtos.published.count()+ Celeb.published.count()+\
                                         Loves.published.count()+ Campuss.published.count()+\
                                         Personalities.published.count()+ Events.published.count()

@register.simple_tag
def total_draft_posts():
    return Crimes.draft.count()+ Business.draft.count()+\
                                          Political.draft.count() + Entertainments.draft.count()+\
                                         Internationals.draft.count() + Educations.draft.count()+\
                                         Science_AND_Techs.draft.count() + Sports.draft.count()+\
                                         Healths.draft.count() + Political_Articless.draft.count()+\
                                         Happenings.draft.count() + Innovative_Articles.draft.count()+\
                                         Lifestyle_Articles.draft.count() + Religion_Articles.draft.count()+\
                                         Sport_Articles.draft.count() + Cultures.draft.count()+\
                                         Foods.draft.count() + Business_Articles.draft.count()+ Howtos.draft.count() + Celeb.draft.count()+\
                                         Loves.draft.count() + Campuss.draft.count()+\
                                         Personalities.draft.count() + Events.draft.count()

@register.simple_tag
def total_posts():
    return Crimes.published.count() + Business.published.count() + Political.published.count()+ Entertainments.published.count()+Internationals.published.count()+Educations.published.count() +\
                                         Science_AND_Techs.published.count()+ Sports.published.count()+\
                                         Healths.published.count() + Political_Articless.published.count()+\
                                         Happenings.published.count() + Innovative_Articles.published.count()+\
                                         Lifestyle_Articles.published.count()+ Religion_Articles.published.count()+\
                                         Sport_Articles.published.count()+ Cultures.published.count()+\
                                         Foods.published.count()+ Business_Articles.published.count()+\
                                         Howtos.published.count()+ Celeb.published.count()+\
                                         Loves.published.count()+ Campuss.published.count()+\
                                         Personalities.published.count()+ Events.published.count()+\
                                         Crimes.draft.count()+ Business.draft.count()+\
                                          Political.draft.count() + Entertainments.draft.count()+\
                                         Internationals.draft.count() + Educations.draft.count()+\
                                         Science_AND_Techs.draft.count() + Sports.draft.count()+\
                                         Healths.draft.count() + Political_Articless.draft.count()+\
                                         Happenings.draft.count() + Innovative_Articles.draft.count()+\
                                         Lifestyle_Articles.draft.count() + Religion_Articles.draft.count()+\
                                         Sport_Articles.draft.count() + Cultures.draft.count()+\
                                         Foods.draft.count() + Business_Articles.draft.count()+ Howtos.draft.count() + Celeb.draft.count()+\
                                         Loves.draft.count() + Campuss.draft.count()+\
                                         Personalities.draft.count() + Events.draft.count()
                                          
                                          
                                          
                                          
                                          
   