import base64
import hashlib
import hmac
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from social_django.models import UserSocialAuth

from src import settings


class CSRFExemptView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptView, self).dispatch(*args, **kwargs)


def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    return render(request, 'home.html')


class DeauthorizeView(CSRFExemptView):
    def post(self, request, *args, **kwargs):
        try:
            signed_request = request.POST['signed_request']
            encoded_sig, payload = signed_request.split('.')
        except (ValueError, KeyError):
            return HttpResponse(status=400, content='Invalid request')

        try:
            # Reference for request decoding:
            # https://developers.facebook.com/docs/games/gamesonfacebook/login#parsingsr
            # For some reason, the request needs to be padded in order to be decoded.
            # See https://stackoverflow.com/a/6102526/2628463
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode(
                'utf-8')
            decoded_payload = json.loads(decoded_payload)

            if type(
                    decoded_payload) is not dict or 'user_id' not in decoded_payload.keys():
                return HttpResponse(status=400, content='Invalid payload data')

        except (ValueError, json.JSONDecodeError):
            return HttpResponse(status=400, content='Could not decode payload')

        try:
            secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET

            sig = base64.urlsafe_b64decode(encoded_sig + "==")
            expected_sig = hmac.new(
                bytes(secret, 'utf-8'),
                bytes(payload, 'utf-8'), hashlib.sha256
            )
        except:
            return HttpResponse(
                status=400, content='Could not decode signature'
            )

        if not hmac.compare_digest(expected_sig.digest(), sig):
            return HttpResponse(status=400, content='Invalid request')

        user_id = decoded_payload['user_id']

        try:
            user_social_auth = UserSocialAuth.objects.get(uid=user_id)
        except UserSocialAuth.DoesNotExist:
            return HttpResponse(status=200)
        #
        # Own custom logic here

        # now set the user is_active flag to false.
        user_social_auth.user.is_active = False
        user_social_auth.user.save(commit=True)

        return HttpResponse(status=200)
