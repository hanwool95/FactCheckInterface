from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
    path('', views.index, name='index'),
    path('making_claim', views.making_claim, name='making_claim'),
    path('claim_results', views.claim_results, name='claim_results'),
    path('making_variation', views.making_variation, name='making_variation'),
    path('variation_results/<int:claim_id>/', views.variation_results, name='variation_results'),
]