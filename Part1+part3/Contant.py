import JSON
import re
def contant():
    phonecon=True
    emCon=True
    phoList=[]
    emList=[]
    stop="False"
    tagCont=True
    tagDict={'{{systemDefault':['{{Everyone']}
    while 1>0:
        name=input("Name:")
        if name=="":
            print("Name can not be empty")
        else:
            break    
    while phonecon==True:
        phonenum=input("Phone-number:")
        
        PhoCheck=re.search("\D",phonenum)
        while 1>0:
            phoCont=input("If you want to continue (input Yes or No)?:").capitalize()
            if phoCont=="Yes" or phoCont=="No":
                break
        if PhoCheck==None and phonenum!="":
            phoList.append(phonenum)    
        if phoCont=="No":
            break
    while emCon==True: 
        email=input("Email:")
        emCheck=re.search("([a-zA-Z0-9]*)@([a-z0-9]*).([a-z]*)",email)
        if emCheck!=None and email!="":
            emList.append(email)
        while 1>0:        
            emCont=input("If you want to continue (input Yes or No)?:").capitalize()
            if emCont=="Yes" or emCont=="No":
                break
        if emCont=="No":
            break   
    while tagCont==True:    
        while 1>0:
            tag=input("Define tag:").capitalize()
            if tag=="":
                print("tag cannot be empty")
            else:
                break    
        conTag=input("tag contant:")
        if tag in tagDict:
            tagDict[tag].append(conTag)
        else:    
            tagTemp={tag:[conTag]}
        tagDict.update(tagTemp)
        while tagCont==True:
            stop=input("If to continue( input True or False?):").capitalize()
            print(stop)
            if stop=="False":
                tagCont=False
            elif stop=="True":
                break  
    remark=input("remark:")
    dictTemp={name:{'Name':name,'Phone-number':phoList,'Email':emList,'Tag':tagDict,'Remark':remark}}
    f=open("C:\connect\connect.txt","r")
    connect=f.read()
    conDict=dict(JSON.parse(connect))
    print(conDict)
    conDict.update(dictTemp)
    f.close()
    f=open("C:\connect\connect.txt","w+")
    f.write(str(conDict))
    f.close()
contant()    