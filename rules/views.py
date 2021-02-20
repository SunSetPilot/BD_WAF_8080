import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from rules.models import Rules
# Create your views here.
def get_all_rules(request):
    ret = request.session.get('is_login', False)
    if ret:
        data = []
        for line in Rules.objects.filter(r_selected__exact=0):
            rule_data = {}
            rule_data['id'] = line.r_id
            rule_data['rulename'] = line.r_name
            rule_data['type'] = line.r_type
            rule_data['date'] = line.r_date
            rule_data['discription'] = line.r_discription
            data.append(rule_data)
        return JsonResponse(data,safe=False)
    else:
        pass

def get_selected_rules(request):
    ret = request.session.get('is_login', False)
    if ret:
        data = []
        for line in Rules.objects.filter(r_selected__exact=1):
            rule_data = {}
            rule_data['id'] = line.r_id
            rule_data['rulename'] = line.r_name
            rule_data['type'] = line.r_type
            rule_data['date'] = line.r_date
            rule_data['discription'] = line.r_discription
            data.append(rule_data)
        return JsonResponse(data,safe=False)
    else:
        pass

def add_rules(request):
    ret = request.session.get('is_login', False)
    if ret:
        for rule in json.loads(request.POST.get('rules')):
            id = rule['id']
            r = Rules.objects.get(r_id__exact=id)
            r.r_selected = 1
            r.save()
        with open('/usr/local/nginx/conf/rules/user_rule_ban.conf','w') as f:
            for line in Rules.objects.filter(r_selected__exact=0):
                f.write('SecRuleRemoveById'+' '+line.r_id+'\n')
        os.system('/usr/local/nginx/sbin/nginx -s reload')
        return JsonResponse({"code":200})
    else:
        pass

def del_rules(request):
    ret = request.session.get('is_login', False)
    if ret:
        for rule in json.loads(request.POST.get('rules')):
            id = rule['id']
            r = Rules.objects.get(r_id__exact=id)
            r.r_selected = 0
            r.save()
        with open('/usr/local/nginx/conf/rules/user_rule_ban.conf', 'w') as f:
            for line in Rules.objects.filter(r_selected__exact=0):
                f.write('SecRuleRemoveById' + ' ' + line.r_id + '\n')
        os.system('/usr/local/nginx/sbin/nginx -s reload')
        return JsonResponse({"code":200})
    else:
        pass