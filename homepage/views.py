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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm, NewsLetterForm
from queryset_sequence import QuerySetSequence
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from users.models import SubscribedUsers
from functools import reduce





def homepage(request, template='home.html'):
   business_posts = businesses_posts(request)
   politics_posts = political_posts(request)
   context = {
            'politics_posts': politics_posts,
            'business_posts':business_posts, 
            'crime_posts':Crimes.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'entertainment_posts':Entertainments.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5],
            'international_posts':Internationals.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5],
            'education_posts':Educations.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'st_posts':Science_AND_Techs.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'sport_posts':Sports.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
             'health_posts':Healths.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
             'political_posts':Political_Articless.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
             'happenings_posts':Happenings.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
             'innovation_posts':Innovative_Articles.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
             'lifestyle_posts':Lifestyle_Articles.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
             'religion_posts':Religion_Articles.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
             'sports_posts':Sport_Articles.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'culture_posts':Cultures.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'food_posts':Foods.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'business_article_posts':Business_Articles.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'howto_posts':Howtos.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'celebrity_posts':Celeb.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'love_posts':Loves.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'campus_posts':Campuss.published.select_related('author').defer('body', 'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'personality_posts':Personalities.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            'event_posts':Events.published.select_related('author').defer('body',  'caption', 'created', 'updated', 'edited', 'status', 'tags').all()[:5], 
            }
  
   return render(request, template, context)

#Business post
def list_load_business_posts_view(request):
   business_posts = businesses_posts(request)
   context = {'business_posts':business_posts}
   return render(request, "homepage/partials/all_business_posts.html", context)

def businesses_posts(request):
   objs = Business.published.select_related('author').all()[:5]
   page_number = request.GET.get('page', 1)
   paginator = Paginator(objs, per_page=15)
   page_objects = paginator.get_page(page_number)
   return page_objects


#politics post
def list_load_politics_posts_view(request):
   politics_posts = political_posts(request)
   context = {'politics_posts':politics_posts}
   return render(request, "homepage/partials/all_politics_posts.html", context)

def political_posts(request):
   objs = Political.published.select_related('author').all()[:5]
   page_number = request.GET.get('page', 1)
   paginator = Paginator(objs, per_page=15)
   page_objects = paginator.get_page(page_number)
   return page_objects


def search_view(request):
   all_queryset = reduce(QuerySetSequence, [Crimes.published.select_related('author').all(), Business.published.select_related('author').all(),
                                         Political.published.select_related('author').all(), Entertainments.published.select_related('author').all(),
                                         Internationals.published.select_related('author').all(),Educations.published.select_related('author').all(),
                                         Science_AND_Techs.published.select_related('author').all(), Sports.published.select_related('author').all(),
                                         Healths.published.select_related('author').all(), Political_Articless.published.select_related('author').all(),
                                         Happenings.published.select_related('author').all(), Innovative_Articles.published.select_related('author').all(),
                                         Lifestyle_Articles.published.select_related('author').all(), Religion_Articles.published.select_related('author').all(),
                                         Sport_Articles.published.select_related('author').all(), Cultures.published.select_related('author').all(),
                                         Foods.published.select_related('author').all(), Business_Articles.published.select_related('author').all(),
                                         Howtos.published.select_related('author').all(), Celeb.published.select_related('author').all(),
                                         Loves.published.select_related('author').all(), Campuss.published.select_related('author').all(),
                                         Personalities.published.select_related('author').all(), Events.published.select_related('author').all() ])
   context = {'count': all_queryset.count()}
   return render(request, 'homepage/search/search.html', context)

def search_results_view(request):
   query = request.GET.get('search', '')
   print(f'{query =}')

   all_queryset = reduce(QuerySetSequence, [Crimes.published.select_related('author').all(), Business.published.select_related('author').all(),
                                         Political.published.select_related('author').all(), Entertainments.published.select_related('author').all(),
                                         Internationals.published.select_related('author').all(),Educations.published.select_related('author').all(),
                                         Science_AND_Techs.published.select_related('author').all(), Sports.published.select_related('author').all(),
                                         Healths.published.select_related('author').all(), Political_Articless.published.select_related('author').all(),
                                         Happenings.published.select_related('author').all(), Innovative_Articles.published.select_related('author').all(),
                                         Lifestyle_Articles.published.select_related('author').all(), Religion_Articles.published.select_related('author').all(),
                                         Sport_Articles.published.select_related('author').all(), Cultures.published.select_related('author').all(),
                                         Foods.published.select_related('author').all(), Business_Articles.published.select_related('author').all(),
                                         Howtos.published.select_related('author').all(), Celeb.published.select_related('author').all(),
                                         Loves.published.select_related('author').all(), Campuss.published.select_related('author').all(),
                                         Personalities.published.select_related('author').all(), Events.published.select_related('author').all() ])
   if query:
      search_vector = SearchVector('title', 'body')
      search_query = SearchQuery(query)
      results = all_queryset.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
   else:
      results = []

   context = {'results': results,
              'count': all_queryset.count()}
   return render(request, 'homepage/search/search_results.html', context)


@user_passes_test(lambda u: u.is_staff)
def newsLetter(request):
   if request.method == 'POST':
      form = NewsLetterForm(request.POST)
      if form.is_valid():
         subject = form.cleaned_data.get('subject')
         receivers = form.cleaned_data.get('receivers').split(',')
         email_message = form.cleaned_data.get('message')
         mail = EmailMessage(subject, email_message, f"Converse<{request.user.email}>", bcc=receivers)
         mail.content_subtype = "html"
         if mail.send():
            messages.success(request, "Email sent successfully")
         else:
            messages.error(request, "There was an error sending email")
      else:
         for error in list(form.errors.values()):
            messages.error(request, error)
      return redirect('/')
   form = NewsLetterForm()
   form.fields['receivers'].initial = ','.join([active.email 
                                               for active in SubscribedUsers.objects.all()] ) 
   return render(request=request, template_name='homepage/newsletter.html', context={'form':form})
