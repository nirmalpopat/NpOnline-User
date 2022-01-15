from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Stock, Sells
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SellsForm
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                )
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.core.mail import send_mail
import pytz
from django.utils.timezone import localtime, now
from django.utils import timezone
from django.db.models import Sum, Count
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
# timezone.activate(pytz.timezone("Asia/Kolkata")) 
# from django.utils import timezone
# timezone.localtime(timezone.now())


class AddSell(LoginRequiredMixin, FormView):
    login_url = '/accounts/login/'
    template_name = 'AddSell.html'
    form_class = SellsForm
    success_url = '/'
    def form_valid(self, form):
        # from .task import fun
        print('==========Calliing===========')
        # print(fun.delay())
        print(self.request.POST['item_name'])

        form.instance.user_name = self.request.user
        
        sold_item = Stock.objects.get(item_name = self.request.POST['item_name'], user_name=self.request.user)
        form.funn(self.request.user.username)
        qty = sold_item.item_qty
        qty -= int(self.request.POST['item_qty'])
        sold_item.item_qty = int(qty)
        sold_item.save()
        form.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form)
        print('invailid')
        print(form.errors)

class StockListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    
    model = Stock
    context_object_name = 'stock'
    template_name='stock_list.html'
    
    def get_queryset(self):
        import datetime
        now = datetime.datetime.now()
        print(now,'  ==================================')
        queryset = Stock.objects.filter(user_name=self.request.user)
        return queryset
  
class ReportView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Sells
    template_name='list.html'
    
    def get_context_data(self, *args, **kwargs):
        
        timezone.activate(pytz.timezone("Asia/Kolkata")) 
        context = super().get_context_data(**kwargs)
        f_date = t_date = localtime(now()).date()
        if self.request.user.is_superuser:
            context['data'] = Sells.objects.filter(created_at__date__range=[f_date, t_date]).order_by("user_name__username")#.group_by('user_name') 
            total_sells = Sells.objects.filter(created_at__date__range=[f_date, t_date]).aggregate(Sum('price'))
            context['total_sells'] = total_sells['price__sum']  
            context['username'] = True
            res = []
            sums = Sells.objects.filter(created_at__date__range=[f_date, t_date]).values('user_name').annotate(sums = Sum('price'))
            for i in sums:
                res.append(i)
                res[-1]['user_name'] = User.objects.get(id=i['user_name']).username
            context['sums'] = res
        else:
            context['data'] = Sells.objects.filter(user_name = self.request.user, created_at__date__range=[f_date, t_date]).order_by("-created_at")
            total_sells = Sells.objects.filter(user_name = self.request.user, created_at__date__range=[f_date, t_date]).aggregate(Sum('price'))
            context['total_sells'] = total_sells['price__sum']
        context['f_date'] = f_date
        context['t_date'] = t_date
        return context

    def post(self, request, *args, **kwargs):
        f_date = self.request.POST['f_date']
        t_date = self.request.POST['t_date']
        if f_date and t_date:
            pass
        elif f_date and not t_date:
            t_date = localtime(now()).date()
        else:
            f_date = t_date = localtime(now()).date()
        context = {}
        if self.request.user.is_superuser:
            context['data'] = Sells.objects.filter(created_at__date__range=[f_date, t_date]).order_by("user_name__username")#.group_by('user_name') 
            total_sells = Sells.objects.filter(created_at__date__range=[f_date, t_date]).aggregate(Sum('price'))
            context['total_sells'] = total_sells['price__sum']  
            context['username'] = True
            res = []
            sums = Sells.objects.filter(created_at__date__range=[f_date, t_date]).values('user_name').annotate(sums = Sum('price'))
            for i in sums:
                res.append(i)
                res[-1]['user_name'] = User.objects.get(id=i['user_name']).username
            context['sums'] = res
        else:
            context['data'] = Sells.objects.filter(user_name = self.request.user, created_at__date__range=[f_date, t_date]).order_by("-created_at")
            total_sells = Sells.objects.filter(user_name = self.request.user, created_at__date__range=[f_date, t_date]).aggregate(Sum('price'))
            context['total_sells'] = total_sells['price__sum']
        context['f_date'] = f_date
        context['t_date'] = t_date
        
        
        return render(request, 'list.html', context)