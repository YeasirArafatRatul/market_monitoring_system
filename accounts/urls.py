from django.urls import path, include
from django.conf import settings


from accounts.views import *
from django.conf.urls.static import static

app_name = "accounts"


urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='home'),
   
    path('register/', UserRegisterView.as_view(),
         name='register'),

    path('login/', LoginView.as_view(),
         name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile/', profile,
         name='profile'),
    path('profile-update/', user_update,
         name='profile-update'),
    path('password-change', password_change, name='password-change'),

    path('users/<str:role>/', ListOfUsersView.as_view(), name='user-type-view'),

    path('user/profile/<int:id>', UserDetailView.as_view(),
         name='user-detail'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
