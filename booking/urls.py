from django.urls import path

from booking.views import display_search_page, search_by_name, search_by_speciality, show_visit_times, \
    reserve_visit_times, check_visit_times, show_reservations, add_comment, display_past_visit_times, save_comment

urlpatterns = [
    path('show/reservations/', show_reservations, name='show_reservations'),
    path('search/', display_search_page, name='search_page'),
    path('search/name/', search_by_name, name='search_by_name'),
    path('search/speciality/', search_by_speciality, name='search_by_spec'),
    path('visit/time/', show_visit_times, name='visit_time'),
    path('check/time/', check_visit_times, name='check_visit_time'),
    path('reserve/time/', reserve_visit_times, name='reserve_visit_time'),
    path('visit/time/past/display', display_past_visit_times, name='display_past_visit_times'),
    path('visit/time/addcomment', add_comment, name='add_comment'),
    path('visit/time/savecomment', save_comment, name='save_comment'),
]
