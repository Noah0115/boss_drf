from django.contrib import admin
from django.urls import path
from back.api import index
urlpatterns = [
    path('', index.index),
    path('index/', index.index),
    path('datatable/', index.datatable),
    path('avgWageOfCityAndJob/', index.avgWageOfCityAndJob),
    path('everyJobTypeCountInCity/', index.everyJobTypeCountInCity),
    path('job_count_inCity/', index.job_count_inCity),
    path('educationAndExperienceOfCity/', index.educationAndExperienceOfCity),
    path('getJobsInfo/', index.getJobsInfo),
    path('avgWage/', index.getAvgSalaryByCityAndJobType),
    path('jobTypeCountOfCity/', index.getJobTypeCountByCity),
    path('jobCountsEveryCity/', index.getJobCountsByEveryCity),
    path('getEducationAndExperienceOfCity/', index.getEducationAndExperienceOfCity),
    path('onlineSpider/', index.onlineSpider),
    path('data_init/', index.data_init),
    path('data_init_page/', index.data_init_page),
    path('data_to_sql/', index.data_to_sql),
    path('predict_page/', index.predict_page),
    path('predict/', index.predict),



]
