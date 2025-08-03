from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('secret', views.secret),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  
    path('me/', views.me, name='me'),  
    path('manager_view/', views.manager_view, name='manager-view'),  
    path('throttle_check/', views.throttle_check, name='throttle-check'),  
    path('throttle_check_auth/', views.throttle_check_auth, name='throttle_check'),  
    
    # path('menu-items/', views.menu_items, name='menu_items'),
    # path('single-item/<int:id>', views.single_item, name='single_item'),

    # path('menu-items', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),

]
