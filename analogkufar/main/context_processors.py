from .forms import TitleSearchForm

def title_search_form(request):
    search_form = TitleSearchForm(request.GET)
    return {'title_search_form': search_form}