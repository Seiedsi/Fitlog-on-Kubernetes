from django.urls import path
from .views import ExerciseListAPIView, WorkoutTrackerView, SubmitExerciseView, LogPageView, DailySummaryView

urlpatterns = [
    path('', WorkoutTrackerView.as_view(), name='workout-tracker'),
    path('submit/', SubmitExerciseView.as_view(), name='submit-exercised'),
    path('log/', LogPageView.as_view(), name='log-page'),
    path('api/workouts/', ExerciseListAPIView.as_view(), name='workout-api'),
    path('daily-summary/', DailySummaryView.as_view(), name='daily-summary'),
]