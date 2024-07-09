from django.urls import path

from booking.views import display_search_page, search_by_name, search_by_speciality, show_visit_times, \
    reserve_visit_times

urlpatterns = [
    path('search/', display_search_page, name='search_page'),
    path('search/name/', search_by_name, name='search_by_name'),
    path('search/speciality/', search_by_speciality, name='search_by_spec'),
    path('visit/time/', show_visit_times, name='visit_time'),
    path('reserve/time/', reserve_visit_times, name='reserve_visit_time')
]
