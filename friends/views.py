from django.contrib.auth.models import User
from selectstat.friends.models import JoinInvitation, Friendship, FriendshipInvitation
from selectstat.friends.forms import JoinRequestForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

def accept_join_invitation(request, confirmation_key):
    # haven't gotten this to work as I'm using django-registration
    pass

def accept_friendship_invitation(request, from_user_id):
    to_user = get_object_or_404(User, username=request.user)
    from_user = get_object_or_404(User, id=from_user_id)
    
    invites = FriendshipInvitation.objects.invitations(to_user=to_user, from_user=from_user)
    for invite in invites:
        invite.accept()
    
    to_user.message_set.create(message="You and %s are now friends." % (from_user.first_name))
    
    return HttpResponseRedirect(reverse('friends_manage'))
accept_friendship_invitation=login_required(accept_friendship_invitation)

def decline_friendship_invitation(request, from_user_id):
    to_user = get_object_or_404(User, username=request.user)
    from_user = get_object_or_404(User, id=from_user_id)
    
    invites = FriendshipInvitation.objects.invitations(to_user=to_user, from_user=from_user)
    for invite in invites:
        invite.decline()
    
    to_user.message_set.create(message="%s's reqeust for friendship has been declined." % (from_user.first_name))
    
    return HttpResponseRedirect(reverse('friends_manage'))
decline_friendship_invitation=login_required(decline_friendship_invitation)
    

def manage_friendships(request, template_name="friends/manage_friendships.html"):
    user = get_object_or_404(User, username=request.user)
    
    friendships = Friendship.objects.friends_for_user(user)
    friendship_invitations = FriendshipInvitation.objects.invitations(to_user=user).exclude(status="5")
    
    try:
        profile_obj = user.get_profile()
    except ObjectDoesNotExist:
        raise Http404

    
    extra_context = {
                     'friendships':friendships,
                     'friendship_invitations': friendship_invitations
                     }
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              {},
                              context_instance=context)        
manage_friendships = login_required(manage_friendships)


def remove_friendship(request, to_user_id):
    from_user = get_object_or_404(User, username=request.user)
    to_user = get_object_or_404(User, id=to_user_id)
    
    Friendship.objects.remove(from_user, to_user)
    
    from_user.message_set.create(message="You and %s are no longer friends." % (to_user.first_name))
    
    return HttpResponseRedirect(reverse('friends_manage'))
remove_friendship=login_required(remove_friendship)


def send_friendship_invitation(request, to_user_id):
    from_user = get_object_or_404(User, username=request.user)
    to_user = get_object_or_404(User, id=to_user_id)
    
    FriendshipInvitation.objects.send_invitation(from_user, to_user)

    from_user.message_set.create(message="An invitation has been sent to %s." % (to_user.first_name))
    
    return HttpResponseRedirect(reverse('friends_manage'))
send_friendship_invitation = login_required(send_friendship_invitation)


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