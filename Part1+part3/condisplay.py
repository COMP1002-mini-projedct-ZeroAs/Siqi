def condisplay(dictiter):
    tagCont=""
    tag=""
    listKey=dictiter.keys()
    for i in listKey:
        if type(dictiter[i])==list:
            print(f"{i}:",*dictiter[i])
        elif type(dictiter[i])==dict:
            for j in dictiter[i]:
                if j!="{{systemDefault":
                    for h in dictiter[i][j]:
                        tagCont+=h+" "
                    tagTmp=f"{j}:{tagCont}"
                    tagCont=""
                    tag+=tagTmp+"  "
            print(f"{i}:{tag}")   
        else:        
            print(f"{i}:{dictiter[i]}")
            