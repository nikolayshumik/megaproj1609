from django.urls import path
from . import views
from .views import register_view
from django.conf import settings
from django.conf.urls.static import static
from .views import ad_details
from .views import ContactView

urlpatterns = [
                  path('', views.index, name='home'),

                  path('basket', views.basket, name='basket'),
                  path('test', views.test, name='test'),
                  path('postads', views.postads, name='postads'),
                  path('profile', views.profile, name='profile'),
                  path('buy', views.buy, name='buy'),
                  path('profile/edit/', views.edit_profile, name='profiles_edit'),
                  path('profiles', views.profiles, name='profiles'),
                  path('register/', register_view, name='register'),
                  path('delete-from-basket/', views.delete_from_basket, name='delete_from_basket'),
                  path('details/', views.details, name='details'),
                  path('myads', views.myads, name='myads'),
                  path('myads/<int:ad_id>/', ad_details, name='ad_details'),
                  path('celery', views.celery, name='celery'),
                  path('create/', views.create_order, name='create_order'),
                  path('confirmation/', views.order_confirmation, name='confirmation'),
                  path('contact/', ContactView.as_view(), name='contact'),
                  path('edit_ad/<int:ad_id>', views.edit_ad, name='edit_ad'),
                  path('delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),
                  path('seller/<int:user_id>/', views.seller_profile, name='seller_profile'),
                  # path('user-list/', views.user_list, name='user_list'),
                  path('compose/<int:user_id>/', views.compose_message, name='compose_message'),
                  path('submit_order/', views.submit_order, name='submit_order'),
                  path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
                  path('online_payment/', views.online_payment, name='online_payment'),
                  path('user-list/<int:user_id>/', views.user_list, name='user_list'),
                  path('support/', views.support, name='support'),
                  path('email_sent/', views.email_sent, name='email_sent'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
