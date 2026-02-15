
import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from blog.forms import PostForm
from taggit.forms import TagWidget

def verify():
    form = PostForm()
    widget = form.fields['tags'].widget
    print(f"Widget for 'tags': {widget}")
    
    if isinstance(widget, TagWidget):
        print("SUCCESS: 'tags' field is using TagWidget.")
    else:
        print(f"FAILURE: 'tags' field is NOT using TagWidget. It is using {type(widget)}")

if __name__ == "__main__":
    verify()
