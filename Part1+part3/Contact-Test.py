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
    noneList=[]
    coverOption=False
    coverName=''
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
        condiction=False
        for name in Conncact.getPhone():
            if phone in Conncact.getPhone()[name]:
                condiction=True
                break
        print(name)    
        if condiction==True:            
            print(f"This phone:{phone} already exist or recreate?")
            option=Conncact.phoneoptioninput()
            if option=='Recreate':
                return Conncact.output(self)
            elif option=='Cover':
                coverOption=True
                coverName=name
                Conncact.phoneList.append(phone)
                return Conncact.phoneList,coverName,coverOption
        else:               
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
        if tagCont=="":
            return Conncact.tagCont_edit()
        else: 
            Conncact.tagContList.append(tagCont)
            if Conncact.continue_Judge()==True:
                return Conncact.tagCont_edit()
            else:
                return Conncact.tagContList    
    def tag_edit(self):
        tagClass=input("Input the tag:")
        if tagClass=="":
            return Conncact.tag_edit(self)
        else:
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
    def optioninput():
        option=input("Recreate, Cover or Merge?").capitalize()
        if option=='Merge':
            return option
        elif option=='Recreate':
            return option
        elif option=='Cover':
            return option
        else:
            return Conncact.optioninput() 
    def phoneoptioninput():
        option=input("Recreate or Cover?").capitalize()
        if option=='Recreate':
            return option
        elif option=='Cover':
            return option
        else:
            return Conncact.optioninput()         
    def getPhone():
        phoneList={}
        for name in Conncact.contDict:
            for phone in Conncact.contDict[name]['Phone-num']:
                if phone not in list(phoneList.values()):
                    if name in list(phoneList.keys()):
                        phoneList[name].append(phone)
                    else:
                        tempDict={name:[phone]}
                        phoneList.update(tempDict)        
        return phoneList                                
    def output(self):                                       #Create connact
        self.n=input("Input name:")
        if self.n in Conncact.contDict:
            print("This name already exist, recreate or merge?")
            operateType=Conncact.optioninput()
            if operateType=='Recreate':
                return Conncact.output(self)
            elif operateType=='Cover':
                Conncact.coverOption=True 
                Conncact.coverName=self.n   
            elif operateType=='Merge':
                partList=['Phone-num','Email','Tag','Remark']
                for part in partList:
                    Conncact.updateInfo(self,self.n,part)
                return    
        self.p,name,condition=Conncact.phone_check(self)
        self.e=Conncact.eamil_check(self)
        self.t=Conncact.tag_edit(self)
        self.r=input("Input remark:")
        cont={self.n:{f'Name':self.n,'Phone-num':self.p,'Email':self.e,'Tag':self.t,'Remark':self.r}}
        return cont,name,condition
    def fileinput(self):
        tempdict,name,condition=Conncact.output(self)
        if condition==True:
            print(name)
            Conncact.contDict.pop(name)
        Conncact.contDict.update(tempdict)
        f=open("C:\connect\connect.txt","w+")
        f.write(str(Conncact.contDict))
        f.close()
        f=open("C:\connect\connect.txt","r")
        cont=f.read()
        f.close()
        Conncact.contDict=dict(JSON.parse(cont))
        return Conncact.contDict
    def getInfo(self):
        for person in Conncact.contDict:
            Conncact.personInfo.append(Conncact.contDict[person])
        return Conncact.personInfo
    def infoList(self,name):
        infoDict=Conncact.contDict[name]
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
    def printall(self):                         #print all information
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
                          
    def updateInfo(self,name,part=None):                                                  #update information
        if part==None:
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
            if tagtype in self.t:
                for contant in tagDict[tagtype]:
                    if contant not in tagList:
                        tagList.append(contant)
            else:
                if name not in Conncact.noneList:
                    Conncact.noneList.append(name)          
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
            if tagtype in tagDict:
                if tagCont in tagDict[tagtype]:
                    nameList.append(name)
            else:
                if name not in Conncact.noneList:
                    Conncact.noneList.append(name)
                        
        return nameList
    def tagClassify(self,tagtype):                              #tagClassify
        for tagCont in Conncact.tagGet(self,tagtype):
            print(f'{tagCont}:')
            for name in Conncact.taggfilter(self,tagtype,tagCont):
                Conncact.printInfo(self,name)    
                print()    
        print("None:")
        for name in Conncact.noneList:
            Conncact.printInfo(self,name)
            print()
    def filterPrint(self,tagtype,tagCont):
        nameList=Conncact.taggfilter(self,tagtype,tagCont)
        print(tagCont)
        for name in nameList:
            Conncact.printInfo(self,name)
            print()   
    def tagClass_get(self):
        tagClassList=[]
        for name in Conncact.contDict:
            for tagClass in Conncact.contDict[name]['Tag']:
                if tagClass not in tagClassList:
                    tagClassList.append(tagClass)
        return tagClassList                   
    def tag_input(self):
        tagClass=input("Input the tag:")
        tagClassList=Conncact.tagClass_get(self)
        if tagClass not  in tagClassList:
            print("No such tag")
            return Conncact.tag_input(self)
        else:
            tagTemp={tagClass:Conncact.tagCont_edit()}
            Conncact.tagContList=[]
            Conncact.tagDict.update(tagTemp)
            print("Whether to add a new tag?")
            if Conncact.continue_Judge()==True:
                return Conncact.tag_input(self)
            else:
                return Conncact.tagDict
    def multiFilter(self):
        tagList=[]
        tagDict=Conncact.tag_input(self)
        tagDict.pop('{{systemDefault')
        tagList=tagDict
        nameset=[]
        for tag in tagList:
            tagList[tag]
            for tagCont in tagList[tag]:
                set1=set(Conncact.taggfilter(self,tag,tagCont))
                nameset.append(set1)
        return nameset        
            
    def multifilterPrint(self):                     #filter
        nameset=Conncact.multiFilter(self)
        set1=nameset.pop(0)
        nameList=list(set1.intersection(*nameset))
        if nameList!=[]:
            for name in nameList:
                Conncact.printInfo(self,name)
                print()        
        else:
            print("None")        
con1=Conncact(1,1,1,1,1)
#for name in Conncact.getPhone():
    #print(list(Conncact.getPhone()[name]))
#con1.updateInfo('Zhang')
#con1.filterPrint('Location','China') 
con1.fileinput()
con1.printall()
#写代码的是小丑，超级大傻逼，代码写的像答辩。
#写part4的是大佬，代码超级美观，安全，高效

    