from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import RedirectView


class Logout(RedirectView):
    def get(self, request: HttpRequest):
        logout(request)
        return HttpResponseRedirect(reverse("index"))
