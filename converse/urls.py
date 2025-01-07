"""
URL configuration for converse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from homepage.sitemaps import PostSitemap


sitemaps = {
'posts': PostSitemap,
}

urlpatterns = [
     path('sTaFfOnLy/', admin.site.urls),
     path("", include('homepage.urls')),
     path('business/', include('business.urls')),
     path('business_article/', include('business__articles.urls')),
     path('campus/', include('campuss.urls')),
     path('celebrity/', include('celeb.urls')),
     path('crime/', include('crimes.urls')),
     path('culture/', include('cultures.urls')),
     path('education/', include('educations.urls')),
     path('event/', include('events.urls')),
     path('food/', include('foods.urls')),
     path('entertainment/', include('entertainments.urls')),
     path('happening/', include('happening.urls')),
     path('health/', include('health_articles.urls')),
     path('how-to/', include('howtos.urls')),
     path('innovation/', include('innovations.urls')),
     path('international/', include('internationals.urls')),
     path('lifestyle/', include('lifestyles.urls')),
     path('love/', include('loves.urls')),
     path('politics/', include('newss.urls')),
     path('personality/', include('personalitys.urls')),
     path('political_article/', include('political_articles.urls')),
     path('religion/',include('religions.urls')),
     path('science/', include('sciences.urls')),
     path('sport/', include('sports.urls')),
     path('sport_article/', include('sport_articles.urls')),
     path('users/', include('users.urls')),
    
     path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, 
          name='django.contrib.sitemaps.views.sitemap'),
     path('social-auth/', include('social_django.urls', namespace='social')),
     path("", include('pwa.urls')),
     path('message', include('postman.urls'), name='postman'),
    path('prose/', include('prose.urls')),
    
]
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
