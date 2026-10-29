from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.ApiRootView.as_view(), name='root'),
    path('site/', views.SiteView.as_view(), name='site'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('enquiries/', views.EnquiryView.as_view(), name='enquiries'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
]
