from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
    path('', views.index, name='index'),
    path('claim_current/<int:state>', views.claim_current, name='claim_current'),
    path('admin_current/', views.admin_current, name='admin_current'),
    path('all_current', views.all_current, name='all_current'),
    path('making_claim', views.making_claim, name='making_claim'),
    path('claim_detail/<int:claim_id>', views.claim_detail, name='claim_detail'),
    path('claim_delete/<int:claim_id>', views.claim_delete, name='claim_delete'),
    path('claim_update/<int:claim_id>', views.claim_update, name='claim_update'),
    path('claim_update_result/<int:claim_id>', views.claim_update_result, name='claim_update_result'),
    path('claim_results/<int:reference_id>', views.claim_results, name='claim_results'),
    path('making_variation', views.making_variation, name='making_variation'),
    path('making_paraphrased', views.making_paraphrased, name='making_paraphrased'),
    path('variation_results/<int:claim_id>/', views.variation_results, name='variation_results'),
    path('paraphrased_results/<int:claim_id>/', views.paraphrased_results, name='paraphrased_results'),
]