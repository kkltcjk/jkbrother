# -*- coding: UTF-8 -*-

from django.db import transaction
from django.contrib.auth.models import User

from configuration.models import BetaApply, Designer_User, Vender_User

import random


class Verification():
    '''
    验证
    '''
    def __init__(self):
        pass


    def is_phone_exist(self, phone):
        '''
        description:手机号是否存在
        params: phone
        return: A可申请内测 B已申请内测未注册 C已注册
        '''
        user = User.objects.filter(username=phone).exists()
        beta = BetaApply.objects.filter(phone=phone).exists()
        if beta == False and user == False:
            return 'A'
        elif beta == True and user == False:
            return 'B'
        elif user == True:
            return 'C'

    
    def ramdon_dig(self, phone):
        '''
        description:产生验证码，对手机号码随机
        params: phone
        return: 
        '''
        string = ''
        r = random.randint(11,44)
        for c in phone[-6:]:
            string += str(self.encrypt(int(c)+r))
        return string

    
    def encrypt(self, n):
        return (n*2 + 4) % 10


    def isright_InvitationCode(self, phone, code):
        '''
        description:邀请码是否正确
        params: phone code
        return: True or False
        '''
        try:
            beta = BetaApply.objects.get(phone = phone)
            if beta.InvitationCode == code:
                return True
            else:
                return False
        except Exception as e:
            return False



class UserManager():
    '''
    用户管理
    '''
    def __init__(self):    
        self.v = Verification()
    
    
    @transaction.atomic
    def user_register(self, phone, password, username, identity):
        '''
        description:用户注册
        params: phone, password, identity, username, 
        return: success or failure
        '''
        result = self.v.is_phone_exist(phone)
        if result == 'C':
            return 'FAILURE'
        else:
            new_user = User.objects.create_user(username=phone, password=password)
            new_user.save()
            if identity == 'D':
                new_designer = Designer_User(phone=phone, designername=username, user=new_user)
                new_designer.save()
            elif identity == 'V':
                new_vender = Vender_User(phone=phone, vendername=username, user=new_user)
                new_vender.save()
            else:
                pass
            return 'SUCCESS'


    def user_which(self, user):
        '''
        description:判断哪种用户
        params: user对象
        return: D or V
        '''
        d_user = Designer_User.objects.filter(user=user).exists()
        if (d_user):
            return 'D'
        else:
            v_user = Vender_User.objects.filter(user=user).exists()
            if (v_user):
                return 'V'
            else:
                return 'None'
        return 'None'


    def user_reset_pwd(self, phone, password):
        '''
        description:重置密码
        params: phone, password
        return: SUCCESS
        '''
        user = User.objects.get(username=phone)
        if user:
            user.set_password(password)
            user.save()
            return 'SUCCESS'
        else:
            return 'FAILURE'


    def user_change_phone(self, user, phone):
        '''
        description:修改绑定手机号
        params: user, new_phone
        return: True,False
        '''
        u = User.objects.filter(id=user.id).update(username=phone)
        if u >= 1:
            return True
        else:
            return False
