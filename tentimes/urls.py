from django.urls import path
from tentimes import views

urlpatterns=[
    path('export/', views.export_to_csv, name='export_to_csv'),
    path("",views.news_list,name='news_list'),
]

