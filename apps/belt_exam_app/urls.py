from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'login$',views.login),
    url(r'register$',views.register),
    url(r'logout$',views.logout),
    url(r'dashboard$',views.dashboard),
    url(r'jobs/new$',views.add_job),
    url(r'addjob$',views.addjobDB),
    url(r'adduserjob/(?P<job_id>\d+)$',views.add_job_to_user),
    url(r'removeuserjob/(?P<job_id>\d+)$',views.remove_job_from_user),
    url(r'jobs/edit/(?P<job_id>\d+)$',views.edit_job),
    url(r'editjob/(?P<job_id>\d+)$',views.editjob),
    url(r'jobs/(?P<job_id>\d+)$',views.view_job),
    url(r'remove_job/(?P<job_id>\d+)$',views.remove_job)
]