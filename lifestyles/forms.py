from django import forms
from .models import Lifestyles_Comment, Lifestyle_Articles

class CommentForm(forms.ModelForm):
    class Meta:
      model = Lifestyles_Comment    
      fields = ['body', 'comment_image_one', 'comment_image_two']
      
        
class PostForm(forms.ModelForm):
    news_image = forms.ImageField(required=True)
    class Meta:
      model = Lifestyle_Articles
      fields = [ 'title' , 'tags','news_image', 'caption', 'body', 'news_image_two', 'caption_two', 'news_image_three', 'caption_three', 'news_image_four', 'caption_four']
      widgets = {
          'caption' : forms.widgets.TextInput(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 'placeholder':'Brief Decription of Photo Above',}),
          'caption_two':forms.widgets.Textarea(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white mb-10', 'placeholder':'Use for Detailed Description of image_two if their is any',
                                                             'cols': 300, 'rows': 2}),
          'caption_three':forms.widgets.Textarea(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white mb-10', 'placeholder':'Use for Detailed Description of image_three if their is any',
                                                             'cols': 300, 'rows': 2}),
           'caption_four':forms.widgets.Textarea(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white mb-10', 'placeholder':'Use for Detailed Description of image_four if their is any',
                                                             'cols': 300, 'rows': 2}),
                  }  

class EmailPostForm(forms.Form): 
    
    name = forms.CharField(required=False, 
                               widget=forms.TextInput(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 'placeholder':'Input your name',
                                                                 'rows':2}))  
      
    to = forms.EmailField()    
    comments = forms.CharField(required=False, 
                               widget=forms.Textarea(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 'placeholder':'Drop comment',
                                                                'cols': 15, 'rows':4}))