from django.urls import path
from .views import (
    create_special_offer_view,
    manage_special_offers_view,
    create_event_view,
    manage_events_view,
    analyze_customer_data
)

urlpatterns = [
    path('create-special-offer/<int:restaurant_id>/', create_special_offer_view, name='create_special_offer'),
    path('manage-special-offers/<int:restaurant_id>/', manage_special_offers_view, name='manage_special_offers'),
    path('create-event/<int:restaurant_id>/', create_event_view, name='create_event'),
    path('manage-events/<int:restaurant_id>/', manage_events_view, name='manage_events'),
    path('analyze-customer-data/<int:pk>/', analyze_customer_data, name='analyze_customer_data'),
]