from django.http import JsonResponse
from django.shortcuts import render
from rules_file.models import rule_files_list
from rules.models import Rules
import os
import msc_pyparser
import datetime

# Create your views here.

def get_rule_files(request):
    ret = request.session.get('is_login',False)
    if ret:
        data = []
        for line in rule_files_list.objects.all():
            file_data = {}
            file_data['id'] = line.id
            file_data['rulename'] = line.f_name
            file_data['type'] = line.f_type
            file_data['date'] = line.f_date
            file_data['discription'] = line.f_discription
            data.append(file_data)
        return JsonResponse(data,safe=False)
    else:
        pass

def del_rule_file(request):
    ret = request.session.get('is_login', False)
    if ret:
        f_id = request.POST.get('id')
        rulename = request.POST.get('rulename')
        Rules.objects.filter(r_file=rulename).delete()
        rule_files_list.objects.filter(id=f_id).delete()
        os.remove(os.path.join('/usr/local/nginx/conf/rules',rulename))
        with open('/usr/local/nginx/conf/rules/user_rule_ban.conf', 'w') as f:
            for line in Rules.objects.filter(r_selected__exact=0):
                f.write('SecRuleRemoveById' + ' ' + line.r_id + '\n')
        os.system('/usr/local/nginx/sbin/nginx -s reload')
        return JsonResponse({"code":200})
    else:
        pass

def add_file(request):
    ret = request.session.get('is_login', False)
    if ret:
        file_type = request.POST.get('type')
        file_discription = request.POST.get('discription')
        upload_file = request.FILES['file']
        rule_files_list.objects.create(f_name=upload_file.name,f_type=file_type,f_date=datetime.date.today(),f_discription=file_discription)
        with open(os.path.join('/usr/local/nginx/conf/rules',upload_file.name),'wb+') as f:
            for chunk in upload_file.chunks():
                f.write(chunk)
        mparser = msc_pyparser.MSCParser()
        with open(os.path.join('/usr/local/nginx/conf/rules', upload_file.name), 'r') as f:
            data = f.read()
        mparser.parser.parse(data)
        num = 1
        for line in mparser.configlines:
            if line['type']=='SecRule':
                name = file_type+str(num)
                actions = line['actions']
                for x in actions:
                    if x['act_name']=='id':
                        id = x['act_arg']
                        break
                Rules.objects.create(r_id=id,r_name=name,r_type=file_type,r_date=datetime.date.today(),r_discription=file_discription,r_file=upload_file.name)
                num+=1
        with open('/usr/local/nginx/conf/rules/user_rule_ban.conf', 'w') as f:
            for line in Rules.objects.filter(r_selected__exact=0):
                f.write('SecRuleRemoveById' + ' ' + line.r_id + '\n')
        os.system('/usr/local/nginx/sbin/nginx -s reload')
        return JsonResponse({"code":200})
    else:
        pass

def edit_file(request):
    ret = request.session.get('is_login', False)
    if ret:
        file_id = request.POST.get('id')
        file_name = request.POST.get('filename')
        file_type = request.POST.get('type')
        file_discription = request.POST.get('discription')
        upload_file = request.FILES['file']
        Rules.objects.filter(r_file=file_name).delete()
        os.remove(os.path.join('/usr/local/nginx/conf/rules',file_name))
        with open(os.path.join('/usr/local/nginx/conf/rules',upload_file.name),'wb+') as f:
            for chunk in upload_file.chunks():
                f.write(chunk)
        rule_files_list.objects.filter(id__exact=file_id).update(f_name=upload_file.name,f_type=file_type,f_date=datetime.date.today(),f_discription=file_discription)
        mparser = msc_pyparser.MSCParser()
        data = upload_file.read()
        mparser.parser.parse(data)
        num = 1
        for line in mparser.configlines:
            if line['type'] == 'SecRule':
                name = file_type + str(num)
                actions = line['actions']
                for x in actions:
                    if x['act_name'] == 'id':
                        id = x['act_arg']
                        break
                Rules.objects.create(r_id=id, r_name=name, r_type=file_type, r_date=datetime.date.today(),
                                     r_discription=file_discription, r_file=upload_file.name)
                num += 1
        with open('/usr/local/nginx/conf/rules/user_rule_ban.conf', 'w') as f:
            for line in Rules.objects.filter(r_selected__exact=0):
                f.write('SecRuleRemoveById' + ' ' + line.r_id + '\n')
        os.system('/usr/local/nginx/sbin/nginx -s reload')
        return JsonResponse({"code": 200})
    else:
        pass



