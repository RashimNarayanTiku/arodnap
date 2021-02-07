from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Entry
from datetime import date
import pytz
import random 
from django.conf import settings


class HomeView(View):
    def get(self, request):

        if(request.user.is_authenticated):
            
            entries = Entry.objects.filter(owner=request.user).filter(created_at__date=date.today()).order_by('-created_at')        
            
            local_timezone = pytz.timezone(settings.TIME_ZONE)
            for entry in entries:
                entry.created_at = entry.created_at.astimezone(local_timezone)
            ctx = {'entries' : entries}
            return render(request, 'main/home.html',ctx)
        return render(request, 'main/home.html')

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    success_url = reverse_lazy('main:home')
    template_name = 'main/entry_create.html'
    fields = ['title', 'text']

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy('main:home')
    template_name = "main/entry_delete.html"

    def test_func(self):
        entry = self.get_object()
        if self.request.user == entry.owner:
            return True
        return False

class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    success_url = reverse_lazy('main:home')
    template_name = "main/entry_update.html"
    fields = ['title', 'text']

    def test_func(self):
        entry = self.get_object()
        if self.request.user == entry.owner:
            return True
        return False


class BoxView(LoginRequiredMixin, View):

    def get(self, request):
        entries = Entry.objects.filter(owner=request.user)

        # if entries.count()!=0:
        ranges = range(0, entries.count())
        if ranges:
            random_id = random.choice(ranges)
            random_entry = entries[random_id]
        else:
            random_entry = None
        return render(request,'main/box.html',{'entry':random_entry})


