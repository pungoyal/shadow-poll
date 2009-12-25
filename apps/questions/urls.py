#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.conf.urls.defaults import *
import questions.views as views


urlpatterns = patterns('',
    
    # mini dashboard for this app
    url(r'^questions$',
        views.dashboard,
        name="questions-home"),
    
    # view all questions and recent activity
    # within a section
    url(r'^sections/(?P<section_pk>\d+)$',
        views.section,
        name="view-section"),
    
    # to view all of the submissions and answers
    # linked to a question, with lightweight graphs
    url(r'^sections/(?P<section_pk>\d?)/questions/(?P<question_pk>\d+)$',
        views.question,
        name="view-question"),
    
    # to view all of the submissions and answers
    # linked to a question, with lightweight graphs
    url(r'^sections/(?P<section_pk>\d?)/questions/(?P<question_pk>\d+)/xls$',
        views.question_xls,
        name="export-question-xls"),
    
    # to view all submissions
    url(r'^submissions/$',
        views.submissions,
        name="view-submissions"),
        
    # to view all submissions
    # ...by a single reporter
    url(r'^reporters/(?P<reporter_pk>\d+)/submissions/$',
        views.submissions,
        name="submissions-by-reporter"),
    
    # to view all submissions
    # ...by a single connection
    url(r'^connections/(?P<connection_pk>\d+)/submissions/$',
        views.submissions,
        name="submissions-by-connection")
)
