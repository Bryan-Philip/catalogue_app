from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.auction_years, name='auction-years'),
    path('upload_allocations', views.upload_allocations, name='upload_allocations'),
    path('upload_sale', views.upload_sale, name='upload_sale'),
    path('update_allocation', views.update_allocation, name='update_allocation'),
    path('update_sale', views.update_sale, name='update_sale'),
    path('generate_catalogue', views.generate_catalogue_data, name='generate_catalogue_data'),
    path('generate_invoices', views.generate_invoices_data, name='generate_invoices_data'),
    path('generate_account_sales', views.generate_account_sales_data, name='generate_account_sales_data'),
    path('auctions/', views.auction_years, name='auction-years'),
    path('auctions/<int:year>/', views.auctions_display, name='auctions-display'),
    path('auctions/<int:year>/<str:number>/', views.auction_view, name='auction-dashboard'),
    path('auctions/<int:year>/<str:number>/documents/', views.auction_view, name='auction-documents'),
    path('auctions/<int:year>/<str:number>/catalogue/', views.auction_view, name='auction-catalogue'),
    path('auctions/<int:year>/<str:number>/invoices/', views.auction_view, name='auction-invoices'),
    path('auctions/<int:year>/<str:number>/allocations/', views.auction_view, name='auction-allocations'),
    path('auctions/<int:year>/<str:number>/generate_catalogue/', views.generate_catalogue, name='generate-catalogue'),
    path('auctions/<int:year>/<str:number>/generate_invoices/', views.generate_invoices, name='generate-invoices'),
    path('auctions/<int:year>/<str:number>/generate_account_sales/', views.generate_account_sales, name='generate-account-sales'),
    path('download', views.download_zipped, name='download'),
]
