from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>', views.car, name='car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('myorders/', views.OrdersByUserListView.as_view(), name='my-orders'),
    path('myorders/<int:pk>', views.OrderByUserDetailView.as_view(), name='my-order'),
    path('myorders/new', views.OrderByUserCreateView.as_view(), name='my-orders-new'),
    path('myorders/<int:pk>/update', views.OrderByUserUpdateView.as_view(), name='my-order-update'),
    path('myorders/<int:pk>/delete', views.OrderByUserDeleteView.as_view(), name='my-order-delete'),
    path('myorders/orderline/<int:pk>', views.OrderLineByUserCreateView.as_view(), name='my-orderline'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]