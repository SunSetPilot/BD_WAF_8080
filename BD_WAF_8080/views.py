from django.http import HttpResponse


def redirct(request):
    ret = request.session.get('is_login', False)
    if ret:
        return HttpResponse('<script type="text/javascript">window.location.href="http://47.104.175.189:8080/rules.html";</script>"')
    else:
        return HttpResponse('<script type="text/javascript">window.location.href="http://47.104.175.189:8080/login.html";</script>"')