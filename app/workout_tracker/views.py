from datetime import date
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import generics
from .models import Workout, Exercise
from .serializers import WorkoutSerializer
from django.views import View
from django.core.paginator import Paginator

class ExerciseListAPIView(generics.ListAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutTrackerView(LoginRequiredMixin, TemplateView):
    template_name = 'fitlog/workout_tracker.html'


class SubmitExerciseView(LoginRequiredMixin, View):
    success_url = reverse_lazy('workout-tracker')

    def post(self, request, *args, **kwargs):
        workout_id = request.POST.get('workout')
        time = request.POST.get('time')

        try:
            workout = Workout.objects.get(id=workout_id)
            Exercise.objects.create(
                user=request.user,
                workout=workout,
                time=time,
            )
            return redirect(self.success_url)
        except Workout.DoesNotExist:
            return redirect('workout-tracker')

class LogPageView(LoginRequiredMixin, TemplateView):
    template_name = 'fitlog/workout_log_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercised = Exercise.objects.filter(user=self.request.user, date_exercised=date.today())
        total_calories_burned = 0
        for item in exercised:
            item.calories = item.calculated_calories()
            total_calories_burned = total_calories_burned + item.calories
        context['exercised'] = exercised
        context['total_calories'] = total_calories_burned
        return context


class DailySummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'fitlog/workout_daily_summary.html'
    paginate_by = 7  # Days per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get unique dates for the user
        dates = Exercise.objects.filter(user=self.request.user) \
            .dates('date_exercised','day', order='DESC')

        # Paginate dates
        paginator = Paginator(dates, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Calculate totals for each date in current page
        daily_totals = []
        for date_obj in page_obj.object_list:
            exercise = Exercise.objects.filter(
                user=self.request.user,
                date_exercised=date_obj
            )

            totals = {
                'date': date_obj,
                'calories': 0,
            }

            for e in exercise:
                ratio = e.time / 60
                totals['calories'] += e.workout.calories * ratio

            daily_totals.append(totals)

        context.update({
            'page_obj': page_obj,
            'daily_totals': daily_totals
        })
        return context