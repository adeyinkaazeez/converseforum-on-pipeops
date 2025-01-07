from django import forms
from tinymce.widgets import TinyMCE


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 'placeholder':'Input Keyword to search this forum',
                                                                 'rows':2})) 

    


class NewsLetterForm(forms.Form):
    subject = forms.CharField( widget=forms.TextInput(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 'placeholder':'Email subject',
                                                                 }))
    receivers = forms.CharField( widget=forms.TextInput(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 
                                                                 }))
    message = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 20}), label = "Email content")