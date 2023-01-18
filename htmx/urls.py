from django.urls import path
from . import views

app_name = 'htmx'
urlpatterns = [
    path('', views.home, name='home'),
    path('gini/', views.gini, name='gini'),
    path('cpi/', views.cpi, name='cpi'),
    path('stock/', views.stock, name='stock'),
]

handler404 ='htmx.views.page_not_found'
handler500 ='htmx.views.server_error'