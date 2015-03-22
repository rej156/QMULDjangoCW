from django.shortcuts import render,render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from social.models import Member, Profile

appname = 'Facemagazine'

def index(request):
    template = loader.get_template('social/index.html')
    context = RequestContext(request, {
            'appname': appname,
        })
    return HttpResponse(template.render(context))

def messages(request):
    if 'username' in request.session:
        username = request.session['username']
        template = loader.get_template('social/messages.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': username,
                'loggedin': True
            })

        return HttpResponse(template.render(context))
    else:
        raise Http404("User is not logged it, no access to messages page!")

def signup(request):
    template = loader.get_template('social/signup.html')
    context = RequestContext(request, {
            'appname': appname,
        })
    return HttpResponse(template.render(context))

def register(request):
    u = request.POST['user']
    p = request.POST['pass']
    user = Member(username=u, password=p)
    user.save()
    template = loader.get_template('social/user-registered.html')
    context = RequestContext(request, {
        'appname': appname,
        'username' : u
        })
    return HttpResponse(template.render(context))

def login(request):
    if 'username' not in request.POST:
        template = loader.get_template('social/login.html')
        context = RequestContext(request, {
                'appname': appname,
            })
        return HttpResponse(template.render(context))
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            raise Http404("User does not exist")
        if member.password == p:
            request.session['username'] = u;
            request.session['password'] = p;
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
                )
        else:
            raise Http404("Incorrect password")

def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()
        template = loader.get_template('social/logout.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': u
            })
        return HttpResponse(template.render(context))
    else:
        raise Http404("Can't logout, you are not logged in")

def member(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=view_user)

        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"

        if member.profile:
            text = member.profile.text
        else:
            text = ""
        return render(request, 'social/member.html', {
            'appname': appname,
            'username': username,
            'greeting': greeting,
            'profile': text,
            'loggedin': True}
            )
    else:
        raise Http404("User is not logged it, no access to members page!")

def friends(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        # render reponse
        return render(request, 'social/friends.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'followers': followers,
            'loggedin': True}
            )
    else:
        raise Http404("User is not logged it, no access to members page!")

def members(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # follow new friend
        if 'add' in request.GET:
            friend = request.GET['add']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.add(friend_obj)
            member_obj.save()
        # unfollow a friend
        if 'remove' in request.GET:
            friend = request.GET['remove']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.remove(friend_obj)
            member_obj.save()
        # view user profile
        if 'view' in request.GET:
            return member(request, request.GET['view'])
        else:
            # list of all other members
            members = Member.objects.exclude(pk=username)
            # list of people I'm following
            following = member_obj.following.all()
            # list of people that are following me
            followers = Member.objects.filter(following__username=username)
            # render reponse
            return render(request, 'social/members.html', {
                'appname': appname,
                'username': username,
                'members': members,
                'following': following,
                'followers': followers,
                'loggedin': True}
                )
    else:
        raise Http404("User is not logged it, no access to members page!")

def profile(request):
    if 'username' in request.session:
        u = request.session['username']
        member = Member.objects.get(pk=u)
        if 'text' in request.POST:
            text = request.POST['text']
            if member.profile:
                member.profile.text = text
                member.profile.save()
            else:
                profile = Profile(text=text)
                profile.save()
                member.profile = profile
            member.save()
        else:
            if member.profile:
                text = member.profile.text
            else:
                text = ""
        return render(request, 'social/profile.html', {
            'appname': appname,
            'username': u,
            'text' : text,
            'loggedin': True}
            )
    else:
        raise Http404("User is not logged it, no access to profiles!")

def checkuser(request):
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return HttpResponse("<span class='taken'>&nbsp;&#x2718; This username is taken</span>")
        else:
            return HttpResponse("<span class='available'>&nbsp;&#x2714; This username is available</span>")

def handler404(request):
    response = render_to_response('social/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response
