from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name="login"),
    path('logout', views.CustomLogoutView.as_view(), name="logout"),
    path('register', views.CustomRegisterView.as_view(), name="register"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('', views.IndexView.as_view(), name='index'),
    path('polls/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
]