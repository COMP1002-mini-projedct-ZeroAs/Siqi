import re
import JSON

class Info:
    
    f=open("C:\connect\connect.txt","r")
    connect=f.read()
    infodict=dict(JSON.parse(connect))
    
    def __init__(self,infodict):
        self.d=infodict
           
class Conncact(Info):
    f=open("C:\connect\connect.txt","r")
    conTemp=f.read()
    f.close()
    emailList=[]
    phoneList=[]
    personInfo=[]
    tagContList=[]
    contDict={}
    contDict.update(dict(JSON.parse(conTemp)))
    tagDict={'{{systemDefault':['{{Everyone']}
    def __init__(self,name,phone,email,tag,remarks):
        self.n=name
        self.p=phone
        self.e=email
        self.t=tag
        self.r=remarks
    def continue_Judge():    
        conInput=input("Input Yes or No to continue:").capitalize()
        if conInput=="Yes":
            return True
        elif conInput=="No":
            return False
        else:
            return Conncact.continue_Judge()
    def eamil_check(self):
        email=input("Input your email:")
        emCheck=re.search("([a-zA-Z0-9]*)@([a-z0-9]*).([a-z]*)",email)
        if emCheck!=None and email!="":  
            Conncact.emailList.append(email)
            if Conncact.continue_Judge()==True:
                return Conncact.eamil_check(self)
            else: 
                return  Conncact.emailList
        else:
            return Conncact.eamil_check(self)
    def phone_check(self):
        phone=input("Input your phone:")
        PhoCheck=re.search("\D",phone) 
        if PhoCheck==None and phone!="":
            Conncact.phoneList.append(phone)
            if Conncact.continue_Judge()==True:
                return Conncact.phone_check(self)
            else:
                return Conncact.phoneList
        else:
            return Conncact.phone_check(self)
    def tagCont_edit():
        tagCont=input("Input tag Contant:") 
        Conncact.tagContList.append(tagCont)
        if Conncact.continue_Judge()==True:
            return Conncact.tagCont_edit()
        else:
            return Conncact.tagContList    
    def tag_edit(self):
        tagClass=input("Input the tag:")
        tagTemp={tagClass:Conncact.tagCont_edit()}
        Conncact.tagContList=[]
        Conncact.tagDict.update(tagTemp)
        print("Whether to add a new tag?")
        if Conncact.continue_Judge()==True:
            return Conncact.tag_edit(self)
        else:
            return Conncact.tagDict
    def itemdel(self,list1):
        item=int(input("Which part to delet(Input number of part):"))
        if item in range(1,len(list1)+1):
            list1.pop(item-1)
        else:
            return Conncact.itemdel(self,list1)        
    def output(self):
        self.n=input("Input name:")
        self.p=Conncact.phone_check(self)
        self.e=Conncact.eamil_check(self)
        self.t=Conncact.tag_edit(self)
        self.r=input("Input remark:")
        cont={self.n:{f'Name':self.n,'Phone-num':self.p,'Email':self.e,'Tag':self.t,'Reamrk':self.r}}
        Conncact.contDict.update(cont)
        f=open("C:\connect\connect.txt","w+")
        f.write(str(Conncact.contDict))
        f.close()
        return Conncact.contDict
    def getInfo(self):
        for person in Conncact.contDict:
            Conncact.personInfo.append(Conncact.contDict[person])
        return Conncact.personInfo
    def infoList(self,name):
        pos=list(Conncact.infodict.keys()).index(name)
        infoDict=Conncact.getInfo(self)[pos]
        self.n=infoDict['Name']
        self.p=infoDict['Phone-num']
        self.e=infoDict['Email']
        self.t=infoDict['Tag']
        self.r=infoDict['Remark']
        return infoDict
    def printInfo(self,name):  
        Conncact.infoList(self,name)  
        print(f"Name:{self.n}")
        print("Phone-num:",end="")
        print(*self.p)
        print("Email:",end="")
        print(*self.e)
        print("Tag:",end=" ")
        for tag in self.t:
            if tag=="{{systemDefault":
                continue
            else:
                print()
                print(f"{tag}:",end="")
                print(*self.t[tag],end=" ")
        print()        
        print(f"Remarks:{self.r}")        
    def printall(self):
        for name in Conncact.contDict:
            Conncact.printInfo(self,name) 
            print()      
    def partCheck(self,name):
        Conncact.personInfo(self,name)   
    def operatetype():
        operatetype=input("Which operatetype you hope to do? Update or Delete?:").capitalize()
        if operatetype=="Update":
            return 'update'
        elif operatetype=='Delete':
            return'delete'
        else:
            return Conncact.operatetype()   
    def tagCheck(tagDict):
        tag=input("Input the tag:")
        if tag in tagDict and tag!="{{systemDefault":
            return tag
        else:
            return Conncact.tagCheck(tagDict)
                          
    def updateInfo(self,name):
        part=input("Input which part you want to update:").capitalize()
        if part not in ['Name','Phone-num','Email','Tag','Remark']:
            return Conncact.updateInfo(self,name)     
        else:    
            infoDict=Conncact.infoList(self,name)
            print(infoDict[part])
            if type(infoDict[part])==str:
                infoDict[part]=input("Input the contant:")
                if Conncact.continue_Judge==True:
                    return Conncact.updateInfo(self,name)
            elif type(infoDict[part])==list:
                if Conncact.operatetype()=='update':
                    if part=='Email':
                        infoDict[part].extend(Conncact.eamil_check(self))
                    else:
                        infoDict[part].extend(Conncact.phone_check(self))
                else:
                    Conncact.itemdel(self,infoDict[part])            
            elif type(infoDict[part])==dict:
                if Conncact.operatetype()=='update':
                    changeTag=Conncact.tagCheck(infoDict[part])
                    if Conncact.operatetype()=='update':
                        infoDict[part][changeTag].extend(Conncact.tagCont_edit())
                    else:
                        Conncact.itemdel(infoDict[part][changeTag])    
                else:
                     changeTag=Conncact.tagCheck(infoDict[part])
                     infoDict[part].pop(changeTag)  
        if Conncact.continue_Judge==True:
            return Conncact.updateInfo(self,name)
        else:
            Conncact.contDict[name]=infoDict
            f=open("C:\connect\connect.txt","w+")
            f.write(str(Conncact.contDict))
            f.close()       
    def tagGet(self,tagtype):
        tagList=[]
        for name in Conncact.contDict:
            Conncact.infoList(self,name)
            tagDict=self.t
            for contant in tagDict[tagtype]:
                if contant not in tagList:
                    tagList.append(contant)
        return tagList
    def tagtypeGet(self):
        tagtypeList=[]
        for name in Conncact.contDict:
            Conncact.infoList(self,name)
            tagtypeDict=self.t
            for tagtype in tagtypeDict:
                tagtypeList.append(tagtype)
        return tagtypeList        
    def taggfilter(self,tagtype,tagCont):
        nameList=[]
        Conncact.tagGet(self,tagtype)
        for name in Conncact.contDict:
            Conncact.infoList(self,name)
            tagDict=self.t
            if tagCont in tagDict[tagtype]:
                nameList.append(name)
        return nameList
    def tagClassify(self,tagtype):
        for tagCont in Conncact.tagGet(self,tagtype):
            print(f'{tagCont}:')
            for name in Conncact.taggfilter(self,tagtype,tagCont):
                Conncact.printInfo(self,name)    
                print()    
    def filterPrint(self,tagtype,tagCont):
        nameList=Conncact.taggfilter(self,tagtype,tagCont)
        print(tagCont)
        for name in nameList:
            Conncact.printInfo(self,name)
            print()
    
            
                
con1=Conncact(1,1,1,1,1)
con1.filterPrint('Location','China') 

   
    