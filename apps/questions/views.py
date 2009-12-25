#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.views.decorators.http import *
from django.utils.simplejson import JSONEncoder
from django.shortcuts import get_object_or_404
from rapidsms.webui.utils import *
from questions.models import *
from reporters.models import *
from export.utils import excel


def __global(req):
    return {
        "sections": Section.objects.all() }


@require_GET
def dashboard(req):
    return render_to_response(req,
        "questions/dashboard.html")


@require_GET
def section(req, section_pk):
    sect = get_object_or_404(
        Section, pk=section_pk)
    
    return render_to_response(req,
        "questions/section.html", {
            "active_section_tab": sect.pk,
            "questions": sect.questions.all(),
            "section": sect })


@require_GET
def question(req, section_pk, question_pk):
    sect = get_object_or_404(Section, pk=section_pk)
    ques = get_object_or_404(Question, pk=question_pk)
    
    return render_to_response(req,
        "questions/question.html", {
            "active_section_tab": sect.pk,
            "answers": ques.answers.all().select_related(),
            "question": ques,
            "section": sect })


@require_GET
def question_xls(req, section_pk, question_pk):
    sect = get_object_or_404(Section, pk=section_pk)
    ques = get_object_or_404(Question, pk=question_pk)
    
    def __row(answer):
        sub = answer.submission
        
        return [
            answer.normalized,
            sub.reported_by,
            sub.location,
            sub.submitted
        ]
    
    return excel(
        [["Answer", "Reporter", "Location", "Date"]] +
        [__row(ans) for ans in ques.answers.all()])


@require_GET
def submissions(req, reporter_pk=None, connection_pk=None):
    
    # if this view was accessed via /reporters/n/submissions,
    # include only those submissions linked to the reporter
    if reporter_pk is not None:
        rep = get_object_or_404(Reporter, pk=reporter_pk)
        subm = rep.submissions.all().order_by("-submitted")
        
        data = {
            "submissions": paginated(req, subm),
            "reporter": rep }
        
    # likewise for /connections/n/submissions
    # (TODO: right now, there is no /connections/n/
    # view in reporters.views, which is rather
    # confusing. we should probably implement it)
    elif connection_pk is not None:
        conn = get_object_or_404(PersistantConnection, pk=connection_pk)
        subm = conn.submissions.all().order_by("-submitted")
        
        data = {
            "submissions": paginated(req, subm),
            "connection": conn }
    
    # otherwise, include *all* submissions
    else:
        subm = Submission.objects.all().order_by("-submitted")
        data = { "submissions": paginated(req, subm) }
    
    return render_to_response(req,
        "questions/submissions.html",
        data)







@require_GET
def report(req):
    g = req.GET
    
    # check that the required fields
    # were all provided, or raise
    try:
        sc      = g["sc"]
        qx_num  = int(g["qx"])
        qy_num  = int(g["qy"])
        
    except KeyError:
        return HttpResponse(
            "Required fields: sc, qx, qy",
            content_type="text/plain",
            status=400)
    
    except ValueError:
        return HttpResponse(
            "Invalid question number(s)",
            content_type="text/plain",
            status=400)
    
    # resolve the section code into a Section
    # object, question numbers into Questions
    section = Section.objects.get(code=sc)
    qx      = section.questions.get(number=qx_num)
    qy      = section.questions.get(number=qy_num)
    
    # fetch and check the
    # values of optional fields
    qx_type = getattr(Answer, g.get("tx", "str").upper())
    qy_type = getattr(Answer, g.get("ty", "str").upper())
    
    # find all of the submissions which have answers
    # to both question-x and question-y. if either
    # are missing, we can't draw any correlation,
    # so omit the data altogether
    submissions = [
        (subm,
         subm.answers.get(question__number=qx_num),
         subm.answers.get(question__number=qy_num))
        for subm in Submission.objects.filter(section__code=sc)
        if subm.answers.filter(question__number__in=[qx_num, qy_num]).count() == 2]
    
    graph_data = [
        (ans_x.normalized(qx_type),
         ans_y.normalized(qy_type))
        for subm, ans_x, ans_y in submissions]
    
    graph_data_json =\
        JSONEncoder().encode(
            graph_data)
    
    return render_to_response(req,
        "questions/report.html", {
        "graph_data": graph_data_json,
        "submissions": submissions,
        "question_x": qx,
        "question_y": qy
    })
    
    return HttpResponse(
        "subm: %r\nans: %r" % (list(submissions), list(answers)),
        content_type="text/plain")
