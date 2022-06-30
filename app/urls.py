from django.contrib import admin
from django.urls import path
from app import views
#for the slash error (404 page not found) refer the following site --> https://dev.to/learndjango/trailing-url-slashes-in-django-4bf#:~:text=Among%20Django's%20many%20built%2Din,to%20see%20this%20in%20action.
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup),
    path('add-todo/', views.add_todo),
    path('logout/', views.signout),
    path('delete-todo/<int:id>', views.delete_todo),
    path('change_status/<int:id>/<str:status>', views.change_status)
    
]