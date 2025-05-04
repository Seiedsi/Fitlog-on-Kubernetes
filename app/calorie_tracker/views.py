from datetime import date
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import generics
from .models import Food, Consumption
from .serializers import FoodSerializer
from django.views import View
from django.core.paginator import Paginator

class FoodListAPIView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class CalorieTrackerView(LoginRequiredMixin, TemplateView):
    template_name = 'fitlog/calorie_tracker.html'


class SubmitConsumptionView(LoginRequiredMixin, View):
    success_url = reverse_lazy('calorie-tracker')

    def post(self, request, *args, **kwargs):
        food_id = request.POST.get('food')
        amount = request.POST.get('amount')

        try:
            food = Food.objects.get(id=food_id)
            Consumption.objects.create(
                user=request.user,
                food=food,
                amount=amount
            )
            return redirect(self.success_url)
        except Food.DoesNotExist:
            return redirect('calorie-tracker')

class LogPageView(LoginRequiredMixin, TemplateView):
    template_name = 'fitlog/log_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consumption = Consumption.objects.filter(user=self.request.user, date_consumed=date.today())
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        for item in consumption:
            item.calories = item.calculated_calories()
            total_calories = total_calories + item.calories
            item.protein = item.calculated_protein()
            total_protein = total_protein + item.protein
            item.carbs = item.calculated_carbs()
            total_carbs = total_carbs + item.carbs
            item.fats = item.calculated_fats()
            total_fats = total_fats + item.fats
        context['consumption'] = consumption
        context['total_calories'] = total_calories
        context['total_protein'] = total_protein
        context['total_carbs'] = total_carbs
        context['total_fats'] = total_fats
        return context


class DailySummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'fitlog/daily_summary.html'
    paginate_by = 7  # Days per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get unique dates for the user
        dates = Consumption.objects.filter(user=self.request.user) \
            .dates('date_consumed','day', order='DESC')

        # Paginate dates
        paginator = Paginator(dates, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Calculate totals for each date in current page
        daily_totals = []
        for date_obj in page_obj.object_list:
            consumptions = Consumption.objects.filter(
                user=self.request.user,
                date_consumed=date_obj
            )

            totals = {
                'date': date_obj,
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fats': 0
            }

            for c in consumptions:
                ratio = c.amount / 100
                totals['calories'] += c.food.calories * ratio
                totals['protein'] += c.food.protein * ratio
                totals['carbs'] += c.food.carbs * ratio
                totals['fats'] += c.food.fats * ratio

            daily_totals.append(totals)

        context.update({
            'page_obj': page_obj,
            'daily_totals': daily_totals
        })
        return context