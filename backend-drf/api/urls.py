from django.urls import path
from rest_framework.views import APIView
from users import views as UserViews
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from products import views as ProductViews
from carts import views as CartViews
from orders import views as OrderViews


urlpatterns = [
    path('register/',UserViews.RegisterView.as_view()),

    # User APIs------
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path ('profile/', UserViews.ProfileView.as_view()),

    # Products APIs------

    #Product list
    path('products/', ProductViews.ProductListView.as_view()),

    #Product details
    path('products/<int:pk>/', ProductViews.ProductDetailView.as_view()),

    # Cart APIs-------
    path('carts/',CartViews.CartView.as_view()),

    # Add to cart
    path('carts/add/',CartViews.AddToCartView.as_view()),

    # Manage cart
    path('carts/items/<int:item_id>/',CartViews.ManageCartItemView.as_view()),

    # Orders
    path('orders/place/',OrderViews.PlaceOrderView.as_view()),
    path('orders/',OrderViews.MyOrderView.as_view()),  
    path('orders/<int:pk>/',OrderViews.OrderDetailView.as_view()),

]