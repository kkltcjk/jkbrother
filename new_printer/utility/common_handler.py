import random

from configuration import website as admin_website


class AlgorithmHandler(object):

    def generate_no_repeat_number(self,low,high,number):
        max_value = 100
        return_list = []
        flag = [0] * max_value
        for i in range(number):
            temp_number = random.randint(low,high -  1)
            while flag[temp_number] == 1:
                temp_number = random.randint(low,high - 1)
            flag[temp_number] = 1
            return_list.append(temp_number)
        return return_list


    def get_certain_number_list(self,list,certain_number):
        if(len(list) <= certain_number):
            return list
        else:
            return list[0:certain_number]


class CommonHandler(object):

    def get_file_path(self,part_path):
        path = admin_website.server_path + part_path
        return path


    def utf_to_unicode(self,word):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        unicode_word = word.decode('utf-8')
        return unicode_word