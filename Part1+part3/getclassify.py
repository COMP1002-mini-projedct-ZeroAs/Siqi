import JSON
def getclassify(tag):
    tagClass=[]
    f=open("C:\connect\connect.txt","r")
    conDict=dict(JSON.parse(f.read()))
    f.close()
    for person in conDict:
        tagDict=conDict[person]["Tag"]
        if tag in tagDict:
            for i in tagDict[tag]:
                if i not in tagClass:
                    tagClass.append(i)
    return tagClass 