from django.urls import path
from . import views
app_name='accounts'
urlpatterns=[
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('urprofile/<int:user_id>',views.UserSelfProfileView.as_view(),name='urprofile'),
    path('reset/',views.UserPasswordResetView.as_view(),name='reset_password'),
    path('reset/done/',views.UserPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('confirm/<uidb64><token>',views.UserPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('confirm/complete/',views.UserPasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('unfollow/<int:user_id>/',views.UserUnfollowView.as_view(),name='unfollow'),
    path('follow/<int:user_id>/',views.UserFollowView.as_view(),name='follow'),
    path('edit/',views.UserEditView.as_view(),name='edit')


]