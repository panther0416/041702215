# -*- coding: utf-8 -*-
import cpca
import re
import json
class OldFile(str):
    name,phone,address,level='','',[],''
    def __init__(self,str):
        self.level=str.split('!')[0]
        self.str=str.split('!')[1]
    def find_name(self):
        name_pattern='^[\u4e00-\u9fa5]*'
        if(re.match(name_pattern,self.str)):
            self.name=re.match(name_pattern,self.str).group()
        self.str=self.str.replace(self.name,"")
        return self.name
    def find_phone(self):
        phone_pattern='\d{11}'
        if(re.search(phone_pattern,self.str)):
            self.phone=re.search(phone_pattern,self.str).group()
        self.str=self.str.replace(self.phone,"")
        return self.phone
    def find_address(self):
        self.str=self.str.strip(',.')
        addr=cpca.transform([self.str],cut=False)
        addr=dict(addr.iloc[0,0:4])     #DataFrame格式转换成dict格式
        self.address.append(addr["省"])
        self.address.append(addr["市"])
        self.address.append(addr["区"])
        detailed_address=addr["地址"]
        
        #街道/镇/乡,详细地址
        if "街道" in detailed_address:
            self.address.append(detailed_address.split("街道")[0]+"街道")
            detailed_address=detailed_address.split("街道")[1]
        elif "镇" in detailed_address:
            self.address.append(detailed_address.split("镇")[0]+"镇")
            detailed_address=detailed_address.split("镇")[1]
        elif "乡" in detailed_address:
            self.address.append(detailed_address.split("乡")[0]+"乡")
            detailed_address=detailed_address.split("乡")[1]
        else:
            self.address.append("")
            
        #七级地址
        if(self.level=='2' or self.level=='3'):
            #街、路、巷
            if "路" in detailed_address:
                self.address.append(detailed_address.split("路")[0]+"路")
                detailed_address=detailed_address.split("路")[1]
            elif "街" in detailed_address:
                self.address.append(detailed_address.split("街")[0]+"街")
                detailed_address=detailed_address.split("街")[1]
            elif "巷" in detailed_address:
                self.address.append(detailed_address.split("乡")[0]+"乡")
                detailed_address=detailed_address.split("乡")[1]
            else:
                self.address.append("")
            #号
            if("号" in detailed_address):
                self.address.append(detailed_address.split("号")[0]+"号")
                self.address.append(detailed_address.split("号")[1])
            else:
                self.address.append(detailed_address)
        else:
            self.address.append(detailed_address)
        return self.address
    def find(self):
        dict={
            "姓名":self.find_name(),
            "手机":self.find_phone(),
            "地址":self.find_address()
              }
        return dict

str=input()
oldfile=OldFile(str)
dict=oldfile.find()
#print(dict)
#转换成json文件
jsonfile=json.dumps(dict)
print(jsonfile)




#处理字符串的其他方法
#提取信息
'''name=re.match("(?P<姓名>^[\u4e00-\u9fa5]*)",str).groupdict()
    phone=re.search("(?P<手机>\d{11})",str).groupdict()'''
#str.strip()函数只处理字符串首尾
#除去信息
'''str.split() 分割后再合并
    re.sub(pattern,replace,str)
    str.replace(xxxx,"")
'''
