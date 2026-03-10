from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing.forms import MessageForm, SendingForm, SubscriberForm
from mailing.models import Message, SendAttempt, Sending, Subscriber


class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscribers_count"] = Subscriber.objects.all().count()
        context["all_sending"] = Sending.objects.all().count()
        context["started_sending"] = Sending.objects.filter(status="started").count()
        return context


class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber
    template_name = "mailing/subscribers_list.html"
    context_object_name = "subscribers"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Managers").exists():
            return Subscriber.objects.all()
        return Subscriber.objects.filter(owner=self.request.user)


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailing:subscriber_detail", args=[self.object.pk])


class SubscriberDetailView(LoginRequiredMixin, DetailView):
    model = Subscriber
    template_name = "mailing/subscriber_detail.html"
    context_object_name = "subscriber"


class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscriber
    fields = ["email", "full_name", "comment", "owner"]

    def get_success_url(self):
        return reverse("mailing:subscriber_detail", args=[self.object.pk])


class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    model = Subscriber
    success_url = reverse_lazy("mailing:subscribers_list")


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = "mailing/sending_list.html"
    context_object_name = "sending"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Managers").exists():
            return Sending.objects.all()
        return Sending.objects.filter(owner=self.request.user)


class SendingDetailView(LoginRequiredMixin, DetailView):
    model = Sending
    template_name = "mailing/sending_detail.html"
    context_object_name = "sending"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm

    def form_valid(self, form):
        form.instance.status = "created"
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailing:sending_detail", args=[self.object.pk])


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj

    def get_success_url(self):
        return reverse("mailing:sending_detail", args=[self.object.pk])


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sending
    success_url = reverse_lazy("mailing:sending_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Managers").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_detail.html"
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailing:message_detail", args=[self.object.pk])


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse("mailing:message_detail", args=[self.object.pk])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:messages_list")


class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)

        for subscriber in sending.subscribers.all():
            try:
                sending.send_mail(subscriber.email)
                SendAttempt.objects.create(status="successfully", response="Успешная отправка", sending=sending)
            except Exception as e:
                SendAttempt.objects.create(status="not_successfully", response=str(e), sending=sending)

        return redirect("mailing:sending_list")


class SendAttemptListView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/log_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logs = [x for x in SendAttempt.objects.all() if x.sending.owner == self.request.user]
        context["logs"] = logs
        return context
