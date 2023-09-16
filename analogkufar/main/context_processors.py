from .forms import TitleSearchForm
from django.contrib.auth import get_user

def current_user(request):
    user = get_user(request)
    return {'current_user': user}
def title_search_form(request):
    search_form = TitleSearchForm(request.GET)
    return {'title_search_form': search_form}