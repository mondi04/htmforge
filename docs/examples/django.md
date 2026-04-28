# Django example

This is a minimal sketch showing how to use `to_django()` and `Page` in a Django view.

```python
# views.py
from django.http import HttpResponse
from htmforge.components.page import Page

class UsersPage(Page):
    def _body_content(self):
        return []

def users(request):
    page = UsersPage(title="Users")
    return HttpResponse(page.to_html())
```

In `urls.py` add:

```python
from django.urls import path
from .views import users

urlpatterns = [path('users/', users)]
```

Note: full Django project setup omitted; focus is on usage of htmforge within views.
