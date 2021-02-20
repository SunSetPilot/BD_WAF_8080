import os

from django.http import JsonResponse
from django.shortcuts import render
from BW_list.models import IP_list
from BW_list.models import URL_list

# Create your views here.
def get_white_ip(request):
    ret = request.session.get('is_login', False)
    if ret:
        data = []
        for line in IP_list.objects.filter(type__exact='white ip'):
            ip_data={}
            ip_data['id'] = line.id
            ip_data['range'] = line.ip
            ip_data['status'] = line.status
            data.append(ip_data)
        return JsonResponse(data,safe=False)
    else:
        pass

def get_black_ip(request):
    ret = request.session.get('is_login', False)
    if ret:
        data = []
        for line in IP_list.objects.filter(type__exact='black ip'):
            ip_data={}
            ip_data['id'] = line.id
            ip_data['range'] = line.ip
            ip_data['status'] = line.status
            data.append(ip_data)
        return JsonResponse(data,safe=False)
    else:
        pass

def get_white_url(request):
    ret = request.session.get('is_login', False)
    if ret:
        data = []
        for line in URL_list.objects.filter(type__exact='white url'):
            url_data={}
            url_data['id'] = line.id
            url_data['remark'] = line.remark
            url_data['url'] = line.url
            data.append(url_data)
        return JsonResponse(data, safe=False)
    else:
        pass

def get_black_url(request):
    ret = request.session.get('is_login', False)
    if ret:
        data = []
        for line in URL_list.objects.filter(type__exact='black url'):
            url_data={}
            url_data['id'] = line.id
            url_data['remark'] = line.remark
            url_data['url'] = line.url
            data.append(url_data)
        return JsonResponse(data, safe=False)
    else:
        pass

def add_bw(request):
    ret = request.session.get('is_login', False)
    if ret:
        my_type = request.POST.get('type')
        if my_type=='white ip' or my_type=='black ip':
            my_ip = request.POST.get('ip')
            my_status = request.POST.get('status')
            IP_list.objects.create(type=my_type,ip=my_ip,status=my_status)
            with open('/usr/local/nginx/conf/ip_black.txt','w') as f:
                for line in IP_list.objects.filter(status__exact='yes').filter(type__exact='black ip'):
                    f.write(line.ip+'\n')
            with open('/usr/local/nginx/conf/ip_white.txt','w') as f:
                for line in IP_list.objects.filter(status__exact='yes').filter(type__exact='white ip'):
                    f.write(line.ip+'\n')
            os.system('/usr/local/nginx/sbin/nginx -s reload')
            return JsonResponse({'code':200})

        elif my_type=='white url' or my_type=='black url':
            my_url = request.POST.get('url')
            my_remark = request.POST.get('remark')
            URL_list.objects.create(type=my_type,url=my_url,remark=my_remark)
            with open('/usr/local/nginx/conf/url_black.txt','w') as f:
                for line in URL_list.objects.filter(type__exact='black url'):
                    f.write(line.url+'\n')
            with open('/usr/local/nginx/conf/url_white.txt','w') as f:
                for line in URL_list.objects.filter(type__exact='white url'):
                    f.write(line.url+'\n')
            os.system('/usr/local/nginx/sbin/nginx -s reload')
            return JsonResponse({'code': 200})
    else:
        pass

def del_list(request):
    ret = request.session.get('is_login', False)
    if ret:
        my_type = request.POST.get('type')
        my_id = request.POST.get('id')
        if my_type=='white ip':
            IP_list.objects.get(id__exact=my_id).delete()
            with open('/usr/local/nginx/conf/ip_white.txt','w') as f:
                for line in IP_list.objects.filter(status__exact='yes').filter(type__exact='white ip'):
                    f.write(line.ip+'\n')
            os.system('/usr/local/nginx/sbin/nginx -s reload')
            return JsonResponse({'code': 200})
        elif my_type=='black ip':
            IP_list.objects.get(id__exact=my_id).delete()
            with open('/usr/local/nginx/conf/ip_black.txt', 'w') as f:
                for line in IP_list.objects.filter(status__exact='yes').filter(type__exact='black ip'):
                    f.write(line.ip + '\n')
            os.system('/usr/local/nginx/sbin/nginx -s reload')
            return JsonResponse({'code': 200})
        elif my_type=='white url':
            URL_list.objects.get(id__exact=my_id).delete()
            with open('/usr/local/nginx/conf/url_white.txt','w') as f:
                for line in URL_list.objects.filter(type__exact='white url'):
                    f.write(line.url+'\n')
            os.system('/usr/local/nginx/sbin/nginx -s reload')
            return JsonResponse({'code': 200})
        elif my_type=='black ip':
            URL_list.objects.get(id__exact=my_id).delete()
            with open('/usr/local/nginx/conf/url_black.txt', 'w') as f:
                for line in URL_list.objects.filter(type__exact='black url'):
                    f.write(line.url + '\n')
            os.system('/usr/local/nginx/sbin/nginx -s reload')
            return JsonResponse({'code': 200})
    else:
        pass

def change_bw_ip(request):
    ret = request.session.get('is_login', False)
    if ret:
        my_id = request.POST.get('id')
        my_type = request.POST.get('type')
        my_status = request.POST.get('status')
        my_ip = request.POST.get('ip')
        line = IP_list.objects.get(id__exact=my_id)
        line.type = my_type
        line.status = my_status
        line.ip = my_ip
        line.save()
        with open('/usr/local/nginx/conf/ip_black.txt', 'w') as f:
            for line in IP_list.objects.filter(status__exact='yes').filter(type__exact='black ip'):
                f.write(line.ip + '\n')
        with open('/usr/local/nginx/conf/ip_white.txt', 'w') as f:
            for line in IP_list.objects.filter(status__exact='yes').filter(type__exact='white ip'):
                f.write(line.ip + '\n')
        os.system('/usr/local/nginx/sbin/nginx -s reload')
        return JsonResponse({'code': 200})
    else:
        pass

def change_bw_url(request):
    ret = request.session.get('is_login', False)
    if ret:
        my_id = request.POST.get('id')
        my_type = request.POST.get('type')
        my_remark = request.POST.get('remark')
        my_url = request.POST.get('url')
        line = URL_list.objects.get(id__exact=my_id)
        line.type = my_type
        line.remark = my_remark
        line.url = my_url
        line.save()
        with open('/usr/local/nginx/conf/url_black.txt', 'w') as f:
            for line in URL_list.objects.filter(type__exact='black url'):
                f.write(line.url + '\n')
        with open('/usr/local/nginx/conf/url_white.txt', 'w') as f:
            for line in URL_list.objects.filter(type__exact='white url'):
                f.write(line.url + '\n')
        os.system('/usr/local/nginx/sbin/nginx -s reload')
        return JsonResponse({'code': 200})
    else:
        pass