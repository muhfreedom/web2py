# -*- coding: utf-8 -*-
def index():
    #db.survey.description.readable=False
    #db.survey.choices.readable=False
    # db.survey.name.represent = lambda name,row: A(name,_href=URL('take_survey',args=row.uuid))
    #grid = SQLFORM.grid(db.survey.created_by==auth.user_id,create=False,editable=False,deletable=True,details=False,
                       #links=[#lambda row: A('take',_href=URL('take_survey',args=row.uuid),_class="btn"),
                             #lambda row: A('results',_href=URL('see_results',args=row.uuid),_class="btn")])
    return locals()



import pygal
from pygal.style import CleanStyle
def plot_pygal():
   response.headers['Content-Type']='image/svg+xml'
   bar_chart = pygal.Bar(style=CleanStyle)                                            # Then create a bar graph object
   bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
   return bar_chart.render()




@auth.requires_login()
def create_survey():
    def f(form):
        #form.vars.results = [0]*len(request.vars.choices)
        form.vars.results = request.vars.choices
    from gluon.utils import web2py_uuid,time
    db.survey.uuid.default = uuid = web2py_uuid()
    form = SQLFORM(db.survey).process(session=None, formname='test',onvalidation=f)
    if form.accepted:
        time.sleep(4)
        redirect(URL('create_survey2',args=uuid))
    return locals()

@auth.requires_login()
def create_survey2():
    def f(form):
        #form.vars.results = [0]*len(request.vars.choices)
        form.vars.results = request.vars.choices
    from gluon.utils import web2py_uuid,time
    db.survey.uuid.default = uuid = web2py_uuid()
    form = SQLFORM(db.survey).process(session=None, formname='test',onvalidation=f)
    if form.accepted:
        time.sleep(4)
        redirect(URL('create_survey3',args=uuid))
    return locals()

@auth.requires_login()
def create_survey3():
    def f(form):
        #form.vars.results = [0]*len(request.vars.choices)
        form.vars.results = request.vars.choices
    from gluon.utils import web2py_uuid,time
    db.survey.uuid.default = uuid = web2py_uuid()
    form = SQLFORM(db.survey).process(session=None, formname='test',onvalidation=f)
    if form.accepted:
        time.sleep(4)
        redirect(URL('thank_you',args=uuid))
    return locals()

@auth.requires_membership('managers')
def manage():
    grid = SQLFORM.grid(db.survey.created_by==auth.user_id,create=False,editable=False,deletable=True,details=False,
                       links=[#lambda row: A('take',_href=URL('take_survey',args=row.uuid),_class="btn"),
                              lambda row: A('results',_href=URL('see_results',args=row.uuid),_class="btn")])
    return locals()


@auth.requires_login()
def take_survey():
    uuid = request.args(0)
    survey = db.survey(uuid=uuid)
    if survey.requires_login:
        if not auth.user:
            redirect(URL('user/login',vars=dict(_next=URL(args=request.args))))
        #vote = db.vote(survey=survey.id,created_by=auth.user.id)
        participate = db.survey(uuid=uuid,created_by=auth.user.id)
        if participate:
            session.flash = 'Du har redan deltagit, dumma fan!!'
            redirect(URL('thank_you'))
    if request.post_vars:
        #k = int(request.post_vars.choice)
        k = request.post_vars.choice
        #survey.results[k]+=0
        survey.update_record(results=survey.results)
        db.vote.insert(survey=survey.id)
        redirect(URL('thank_you'))
    return locals()

@auth.requires_login()
def see_results():
    uuid = request.args(0)
    survey = db.survey(uuid=uuid)
    if survey.created_by!=auth.user.id:
        session.flash = 'User not authorized'
        redirect(URL('index'))
    return locals()

def thank_you():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
