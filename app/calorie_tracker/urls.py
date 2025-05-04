from django.urls import path
from .views import FoodListAPIView, CalorieTrackerView, SubmitConsumptionView, LogPageView, DailySummaryView

urlpatterns = [
    path('', CalorieTrackerView.as_view(), name='calorie-tracker'),
    path('submit/', SubmitConsumptionView.as_view(), name='submit-consumption'),
    path('log/', LogPageView.as_view(), name='log-page1'),
    path('api/foods/', FoodListAPIView.as_view(), name='food-api'),
    path('daily-summary/', DailySummaryView.as_view(), name='daily-summary1'),
]