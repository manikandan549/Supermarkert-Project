from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import total_shampoo_sales_last_7_daysView,get_high_value_purchasesView,get_total_items_purchasedView,ProductUpdateView
from .views import RegisterView,loginView,UserView,logoutView,make_purchase_stock,PurchaseView,UserUpdateView,ProductViewset
from .views import StoreuserregisterView,StoreuserloginView,StoreuserView,StoreuserlogoutView


router = DefaultRouter()
router.register(r'products', views.ProductViewset)


urlpatterns = [
    path('', include(router.urls)),

    path('UserRegister/',RegisterView.as_view()),
    path('Userlogin/',loginView.as_view()),
    path('current_token_user_details/',UserView.as_view()),
    path('Userlogout/',logoutView.as_view()),
    path('StoreuserRegister/',StoreuserregisterView.as_view()),
    path('Storeuserlogin/',StoreuserloginView.as_view()),
    path('current_token_Storeuser_details/',StoreuserView.as_view()),
    path('Storeuserlogout/',StoreuserlogoutView.as_view()),
    path('Purchase/',PurchaseView.as_view()),
    path('total_shampoo_sales_last_7_days/',total_shampoo_sales_last_7_daysView.as_view()),
    path('get_high_value_purchases/',get_high_value_purchasesView.as_view()),
    path('get_total_items_purchased/<str:start_date>/<str:end_date>/',get_total_items_purchasedView.as_view()),
    path('products/<int:product_id>/',ProductUpdateView.as_view()),
    path('User/<int:id>/',UserUpdateView.as_view()),
    # path('products/',ProductViewset.as_view()),

    path('make_purchase_with_stock_update/', make_purchase_stock, name='make_purchase_with_stock_update'),# this code working
    # path('User/<int:id>/', UserUpdateView.as_view(), name='User-details-update'),# this code working
]