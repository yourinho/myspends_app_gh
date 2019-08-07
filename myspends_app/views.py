from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect

from .models import Spend
from .forms.forms import NewPaymentForm
from .forms.forms import DatePeriodSelectorForm
import datetime

# from django.template import loader


def payments_list(request):
    # payments = Spend.objects.all()
    date_preset = request.GET['date_preset']
    payments = Spend.objects.filter(spend_owner=request.user.id)
    if date_preset == 'today':
        payments = Spend.objects.filter(spend_date=datetime.date.today())\
            .filter(spend_owner=request.user.id)
    elif date_preset == 'yesterday':
        payments = Spend.objects.filter(spend_date=datetime.date.today()-datetime.timedelta(days=1))\
            .filter(spend_owner=request.user.id)
    elif date_preset == 'current_week':
        week_start_date = datetime.date.today()-datetime.timedelta(datetime.date.today().weekday())
        payments = Spend.objects.filter(spend_date__gte=week_start_date)\
            .filter(spend_date__lte=datetime.date.today())\
            .filter(spend_owner=request.user.id)
    elif date_preset == 'previous_week':
        week_end_date = datetime.date.today() - datetime.timedelta(datetime.date.today().weekday()) - \
                        datetime.timedelta(days=1)
        week_start_date = week_end_date - datetime.timedelta(days=6)
        payments = Spend.objects.filter(spend_date__gte=week_start_date)\
            .filter(spend_date__lte=week_end_date)\
            .filter(spend_owner=request.user.id)
    elif date_preset == 'current_month':
        month_end_date = datetime.date.today()
        month_start_date = month_end_date - datetime.timedelta(days=datetime.date.today().day) \
                           + datetime.timedelta(days=1)
        payments = Spend.objects.filter(spend_date__gte=month_start_date)\
            .filter(spend_date__lte=month_end_date)\
            .filter(spend_owner=request.user.id)
    elif date_preset == 'previous_month':
        month_end_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().day)
        month_start_date = month_end_date - datetime.timedelta(days=month_end_date.day) + datetime.timedelta(days=1)
        payments = Spend.objects.filter(spend_date__gte=month_start_date)\
            .filter(spend_date__lte=month_end_date)\
            .filter(spend_owner=request.user.id)
    summary = 0
    for payment in payments:
        summary += payment.spend_value
    context = {
        'payments_owner': request.user.username,
        'payments_context': payments,
        'summary': summary,
    }
    return render(request, 'myspends_app/payments_list.html', context)


def new_payment(request):
    if request.method == 'POST':
        form = NewPaymentForm(request.POST)
        if form.is_valid():
            payment_record = Spend()
            payment_record.spend_owner = request.user.id
            payment_record.spend_text = form.cleaned_data['payment_description']
            payment_record.spend_value = form.cleaned_data['payment_value']
            payment_record.spend_date = form.cleaned_data['payment_date']
            payment_record.save()
            return HttpResponseRedirect('/myspends_app/payments_list?date_preset=today')
    else:
        form = NewPaymentForm()
    return render(request, 'myspends_app/new_payment.html', {'form': form})


def payment_details(request, payment_id):
    # payment = "You are looking for payment with id=%s."
    try:
        payment = Spend.objects.get(pk=payment_id)
    except Spend.DoesNotExist:
        raise Http404("Payment does not exist.")
    context = {
        'payment_details': payment,
    }
    return render(request, 'myspends_app/payments_detail.html', context)


def edit_payment(request, payment_id):
    try:
        payment_record = Spend.objects.get(pk=payment_id)
    except Spend.DoesNotExist:
        raise Http404("Payment does not exist.")
    data = {'payment_description': payment_record.spend_text,
            'payment_value': payment_record.spend_value,
            'payment_date': payment_record.spend_date}
    if request.method == 'POST':
        form = NewPaymentForm(request.POST, initial=data)
        if form.is_valid():
            payment_record.spend_owner = request.user.id
            payment_record.spend_text = form.cleaned_data['payment_description']
            payment_record.spend_value = form.cleaned_data['payment_value']
            payment_record.spend_date = form.cleaned_data['payment_date']
            payment_record.save()
            return HttpResponseRedirect('/myspends_app/payments_list?date_preset=today')
    else:
        form = NewPaymentForm(initial=data)
    return render(request, 'myspends_app/edit_payment.html', {'form': form})


def delete_payment(request, payment_id):
    try:
        Spend.objects.filter(pk=payment_id).delete()
    except Spend.DoesNotExist:
        raise Http404("Payment does not exist.")
    return HttpResponseRedirect('/myspends_app/payments_list?date_preset=today')
