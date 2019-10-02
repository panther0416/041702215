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
        self.address=[]
        self.str=self.str.strip(',.')
        addr=cpca.transform([self.str],cut=False)
        addr=dict(addr.iloc[0,0:4])     #DataFrame格式转换成dict格式
        #直辖市
        if(addr["省"]=="北京市" or addr["省"]=="天津市" or addr["省"]=="重庆市" or addr["省"]=="上海市"):
            addr["省"]=addr["省"].split("市")[0]
        self.address.append(addr["省"])
        self.address.append(addr["市"])
        self.address.append(addr["区"])
        detailed_address=addr["地址"]
        
        #街道/镇/乡/开发区/管委会/合作区,详细地址
        if "街道" in detailed_address:
            self.address.append(detailed_address.split("街道")[0]+"街道")
            detailed_address=detailed_address.replace((detailed_address.split("街道")[0]+"街道"),"")
        elif "镇" in detailed_address:
            self.address.append(detailed_address.split("镇")[0]+"镇")
            detailed_address=detailed_address.replace((detailed_address.split("镇")[0]+"镇"),"")
        elif "乡" in detailed_address:
            self.address.append(detailed_address.split("乡")[0]+"乡")
            detailed_address=detailed_address.replace((detailed_address.split("乡")[0]+"乡"),"")
        elif "苏木" in detailed_address:
            self.address.append(detailed_address.split("苏木")[0]+"苏木")
            detailed_address=detailed_address.replace((detailed_address.split("苏木")[0]+"苏木"),"")
        elif "开发区" in detailed_address:
            self.address.append(detailed_address.split("开发区")[0]+"开发区")
            detailed_address=detailed_address.replace((detailed_address.split("开发区")[0]+"开发区"),"")
        elif "合作区" in detailed_address:
            self.address.append(detailed_address.split("合作区")[0]+"合作区")
            detailed_address=detailed_address.replace((detailed_address.split("合作区")[0]+"合作区"),"")
        else:
            self.address.append("")
            
        #七级地址
        if(self.level=='2' or self.level=='3'):
            #街、路、巷
            if "路" in detailed_address:
                self.address.append(detailed_address.split("路")[0]+"路")
                detailed_address=detailed_address.split("路")[1]
            elif "村" in detailed_address:
                self.address.append(detailed_address.split("村")[0]+"村")
                detailed_address=detailed_address.split("村")[1]
            elif "道" in detailed_address:
                self.address.append(detailed_address.split("道")[0]+"道")
                detailed_address=detailed_address.split("道")[1]
            elif "街" in detailed_address:
                self.address.append(detailed_address.split("街")[0]+"街")
                detailed_address=detailed_address.split("街")[1]
            elif "巷" in detailed_address:
                self.address.append(detailed_address.split("巷")[0]+"巷")
                detailed_address=detailed_address.split("巷")[1]
            elif "小区" in detailed_address:
                self.address.append(detailed_address.split("小区")[0]+"小区")
                detailed_address=detailed_address.split("小区")[1]
            else:
                self.address.append("")
            #号
            if("号楼" in detailed_address):
                self.address.append(detailed_address.split("号楼")[0]+"号楼")
                self.address.append(detailed_address.split("号楼")[1])
            elif("号" in detailed_address):
                self.address.append(detailed_address.split("号")[0]+"号")
                self.address.append(detailed_address.split("号")[1])
            else:
                self.address.append("")
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
def main(str):
    oldfile=OldFile(str)
    dict=oldfile.find()
    jsonfile=json.dumps(dict,ensure_ascii=False)
    print(jsonfile)

while(1):
    try:
        str=input()
        if(str=="END"):
            break
    except:
        break
    main(str)



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
