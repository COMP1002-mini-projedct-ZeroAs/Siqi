import JSON
def conFund():
    f=open("C:\connect\connect.txt","r")
    iter_f=dict(JSON.parse(f.read()))
    f.close()
    tag=""
    tagCont=""
    print(iter_f)
    for connect in iter_f:
        print(connect)
        dicLine=iter_f[connect]
        listKey=dicLine.keys()
        for i in listKey:
            if type(dicLine[i])==list:
                print(f"{i}:",*dicLine[i])
            elif type(dicLine[i])==dict:
                for j in dicLine[i]:
                    if j!="{{systemDefault":
                        for h in dicLine[i][j]:
                            tagCont+=h.lstrip(str({}))+" "
                        tagTmp=f"{j.lstrip(str({}))}:{tagCont}"
                        tagCont=""
                        tag+=tagTmp+"  "
                print(f"{i}:{tag}")
                tag=""    
            else:        
                print(f"{i}:{dicLine[i]}")
        print()
            
conFund()        