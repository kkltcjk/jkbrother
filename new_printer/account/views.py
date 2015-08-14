# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from configuration.models import BetaApply, Designer_User, Vender_User 
from utility.AccountHandler import Verification, UserManager
from conf import config 

import json
import urllib, urllib2
import re
import time


# Create your views here.

def check_phone(request):
    '''
    description:验证手机号是否能注册
    params:phone
    return:SUCCESS
    '''
    if request.method == 'GET':
        #phone = request.GET.get('phone')
        phone = '15957440169'
        result = Verification().is_phone_exist(phone)
        if result == 'C':
            conf = {'status':'FAILURE'}
        elif result == 'B':
            conf = {'status':'Beta is existed'}
        else:
            conf = {'status':'SUCCESS'} 
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404


def send_verify_message(request):
    '''
    description:发送验证短信
    params:phone
    return:SUCCESS
    '''
    if request.method == 'GET':
        phone = '15957440169'
        verification_code = Verification().ramdon_dig(phone)
        request.session['phone_verify'] = '224662'#verification_code
        request.session['phone_number'] = phone
        
        verification_string = u'您的验证码是【%s】。请不要把验证码泄露给其他人。如非本人操作，可不用理会！' % verification_code
        print verification_code 
        verify_data = {'account': config.ACCOUNT,
                'password': config.PASSWORD,
                'mobile': phone,
                'content': verification_string.encode("utf-8")
                }
        conf = {}
        try:
            verify_data_urlencode = urllib.urlencode(verify_data)
            req = urllib2.Request(url=config.VERIFY_PHONE_URL, data=verify_data_urlencode)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            rer = re.compile(r'(?<=<code>)(.+?)(?=</code>)').search(res)
            if rer.group(0) == '2': 
                conf = {'state': 'SUCCESS'}
            else:
                conf = {'state': 'FAILURE'}
        except Exception as e:
            print e
            conf = {'state': 'FAILURE'}
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404


def beta_apply(request):
    '''
    description:内测申请
    params: phone,verification_code,identity,
    return: SUCCESS
    '''
    if request.method == 'GET':
        phone = '15957440169'
        verification_code = '224662'
        identity = 'V'
        session_verification_code = request.session['phone_verify']
        session_phone = request.session['phone_number']
        ISOTIMEFORMAT='%Y-%m-%d %X'
        date = time.strftime(ISOTIMEFORMAT, time.localtime())
        conf = {}
        if verification_code == session_verification_code:
            beta = BetaApply(phone=phone, InvitationCode='0811', 
                    identity = identity, apply_time = date)
            beta.save()
            conf = {'status':'SUCCESS'}
        else:
            conf = {'status':'FAILURE'}
        del request.session['phone_verify']
        del request.session['phone_number']
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404


def check_code(request):
    '''
    description:验证邀请码
    params:phone,code
    return: SUCCESS
    '''
    if request.method == 'GET':
        phone = '15957440169'
        code = '0811'
        request.session['phone_register'] = phone
        result = Verification().isright_InvitationCode(phone,code)
        conf = {}
        if (result):
            conf = {'status':'SUCCESS'}
        else:
            conf = {'status':'FAILURE'}
        return HttpResponse(json.dumps(conf))


def u_register(request):
    '''
    description:用户注册
    params:username,password,   phone
    '''
    if request.method == 'GET':
        username = 'www'
        password = '111'
        phone = request.session['phone_register']
        beta = BetaApply.objects.get(phone=phone)
        identity = beta.identity
        conf = {}
        result = UserManager().user_register(phone, password, username, identity)
        conf = {'status':result}
        del request.session['phone_register']
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404


def u_login(request):
    '''
    description:用户登录
    params: phone or username, password
    return:
    '''
    if request.method == 'GET':
        username = '15957440169'
        password = '111'
        conf = {}
        try:
            u = authenticate(username=username, password=password)
            if u.is_active:
                login(request, u)
                identity = UserManager().user_which(u)
                if identity =='D':
                    conf = {'status':'D'}
                elif identity =='V':
                    conf = {'status':'V'}
                else:
                    conf = {'status':'None'}
        except Exception as e:
            conf = {'status':'FAILURE'}
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404


def u_forgetpwd(request):
    '''
    desctiption:忘记密码,验证身份
    params: phone, verification_code
    return: SUCCESS
    '''
    if request.method == 'GET':
        phone = '' 
        verification_code = ''
        session_verification_code = request.session['phone_verify']
        conf = {}
        if verification_code == session_verification_code:
            conf = {'status':'SUCCESS'}
        else:
            conf = {'status':'FAILURE'}
        del request.session['phone_verify']
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404


def u_resetpwd(request):
    '''
    description:设置新密码
    params: phone
    return:
    '''
    if request.method == 'GET':
        password = '11'
        session_phone = request.session['phone_number']
        conf = {} 
        result = UserManager().user_reset_pwd(session_phone,password)
        #重置密码成功
        if result == 'SUCCESS':
            #登录
            u = authenticate(username=session_phone, password=password)
            if u.is_active:
                login(request, u)
                identity = UserManager().user_which(u)
                if identity == 'D':
                    conf = {'status':'D'}
                elif identity == 'V':
                    conf = {'status':'V'}
                else:
                    conf = {'status':'None'}
            else:
                conf = {'status':'login error'}
        else:
            conf = {'status':'reset password error'}
        return HttpResponse(json.dumps(conf))

    else:
        raise Http404


@login_required
def u_logout(request):
    '''
    description:用户注销
    params:
    return: SUCCESS
    '''
    logout(request)
    conf = {'status':'SUCCESS'}
    return HttpResponse(json.dumps(conf))


@login_required
def u_change_phone(request):
    '''
    description:修改绑定手机
    params:user, phone
    return:SUCCESS
    '''
    if request.method == 'GET':
        phone = ''
        user = request.user
        result = UserManager().user_change_phone(user, phone)
        conf = {}
        if (result):
            identity = UserManager().user_which(user)
            if identity == 'D':
                d = Designer_User.objects.filter(user=user).update(phone=phone)
                conf = {'status':'SUCCESS'} 
            elif identity == 'V':
                v = Vender_User.objects.filter(user=user).update(phone=phone)
                conf = {'status':'SUCCESS'}
            else:
                conf = {'status':'xx_user failure'}
        else:
            conf = {'status':'auth_user failure'}
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404

@login_required 
def u_change_username(request):
    '''
    description:修改用户名
    params: user, username
    return:
    '''
    if request.method == 'GET':
        username = 'testwangjh'
        user = request.user
        conf = {}
        identity = UserManager().user_which(user)
        if identity == 'D':
            d = Designer_User.objects.filter(user=user).update(designername=username)
            conf = {'status':'SUCCESS'}
        elif identity == 'V':
            v = Vender_User.objects.filter(user=user).update(vendername=username)
            conf = {'status':'SUCCESS'}
        else:
            conf = {'status':'FAILURE'}
        return HttpResponse(json.dumps(conf))
    else:   
        raise Http404

@login_required
def u_alipay(request):
    '''
    description:操作支付宝账号
    params:
    return:
    '''
    if request.method == 'GET':
        alipay = '152@qc'
        user = request.user
        conf = {}
        d = Designer_User.objects.filter(user=user).update(alipay=alipay)
        if d>=1:
            conf = {'status':alipay}
        else:
            conf = {'status':'FAILURE'}
        return HttpResponse(json.dumps(conf))
    else:
        raise Http404

@login_required
def u_img(request):
    '''
    description:操作头像
    params:
    return:
    '''