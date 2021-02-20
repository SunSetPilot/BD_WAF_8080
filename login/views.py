from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from hashlib import sha1

# Create your views here.
def user_login(request):
    u_name = request.POST.get('username')
    u_pwd = request.POST.get('password')
    if u_name == 'admin' and u_pwd == 'bytedance10':
        request.session['is_login'] = True
        request.session.set_expiry(0)
        return JsonResponse({"code":200})
    else:
        pass
