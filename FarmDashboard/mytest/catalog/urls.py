from django.urls import path
from . import views
from django.urls import include # add by myself


urlpatterns = [
    path('hello_world/', views.hello_world), # add by myself
    path('SimpleExample/<str:filedname>', views.SimpleExample), # add by myself
    path('django_plotly_dash/', include('django_plotly_dash.urls')), # add by myself
]