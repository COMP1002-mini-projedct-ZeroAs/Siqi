import JSON
import condisplay
import getclassify           
def conclassify(tag):
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
                    
    for content in conList:
        print(*content.keys(),end=":\n")
        for i in content:
            for conPerson in content[i]:
                condisplay.condisplay(conPerson)
                print()
            print()
    if noneDict['None']!="":
        print('None:')
        for person in noneDict['None']:
            condisplay.condisplay(person)  
    return conList                  
conclassify("Location")   
 