from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dev',views.dev, name="dev"),
    path('register',views.register, name="register"),
    path('display',views.display_ping_data, name="display"),
    path('upload',views.upload_csv, name="upload"),
    path('filter',views.ping_data_filter, name="filter"),
    path('graph',views.graph, name="graph"),
    path('report',views.report, name="report")

]