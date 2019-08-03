from django import forms
import datetime


class NewPaymentForm(forms.Form):
    payment_description = forms.CharField(label='Payment description',
                                          max_length=100,
                                          required=True,
                                          widget=forms.Textarea)
    payment_value = forms.FloatField(label='Payment value', min_value=0, required=True)
    payment_date = forms.DateField(label='Payment date', initial=datetime.date.today, widget=forms.SelectDateWidget)


class DatePeriodSelectorForm(forms.Form):
    start_of_period_date = forms.DateField(label='Start date',
                                           initial=datetime.date.today,
                                           widget=forms.SelectDateWidget)
    end_of_period_date = forms.DateField(label='Start date', initial=datetime.date.today, widget=forms.SelectDateWidget)
