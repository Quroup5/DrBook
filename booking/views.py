from django.shortcuts import render


# Create your views here.
def display_search_page(request):
    return render(request, template_name="booking/search.html")

def search_by_name(request):
    pass

def search_by_speciality(request):
    pass
