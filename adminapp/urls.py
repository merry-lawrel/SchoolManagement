
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('staff/', StaffAPIView.as_view(), name='staff'),  # For GET and POST
    path('staff/<int:pk>/', StaffAPIView.as_view(), name='staff-detail'),  # For GET, PUT, DELETE on individual staff members
    path('librarian/', LibrarianAPIView.as_view(), name='librarian-list'),  # For GET and POST
    path('librarian/<int:pk>/', LibrarianAPIView.as_view(), name='librarian-detail'),  # For GET, PUT, DELETE on individual
    path('student/', StudentAPIView.as_view(), name='student-list'),  # For GET and POST
    path('student/<int:pk>/', StudentAPIView.as_view(), name='student-detail'),  # For GET, PUT, DELETE on individual
    path('libhistory/', LibraryHistoryAPIView.as_view(), name='libraryhistory'),  # For GET and POST
    path('libhistory/<int:pk>/', LibraryHistoryAPIView.as_view(), name='libraryhistory-detail'),  # For GET, PUT, DELETE on individual
    path('feerecords/', FeeRecordsAPIView.as_view(), name='feerecords-list'),  # For GET and POST
    path('feerecords/<int:pk>/', FeeRecordsAPIView.as_view(), name='feerecords-detail'),  # For GET, PUT, DELETE on individual
    path('loginAPI/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),

    # Frontend Pages
    path('', views.loginAPI, name='loginAPI'),
    path('index/', views.index, name='index'),
    path('viewstaff/', views.viewstaff, name='viewstaff'),
    path('addstaff/', views.addstaff, name='addstaff'),
    path('viewstudent/', views.viewstudent, name='viewstudent'),
    path('addstudent/', views.addstudent, name='addstudent'),
    path('viewlibrarians/', views.viewlibrarians, name='viewlibrarians'),
    path('addlibrarian/', views.addlibrarian, name='addlibrarian'),
    path('libraryhistory/', views.libraryhistory, name='libraryhistory'),
    path('fee/', views.fee, name='fee')
]