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
import datetime
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
        # print('==========Calliing===========')
        # print(fun.delay())
        # print(self.request.POST['item_name'],'======================')
        print(type(form.cleaned_data['item_name']),'===============')
        if str(form.cleaned_data['item_name']) == 'Debit':
            # form.cleaned_data['price'] = -(form.cleaned_data['price'])
            form.instance.price = form.cleaned_data['price'] * -1
        form.instance.user_name = self.request.user
        
        sold_item = Stock.objects.get(item_name = self.request.POST['item_name'], user_name=self.request.user)
        # form.funn(self.request.user.username)
        sold_item.is_admin_updated = False
        qty = sold_item.item_qty
        qty -= int(self.request.POST['item_qty'])
        sold_item.item_qty = int(qty)
        sold_item.save()
        form.save()
        return super().form_valid(form)


class StockListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    
    model = Stock
    context_object_name = 'stock'
    template_name='stock_list.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Stock.objects.all()
        else:
            now = datetime.datetime.now()
            queryset = Stock.objects.filter(user_name=self.request.user)
        return queryset
  
class ReportView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Sells
    template_name='list.html'
    
    def get_context_data(self, *args, **kwargs):
        
        timezone.activate(pytz.timezone("Asia/Kolkata"))
        context = super().get_context_data(**kwargs)
        # print(datetime.datetime.now().date(),' ============================')
        f_date = t_date = datetime.datetime.now().date()
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
            
        """ Adding sells to the context """
        sells = {}
        for i in context['data']:
            try:
                sells[i.item_name.item_name][1] += i.price
                sells[i.item_name.item_name][0] += i.item_qty
            except:
                sells[i.item_name.item_name] = [i.item_qty, i.price]
        
        if self.request.user.is_superuser:
            context['sells'] = sells
        
        """ Adding company wise sells to the context """
        company_wise_sells = []
        
        for i in context['data']:
            temp = {}
            try:
                temp['item_name'] = i.item_name.item_name
                temp['company_name'] = i.company_name.company_name
                temp['item_qty'] = i.item_qty
                temp['price'] = i.price
                company_wise_sells.append(temp)
                temp = {}
            except:
                pass
        
        company_wise_sub_total = {}
        
        for i in company_wise_sells:
            try:
                company_wise_sub_total[i['item_name'], i['company_name']][1] += i['price']
                company_wise_sub_total[i['item_name'], i['company_name']][0] += i['item_qty']
            except:
                company_wise_sub_total[i['item_name'], i['company_name']] = [i['item_qty'], i['price']]
                
        if self.request.user.is_superuser:
            context['company_wise_sub_total'] = company_wise_sub_total
        
        
        company_wise_total = {}
        
        for i in company_wise_sells:
            try:
                company_wise_total[i['company_name']] += i['price']
            except:
                company_wise_total[i['company_name']] = i['price']
                
        context['company_wise_total'] = company_wise_total
            
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
    
class ReportView1(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    model = Sells
    template_name='list.html'
    
    def get(self, request, *args, **kwargs):
        timezone.activate(pytz.timezone("Asia/Kolkata"))
        
        # print(datetime.datetime.now().date(),' ============================')
        f_date = t_date = datetime.datetime.now().date()
        if self.request.user.is_superuser:
            sells = {}
            # total_sells = Sells.objects.filter(created_at__date__range=[f_date, t_date]).values().order_by('item_name__item_name')
            total_sells = Sells.objects.all()
            print(total_sells,' =================')
            for i in total_sells:
                try:
                    sells[i.item_name.item_name][0] += i.price
                    sells[i.item_name.item_name][1] += i.item_qty
                except:
                    sells[i.item_name.item_name] = [i.price, i.item_qty]
                # print(i.item_name, i.company_name.company_name)
            print(sells,' =================')
            
            company_wise_sells = []
            
            for i in total_sells:
                temp = {}
                try:
                    temp['item_name'] = i.item_name.item_name
                    temp['company_name'] = i.company_name.company_name
                    temp['item_qty'] = i.item_qty
                    temp['price'] = i.price
                    company_wise_sells.append(temp)
                    temp = {}
                except:
                    pass
                
            print(company_wise_sells)
            
            company_wise_sub_total = {}
            
            for i in company_wise_sells:
                try:
                    company_wise_sub_total[i['item_name'], i['company_name']][0] += i['price']
                    company_wise_sub_total[i['item_name'], i['company_name']][1] += i['item_qty']
                except:
                    company_wise_sub_total[i['item_name'], i['company_name']] = [i['price'], i['item_qty']]
                    
            print(company_wise_sub_total)
            
            company_wise_total = {}
            
            for i in company_wise_sells:
                try:
                    company_wise_total[i['company_name']] += i['price']
                except:
                    company_wise_total[i['company_name']] = i['price']
                    
            print(company_wise_total)
            
            # print(total_sells)
            
            
        #     context['data'] = Sells.objects.filter(created_at__date__range=[f_date, t_date]).order_by("user_name__username")#.group_by('user_name') 
        #     total_sells = Sells.objects.filter(created_at__date__range=[f_date, t_date]).aggregate(Sum('price'))
        #     context['total_sells'] = total_sells['price__sum']  
        #     context['username'] = True
        #     res = []
        #     sums = Sells.objects.filter(created_at__date__range=[f_date, t_date]).values('user_name').annotate(sums = Sum('price'))
        #     for i in sums:
        #         res.append(i)
        #         res[-1]['user_name'] = User.objects.get(id=i['user_name']).username
        #     context['sums'] = res
        # context['f_date'] = f_date
        # context['t_date'] = t_date