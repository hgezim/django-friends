from django.contrib.auth.models import User
from selectstat.friends.models import JoinInvitation
from selectstat.friends.forms import JoinRequestForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

def accept_join_invitation(request, confirmation_key):
    # in registration save(),
    # if there's join confirmation key:
    #    in post_save() of user
    #    accept the JoinInvitation request
    # else
    #     squat!
    pass

def send_join_invitation(request, form_class=JoinRequestForm, template_name="friends/send_join_invitation.html"):
    user = get_object_or_404(User, username=request.user)

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            form.save(user)

            return HttpResponseRedirect(reverse('friends_send_join'))
    else:
        form = form_class()    

    context = RequestContext(request)
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)        
send_join_invitation = login_required(send_join_invitation)