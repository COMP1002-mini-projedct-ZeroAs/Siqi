import JSON
def dicupdate(name):
    f=open("C:\connect\connect.txt",'r+')
    iter_f=dict(JSON.parse(f.read()))
    f.close()
    stop="True"
    tag=""
    tagCon=True
    tagCont=""
    if name not in iter_f:
        return print("No such connact")
    dicLine=iter_f[name]
    listKey=dicLine.keys()
    for i in listKey:
        if type(dicLine[i])==list:
            print(f"{i}:",*dicLine[i])
        elif type(dicLine[i])==dict:
            for j in dicLine[i]:
                if j!="{{systemDefault":
                    for h in dicLine[i][j]:
                        tagCont+=h
                    tagTmp=f"{j}:{tagCont}"
                    tagCont=""
                    tag+=tagTmp+"  "
            print(f"{i}:{tag}")   
        else:        
            print(f"{i}:{dicLine[i]}")
    while 1>0:                
        chanPart=input("Input part you want to change:").capitalize()
        if chanPart in dicLine.keys():
            break
    if type(dicLine[chanPart])==list:
        if dicLine[chanPart]==[]:
            chanCont="all"
        else:    
            chanCont=input("Which part you want change (Input number or all)?")
        if chanCont=="all":
            dicLine[chanPart].clear()
            while stop=="True":
                contant=input("Input contant:")
                dicLine[chanPart].append(contant)
                stop=input("If you want continue (print True or False):")
        else:
            while stop=="True":
                chanPos=int(input("Choose which to change"))
                contant=input("Input contant:")
                dicLine[chanPart][chanPos-1]=contant
                stop=input("If you want continue (print True or False):")         
    elif type(dicLine[chanPart])==dict:
        while 1>0:
            tagChan=input("How do you want to change (Add or Update):").capitalize()
            if tagChan=="Add" or tagChan=="Update":
                break
        if tagChan=="Add":
            while 1>0:
                tag=input("Define tag:").capitalize()
                if tag=="":
                    print("tag cannot be empty")
                else:
                    break    
            conTag=input("tag contant:")
            print(dicLine[chanPart])
            if tag in dicLine[chanPart]:
                dicLine[chanPart][tag].append(conTag)
            else:    
                tagTemp={tag:[conTag]}
                dicLine[chanPart].update(tagTemp)
            while tagCon==True:
                stop=input("If to continue( input True or False?):").capitalize()
                print(stop)
                if stop=="False":
                    tagCon=False
                elif stop=="True":
                    break
        elif tagChan=="Update":
            for j in dicLine[chanPart]:
                if j!="{{systemDefault": 
                    print(j)  
            while 1>0:                         
                tagPart=input("Input part you want to change:").capitalize()
                if tagPart not in dicLine:
                    break     
            print(dicLine[chanPart][tagPart])
            tagListChan=input("Input where you want to change:")
            tagListIndex=input("Input the contant:")
            tagpos=dicLine[chanPart][tagPart].index(tagListChan)
            if tagListIndex=="":
                dicLine[chanPart][tagPart].pop(tagpos)   
            else:     
                dicLine[chanPart][tagPart][tagpos]=tagListIndex       
    else:               
        dicLine[chanPart]=input("Input the content:")
    f=open("C:\connect\connect.txt",'w+') 
    f.write(str(iter_f))       
    f.close()  
dicupdate("Huang")      
        