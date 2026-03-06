from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from mailing.forms import SendingForm, SubscriberForm, MessageForm
from mailing.models import Subscriber, Sending, Message, SendAttempt
from django.shortcuts import get_object_or_404, redirect


class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribers_count'] = Subscriber.objects.all().count()
        context['all_sending'] = Sending.objects.all().count()
        context['started_sending'] = Sending.objects.filter(status='started').count()
        return context


class SubscriberListView(ListView):
    model = Subscriber
    template_name = 'mailing/subscribers_list.html'
    context_object_name = 'subscribers'


class SubscriberCreateView(CreateView):
    model = Subscriber
    form_class = SubscriberForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:subscriber_detail', args=[self.object.pk])


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = 'mailing/subscriber_detail.html'
    context_object_name = 'subscriber'


class SubscriberUpdateView(UpdateView):
    model = Subscriber
    fields = ['email', 'full_name', 'comment', 'owner']

    def get_success_url(self):
        return reverse('mailing:subscriber_detail', args=[self.object.pk])


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    success_url = reverse_lazy('mailing:subscribers_list')


class SendingListView(ListView):
    model = Sending
    template_name = 'mailing/sending_list.html'
    context_object_name = 'sending'


class SendingDetailView(DetailView):
    model = Sending
    template_name = 'mailing/sending_detail.html'
    context_object_name = 'sending'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


class SendingCreateView(CreateView):
    model = Sending
    form_class = SendingForm

    def form_valid(self, form):
        form.instance.status = 'created'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:sending_detail', args=[self.object.pk])


class SendingUpdateView(UpdateView):
    model = Sending
    form_class = SendingForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj

    def get_success_url(self):
        return reverse('mailing:sending_detail', args=[self.object.pk])


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy('mailing:sending_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/messages_list.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_detail', args=[self.object.pk])


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_detail', args=[self.object.pk])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages_list')


class SendMessageView(View):
    def post(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)

        for subscriber in sending.subscribers.all():
            try:
                sending.send_mail(subscriber.email)
                SendAttempt.objects.create(status="successfully", response='Успешная отправка', sending=sending)
            except Exception as e:
                SendAttempt.objects.create(status="not_successfully", response=str(e), sending=sending)

        return redirect('mailing:sending_list')


class SendAttemptListView(ListView):
    model = SendAttempt
    template_name = 'mailing/log_list.html'
    context_object_name = 'logs'