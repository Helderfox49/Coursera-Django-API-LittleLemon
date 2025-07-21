from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.menu_items, name='menu_items'),
    path('single-item/<int:id>', views.single_item, name='single_item'),
    # path('menu-items', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
]
