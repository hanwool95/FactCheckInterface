from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
    path('', views.index, name='index'),
    path('claim_current', views.claim_current, name='claim_current'),
    path('making_claim', views.making_claim, name='making_claim'),
    path('claim_detail/<int:claim_id>', views.claim_detail, name='claim_detail'),
    path('claim_delete/<int:claim_id>', views.claim_delete, name='claim_delete'),
    path('claim_update/<int:claim_id>', views.claim_update, name='claim_update'),
    path('claim_update_result/<int:claim_id>', views.claim_update_result, name='claim_update_result'),
    path('claim_results', views.claim_results, name='claim_results'),
    path('making_variation', views.making_variation, name='making_variation'),
    path('variation_results/<int:claim_id>/', views.variation_results, name='variation_results'),
]