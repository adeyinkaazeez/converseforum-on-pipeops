from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .decorators import user_not_authenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, LoginForm, SetPasswordForm, UserEditForm, ProfileEditForm, PasswordResetRequestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, SubscribedUsers
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import  render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.validators import  EmailValidator, validate_email
from django.shortcuts import HttpResponseRedirect
from queryset_sequence import QuerySetSequence
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




# We want to create context menu for all the post section for each author

from newss.models import Political, Politics_Comments
from business.models import Business, Business_Comment
from crimes.models import Crimes, Crimes_News_Comment
from entertainments.models import Entertainments, Entertainments_Comment
from internationals.models import Internationals, Internationals_Comment
from educations.models import Educations, Educations_Comment
from sciences.models import Science_AND_Techs, Science_and_Tech_Comments
from sports.models import Sports,  Sport_Comments
from health_articles.models import Healths, Healths_Comment
from political_articles.models import Political_Articless, Political_Comments
from happening.models import Happenings,  Happenings_Comment
from innovations.models import Innovative_Articles, Innovatives_Comment
from lifestyles.models import Lifestyle_Articles, Lifestyles_Comment
from religions.models import Religion_Articles,  Religion_Comments
from sport_articles.models import Sport_Articles, Sport_Article_Comments
from cultures.models import Cultures, Cultures_Comment
from foods.models import Foods, Foods_Comment
from business__articles.models import Business_Articles, Business_Articles_Comment
from howtos.models import Howtos, Howtos_Comment
from celeb.models import Celeb, Celeb_Comment
from loves.models import Loves, Love_Comments
from campuss.models import Campuss, Campuss_Comment
from personalitys.models import Personalities, Personality_Comments
from events.models import Events, Events_Comment

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact
from actions.utils import create_action
from actions.models import Action
from notify.signals import notify

# Create your views here.

def register(request):  
    if request.method == 'POST':  
        form = UserRegistrationForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save() 
            Profile.objects.create(user=user) 
            create_action(user, 'has created an account')
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'New Regitration Activation Link '  
            message = render_to_string('template_activate_account.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':default_token_generator.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            if email.send():  
                messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on\
                                 received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')  
                return redirect('homepage')
            else:
                message.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
    else:  
        form = UserRegistrationForm()  
    return render(request, 'register.html', {'form': form})  

#when aspiring user registered and activation link sent to the email address
#This function is triggered when the user click on the activation link
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and default_token_generator.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request, 'Thank you for your email confirmation. You can now login to your account.') 
        return redirect('login') 
    else:  
        messages.error(request, 'Activation link is invalid!')
        return redirect('dashboard') 


def user_login(request):
    next  = request.POST.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'],
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Authenticated successfully')
                    create_action(request.user, 'signed-in')
                    return HttpResponseRedirect(next)
                    #return redirect('dashboard')
                else:
                    messages.error('Disabled account')
            else:
                messages.error(request, 'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
   next  = request.POST.get('next', '/')
   logout(request)
   return HttpResponseRedirect(next)
   #return redirect('homepage')
   #return render(request, 'users/logged_out.html') 



@login_required
def dashboard(request):
    return render(request, 'home.html',
                           {'section': 'dashboard'})


def password_change_view(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully")
            return redirect('login')
            
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'users/password_change_form.html', {'form': form})

def PasswordChangeDoneView(request):
   
   return render(request, 'registration/password_change_done.html') 


@login_required
def edit(request):
    edited = False
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            edited = True
            #messages.success(request, 'Your Profile was updated successfully')
            #return redirect('dashboard')
            return render(request,'users/edit_confirm.html')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,'users/edit.html',
                            {'user_form': user_form,
                             'profile_form': profile_form}) 


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/forgot_password_form.html"
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')

