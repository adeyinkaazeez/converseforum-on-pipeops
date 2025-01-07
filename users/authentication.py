from django.contrib.auth import get_user_model
from .models import Profile

class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None

        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
def create_profile(backend, user, *args, **kwargs):
        # Create user profile for social authentication
        Profile.objects.get_or_create(user=user) 

def save_profile(backend, user, response, is_new=False, *args, **kwargs ):
    if is_new and backend.name =="facebook":
        Profile.objects.filter(owner=user).update(imageUrl = "https://graph.facebook.com/{0}/picture/?type=large&access_token={1}".format(response['id'],
                                                 response['access_token'])) 