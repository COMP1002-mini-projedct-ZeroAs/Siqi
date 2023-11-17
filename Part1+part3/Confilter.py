import getclassify
import condisplay
import JSON
def conFilter(tag,tagCont_list):
    tag_list=tagCont_list.split(",")
    
    for tagCont in tag_list:
        f=open("C:\connect\connect.txt","r")
        conDict=dict(JSON.parse(f.read()))
        f.close()
        conList=[]
        for tagCon in getclassify.getclassify(tag):
            tagDict={tagCon:[]}
            noneDict={'None':[]}
            for connact in conDict:
                #print(connact)
                if tag not in conDict[connact]["Tag"]:
                    noneDict['None'].append(conDict[connact])
                else:    
                    if tagCon in conDict[connact]["Tag"][tag]:
                        tagDict[tagCon].append(conDict[connact])
                    if tagDict not in conList:    
                        conList.append(tagDict)
        print(f"{tagCont}:")
        for content in conList:
            if tagCont in content:
                for person in content[tagCont]:
                    condisplay.condisplay(person)
                    print()
                print()
conFilter("Location","Japan,China")                
                