def my_activities(request, template='myactivities.html'):
    user = request.user
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
        .prefetch_related('target')[:10]

     #retireving comments made on each post by users. 
     # this will be display immediately a user clicked on his/her profile webpage
    all_my_comment = my_commenting_activities(request)
    #retrieving all post by the
    all_my_posting = my_posting_activities(request)

   
    context = {
         "all_my_comment": all_my_comment,
         "all_my_posting": all_my_posting,
         'actions':actions,
       }
    
    return render(request, template,  context, )

def load_all_my_commenting_activites(request):
    all_my_comment = my_commenting_activities(request)
    context = {"all_my_comment": all_my_comment}
    return render(request, "users/partials/all_my_commenting_activities.html", context)

def my_commenting_activities(request):
    all_comment = QuerySetSequence(Business_Comment.objects.filter(name= request.user).order_by('-created'),
        Business_Articles_Comment.objects.filter(name= request.user).order_by('-created'),
        Crimes_News_Comment.objects.filter(name= request.user).order_by('-created'),
        Entertainments_Comment.objects.filter(name= request.user).order_by('-created'),
        Internationals_Comment.objects.filter(name= request.user).order_by('-created'),
        Educations_Comment.objects.filter(name= request.user).order_by('-created'),
        Science_and_Tech_Comments.objects.filter(name= request.user).order_by('-created'),
        Sport_Comments.objects.filter(name= request.user).order_by('-created'),
        Healths_Comment.objects.filter(name= request.user).order_by('-created'),
        Political_Comments.objects.filter(name= request.user).order_by('-created'),
        Happenings_Comment.objects.filter(name= request.user).order_by('-created'),
        Innovatives_Comment.objects.filter(name= request.user).order_by('-created'),
        Lifestyles_Comment.objects.filter(name= request.user).order_by('-created'),
        Religion_Comments.objects.filter(name= request.user).order_by('-created'),
        Sport_Article_Comments.objects.filter(name= request.user).order_by('-created'),
        Cultures_Comment.objects.filter(name= request.user).order_by('-created'),
        Foods_Comment.objects.filter(name= request.user).order_by('-created'),
        Business_Articles_Comment.objects.filter(name= request.user).order_by('-created'),
        Howtos_Comment.objects.filter(name= request.user).order_by('-created'),
        Celeb_Comment.objects.filter(name= request.user).order_by('-created'),
        Love_Comments.objects.filter(name= request.user).order_by('-created'),
        Campuss_Comment.objects.filter(name= request.user).order_by('-created'),
        Personality_Comments.objects.filter(name= request.user).order_by('-created'),
        Politics_Comments.objects.filter(name= request.user).order_by('-created'),
        Events_Comment.objects.filter(name= request.user).order_by('-created'),).order_by('-created')
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(all_comment, per_page=10)
    page_objects_home = paginator.get_page(page_number)
    return page_objects_home

def load_all_my_posting_activities(request):
    all_my_posting = my_posting_activities(request)
    context = {"all_my_posting": all_my_posting}
    return render(request, "users/partials/all_my_posting.html", context)

def my_posting_activities(request):
    all_queryset = QuerySetSequence(
        Business.objects.filter(author= request.user).order_by('-publish'),
        Business_Articles.objects.filter(author= request.user).order_by('-publish'),
        Crimes.objects.filter(author= request.user).order_by('-publish'),
        Entertainments.objects.filter(author= request.user).order_by('-publish'),
        Internationals.objects.filter(author= request.user).order_by('-publish'),
        Educations.objects.filter(author= request.user).order_by('-publish'),
        Science_AND_Techs.objects.filter(author= request.user).order_by('-publish'),
        Sports.objects.filter(author= request.user).order_by('-publish'),
        Healths.objects.filter(author= request.user).order_by('-publish'),
        Political_Articless.objects.filter(author= request.user).order_by('-publish'),
        Happenings.objects.filter(author= request.user).order_by('-publish'),
        Innovative_Articles.objects.filter(author= request.user).order_by('-publish'),
        Lifestyle_Articles.objects.filter(author= request.user).order_by('-publish'),
        Religion_Articles.objects.filter(author= request.user).order_by('-publish'),
        Sport_Articles.objects.filter(author= request.user).order_by('-publish'),
        Cultures.objects.filter(author= request.user).order_by('-publish'),
        Foods.objects.filter(author= request.user).order_by('-publish'),
        Business_Articles.objects.filter(author= request.user).order_by('-publish'),
        Howtos.objects.filter(author= request.user).order_by('-publish'),
        Celeb.objects.filter(author= request.user).order_by('-publish'),
        Loves.objects.filter(author= request.user).order_by('-publish'),
        Campuss.objects.filter(author= request.user).order_by('-publish'),
        Personalities.objects.filter(author= request.user).order_by('-publish'),
        Political.objects.filter(author= request.user).order_by('-created'),
        Political_Articless.objects.filter(author= request.user).order_by('-created'),
        Events.objects.filter(author= request.user).order_by('-publish'),
    ).order_by('-publish')

    page_number = request.GET.get('page', 1)
    paginator = Paginator(all_queryset, per_page=10)
    page_objects_home = paginator.get_page(page_number)
    return page_objects_home




def Subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)

        if not name and email:
            messages.error(request, "valid name and email required to subscribe")
            return redirect("/")
        
        subscribe_user = SubscribedUsers.objects.filter(email=email).first()

        if subscribe_user:
            messages.error(request, f"{email} email address is already a subscriber")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")
        
        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.name = name
        subscribe_model_instance.email = email
        subscribe_model_instance.save()

        messages.success(request, f"{email} email was successfully subscribed to our newsletter")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    
"""Both Anonymous and Login users can actually check 
   an author profile from post list view on the homepage
   or on post detail"""
@login_required
def Author_Profile_View(request, pk, target=None):
    User = get_user_model()
    author = get_object_or_404(User, id=pk)
    all_queryset = QuerySetSequence(Business.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Business_Articles.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Crimes.objects.filter(author= pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Entertainments.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes',),
                                    Internationals.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Educations.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Science_AND_Techs.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes',),
                                    Sports.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Healths.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Political_Articless.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Happenings.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Innovative_Articles.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Lifestyle_Articles.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Religion_Articles.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Sport_Articles.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Cultures.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Foods.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Business_Articles.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Howtos.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Celeb.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Loves.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Campuss.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Personalities.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes',),
                                    Events.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Political.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    Political_Articless.objects.filter(author=pk).defer('tags', 'body', 'created', 'updated', 'edited', 'status',  'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four', 'likes', ),
                                    ).order_by('-publish')
    #let's paginate our author's post to 20 posts per post
    paginator= Paginator(all_queryset, 20) #20 posts per page
    page_number= request.GET.get('page', 1)
     
    try:
       all_queryset_post= paginator.page(page_number)
    except PageNotAnInteger:
       all_queryset_post= paginator.page(1)
    except EmptyPage:
      all_queryset_post = paginator.page(paginator.num_pages) 
    context = {
         'all_queryset_post': all_queryset_post,
         'author': get_object_or_404(User, pk=pk),
    }
    
    #create_action(request.user, 'viewed profile of', author)
    notify.send(request.user, recipient=author, actor=request.user, verb='Viewed your profile',
                nf_type = 'followed_by_one_user')
    return render(request, 'users/author_page.html', context)

#Searching for authors with their username. 
# Only login user can search for author
@login_required
def search_for_author(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'user/search_user.html', {'author':author})






    
@login_required
def user_to_follow(request, id):
    User = get_user_model()
    author = get_object_or_404(User, id=id)
    if request.method =='POST':
        if not request.user.following.filter(id=id).exists():
            Contact.objects.create(user_from=request.user, user_to=author)
            create_action(request.user, 'is following', author)
            return render(request, 'users/partials/followers.html', context={'author':author})
        else:
            Contact.objects.filter(user_from=request.user, user_to=author).delete()
            create_action(request.user, 'has un-follow', author)
            return render(request, 'users/partials/followers.html', context={'author':author})





