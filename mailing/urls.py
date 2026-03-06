from django.urls import path
from mailing.views import HomeView, SubscriberListView, SendingListView, SubscriberDetailView, SubscriberCreateView, \
    SubscriberUpdateView, SubscriberDeleteView, SendingDetailView, SendingCreateView, SendingUpdateView, \
    SendingDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    SendMessageView, SendAttemptListView

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients/', SubscriberListView.as_view(), name='subscribers_list'),
    path('client/<int:pk>/', SubscriberDetailView.as_view(), name='subscriber_detail'),
    path('client/create/', SubscriberCreateView.as_view(), name='subscriber_create'),
    path('client/<int:pk>/update/', SubscriberUpdateView.as_view(), name='subscriber_update'),
    path('client/<int:pk>/delete/', SubscriberDeleteView.as_view(), name='subscriber_delete'),

    path('sending/', SendingListView.as_view(), name='sending_list'),
    path('sending/<int:pk>/', SendingDetailView.as_view(), name='sending_detail'),
    path('sending/create/', SendingCreateView.as_view(), name='sending_create'),
    path('sending/<int:pk>/update/', SendingUpdateView.as_view(), name='sending_update'),
    path('sending/<int:pk>/delete/', SendingDeleteView.as_view(), name='sending_delete'),
    path('sending/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),

    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('report/', SendAttemptListView.as_view(), name='log_list'),
]