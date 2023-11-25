import JSON
import TRIE
import re
class Contact:
    tagRefresh,cateRefresh,infroRefresh=True,True,True
    #字典缓存刷新，类型缓存刷新
    tagDict={}
    #tag字典缓存
    categoryDictTemp={}
    infoDict={}
    #类型缓存
    def __init__(self, path: str):
        try:
            handle = open(path, "r")
            self.contacts = JSON.parse(handle.read())
            handle.close()
        except FileNotFoundError:
            self.contacts = {}
        self.filePath = path

    def listAllContact(self):
        print(self.contacts)

    def showOnePeople(self, people: str):
        if people in self.contacts:
            print("Name: ", self.contacts[people]["name"])
            print("Phone Number: ", *self.contacts[people]["number"])
            print("Email: ", *self.contacts[people]["email"])
            for key in self.contacts[people]["tags"]:
                if key!='{{systemDefault':
                    print(key + ": ", *self.contacts[people]["tags"][key])
            print()
        else:
            print(f"No contact found with the name: {people}")

    def addPerson(self, name: str, mode: str, newDatas: list = []):
        # 参数newDatas的结构为 [phoneNumbers, emails, tags]
        def defaultMode():
            self.contacts[name] = {
                "name": name,
                "number": [],
                "email": [],
                "tags": {}
            }

        if mode == "cover" or mode == "update":
            # "cover"模式覆盖现有联系人，"update"模式更新现有联系人
            if mode == "update":
                words = ["number", "email", "tags"]
                for i in range(len(newDatas)):
                    if newDatas[i] == None or len(newDatas[i]) == 0:
                        newDatas[i] = self.contacts[name].get(words[i], [])
            if name in self.contacts:
                self.contacts[name].clear()  # 清除旧数据
            defaultMode()
        elif mode == "blend":
            # "blend"模式混合现有数据和新数据
            if name not in self.contacts:
                defaultMode()

        # 更新电话号码和电子邮件
        self.contacts[name]["number"] = list(set(self.contacts[name].get("number", []) + newDatas[0]))
        self.contacts[name]["email"] = list(set(self.contacts[name].get("email", []) + newDatas[1]))

        # 更新或添加新标签
        for tag, values in newDatas[2].items():
            if tag not in self.contacts[name]["tags"]:
                self.contacts[name]["tags"][tag] = []
            self.contacts[name]["tags"][tag] += values
            self.contacts[name]["tags"][tag] = list(set(self.contacts[name]["tags"][tag]))
            
        #缓存更新    
        Contact.tagRefresh,Contact.cateRefresh=True,True
        info=''
        for keys in self.contacts[name]:
            if type(self.contacts[name][keys])==list:
                for item in self.contacts[name][keys]:
                    info+=item
            elif type(self.contacts[name][keys])==dict:
                for tag in self.contacts[name][keys]:
                    if tag!='{{systemDefault':
                        info+=tag
                        for category in self.contacts[name][keys][tag]:
                            info+=category
            else:
                info+=self.contacts[name][keys]
            info+=chr(0)
        Contact.infoDict[name]=info 
        print(f"Contact '{name}' added/updated successfully.")
    def deletePerson(self, name: str):
        if name in self.contacts:
            del self.contacts[name]
            print(f"Contact '{name}' deleted successfully.")
        else:
            print(f"No contact found with the name: {name}")

    def save(self):
        handle = open(self.filePath, "w")
        handle.write(JSON.stringify(self.contacts))
        handle.close()
        print("Contacts saved to file.")
    
    
    def tagdict(self):
        #生成以tag为key的字典
            tagDict={}
            for name in self.contacts:
                for tag in self.contacts[name]['tags']:
                    for num in range(len(self.contacts[name]['tags'][tag])):
                        if self.contacts[name]['tags'][tag][num] not in  tagDict.keys():
                            tagDict[self.contacts[name]['tags'][tag][num]]=[name]
                        else:
                            tagDict[self.contacts[name]['tags'][tag][num]].append(name)
            Contact.tagDict=tagDict
            Contact.tagRefresh=False                
        
    
    
    def categoryList(self):
        #获得tag下标签
        categoryDict={}
        for name in self.contacts:
            for tag in self.contacts[name]['tags']:
                if tag not in categoryDict.keys():
                    categoryDict[tag]=[]
                for category in self.contacts[name]['tags'][tag]:
                    if category not in categoryDict[tag]:
                        categoryDict[tag].append(category)                
        Contact.categoryDictTemp=categoryDict
        Contact.cateRefresh=False        
    
    
    def tagFilter(self,categoryList:list,exclude:bool=False):
        #过滤表取交集，输出
        if len(categoryList)==0 or categoryList==None:
            for person in self.contacts:
                Contact.showOnePeople(self,person)
            return
        else:    
            if Contact.tagRefresh==True:
                Contact.tagdict(self)    
            tagDict=Contact.tagDict
            set1=set(tagDict.get(categoryList[0],[]))
            for category in categoryList[1:]:
                set2=set(tagDict.get(category,[]))
                set1=set1 & set2
                print(set1)
            if exclude==True:
                for person in self.contacts:
                    if person not in set1:
                        Contact.showOnePeople(self,person)
            else:                
                for person in set1:
                    Contact.showOnePeople(self,person)
            
    def tagSort(self,tag):
        #tag 分类输出
        if Contact.tagRefresh==True:
            Contact.tagdict(self)
        if Contact.cateRefresh==True:
            Contact.categoryList(self)    
        categoryDict=Contact.categoryDictTemp
        tagDict=Contact.tagDict
        if tag not in categoryDict:  
            for name in self.contacts:
                Contact.showOnePeople(self,name)
        else:   
            for category in categoryDict[tag]:
                print(category)
                for person in tagDict[category]:
                    Contact.showOnePeople(self,person)
    
    def infoAdd(self):
        #个人信息合并，用于模糊搜索
        for name in self.contacts:
            info=''
            for keys in self.contacts[name]:
                if type(self.contacts[name][keys])==list:
                    for item in self.contacts[name][keys]:
                        info+=item
                elif type(self.contacts[name][keys])==dict:
                    for tag in self.contacts[name][keys]:
                            for category in self.contacts[name][keys][tag]:
                                info+=category
                else:
                    info+=self.contacts[name][keys]
                info+=chr(0)
            Contact.infoDict[name]=info.lower()  
            Contact.infroRefresh=False
            
            
    def fuzzySerch(self,search:str):
        if Contact.infroRefresh==True:
            Contact.infoAdd(self)
        print(Contact.infoDict)
        if type(search)==list:
            root=TRIE.TrieNode()
            TRIE.buildTrie(root,search)                          
            TRIE.buildFailPointers(root)
            for name in Contact.infoDict:
                if(TRIE.search(Contact.infoDict[name],root)):
                    Contact.showOnePeople(self,name) 
        else:
            search=search.lower()
            for name in Contact.infoDict:
                if search in Contact.infoDict[name]:
                    Contact.showOnePeople(self,name)
    
    
    def getUserInput(self):
        #输入确认
        inputN = 0
        while(inputN<3):
            sth=input("Y/N >>> ")
            if(sth=="y" or sth=="Y"):
                return True
            elif(sth=="n" or sth=="N"):
                return False
        return False
    
    
def deep_copy(deepDict):
    dictType=type(deepDict)
    newDict=None
    if dictType==dict:
        newDict={}
    else:
        newDict=[]
    for keys in deepDict:
        if dictType==dict:
            if type(deepDict[keys])==list or type(deepDict[keys])==dict:
                newDict[keys]=deep_copy(deepDict[keys])
            else:
                newDict[keys]=deepDict[keys]
        else:
            if type(keys)==list or type(keys)==dict:
                newDict.append(deep_copy(keys))
            else:
                newDict.append(keys)   
    return newDict
    
class Console:
    def __init__(self,path:str):
        self.con = Contact(path)
    def waitForInput(self):
        res=True
        try:
            while(res):
                command = input("CONTACT >>> ")
                res=self.exec(command)
        except KeyboardInterrupt:
            print("\n\nSAVING&QUITTING...")
            self.con.save()
        else:
            print("\n\nSAVING&QUITTING...")
            self.con.save()
    def showHelp(self,showWhich=[]):
        """
        显示控制台命令的帮助信息。
        """
        print("CONTACT MANAGEMENT SYSTEM COMMANDS")
        print("==================================")
        arr = [
            [
                "List Contacts: L [-fe [tag1, tag2, ...]] [-f [tag1, tag2]] [tag]",
                "  -f: Filter tags",
                "  -fe: Exclude tags",
                "  [tag]: Filter by one tag"
            ],
            [
                "Add Contact: A [-n [name]] [-p [phone1, phone2, ...]] [-e [email1, email2, ...]] [-c [tag1, tag2, ...]] [-y]",
                "  -n: Name of the contact",
                "  -p: Phone numbers",
                "  -e: Email addresses",
                "  -c: Custom tags",
                "  -y: Silent mode",
                "  -mode: 'b' for merge, 'u' for update, otherwise cover"
            ],
            [
                "Fuzzy Search: F [-q [querys]] [query]",
                "  -q: Query terms, seperated by comma or space",
                "  query: search only one query"
            ],
            [
                "Modify Contact: M -n [name] [-o [new name]] [-p [phone]] [-e [email]] [-c [tag]]",
                "  -n: Name of the contact to modify",
                "  -o: New name",
                "  -p: Modify phone number",
                "  -e: Modify email",
                "  -c: Modify tag"
            ],
            [
                "Delete Contact: D [name]",
                "  [name]: Name of the contact to delete"
            ]
        ]
        if(len(showWhich)==0):
            showWhich = range(len(arr))
        for i in showWhich:
            for j in arr[i]:
                print(j)
        print("==================================")
    def exec(self,command:str):
        if(len(command)==0):
           return True           #miss input
        if(command[-1]!=" "):
            command+=" "
        strLen = len(command)
        if(strLen==0):
            return
        quoting=[]#space in quote doesnt split
        qLen = 0
        #modes:
        #   L: List
        #   A: Add
        mode = command[0]
        types = []
        curDataInput = ""
        tmpValue = ""
        ind = 1
        while(ind<strLen):
            if(command[ind]=="\"" or command[ind]=="'"):
                # type of quote marks:
                #    "''"
                #    "'"
                if(qLen>0 and quoting[qLen-1]==command[ind]):
                    quoting.pop()
                    qLen-=1
                elif(qLen>1 and quoting[qLen-2]==command[ind]):
                    quoting.pop()
                    quoting.pop()
                    qLen-=2
                else:
                    quoting.append(command[ind])
                    qLen+=1
                if(qLen==0 and len(tmpValue)>0 and (tmpValue[0]=="\"" or tmpValue[0]=="'")):
                    tmpValue = tmpValue[1:-1]
            if(qLen==0):
                if(command[ind]==" " or command[ind]==","):
                    if(len(tmpValue)>0):
                        if(tmpValue[0]=="-"):
                            types.append([tmpValue,[]])
                        else:
                            if(len(types)>0):
                                types[-1][1].append(tmpValue)
                            else:
                                curDataInput = tmpValue
                        tmpValue=""
                else:
                    tmpValue+=command[ind]
            else:
                tmpValue+=command[ind]
            ind+=1
        if(mode=="L"):
            lst=[]
            if(len(types)>0):
                for t in types[0][1]:
                    lst.append(t)
                self.con.tagFilter(lst,types[0][0]=="-fe")
            elif(curDataInput==""):
                self.con.tagFilter(lst,True)
            else:
                self.con.tagSort(curDataInput)
        elif(mode=="A"):
            name = None
            create = [None,None,None]
            silence = False
            cover = False
            update = False
            for t in types:
                if(t[0]=="-p"):
                    create[0] = t[1]
                elif(t[0]=="-e"):
                    create[1] = t[1]
                elif(t[0]=="-c"):
                    create[2] = {"{{systemDefault":t[1]}
                elif(t[0]=="-y"):
                    silence = True
                elif(t[0]=="-n" and len(t[1])>0):
                    name = t[1][0]
                elif(t[0]=="-mode" and len(t[1])>0):
                    if(t[1][0]!="b"):
                        cover=True
                    if(t[1][0]=="u"):
                        update=True
            #check some values
            if(name==None):
                if(not silence):
                    while(name==None or len(name)==0):
                        name = input("Enter Name >>> ")
                else:
                    print("Name Invalid")
                    return True                  #non-exist
            if(not self.con.contacts.get(name) and update):
                print("User does not exists.")
                return True                     #non-exist
            if(not silence and self.con.contacts.get(name) and not cover):
                print("Already exists, cover? (Y/N)")
                if(self.con.getUserInput()):
                    cover=True
            #enter phoneNumber and others
            for i in range(0,2):
                if(create[i]==None):
                    create[i]=[]
                    if(not silence):
                        while(True):
                            pNumber = input(["Number(s) (Press Enter To End): ","Email(s) (Press Enter To End): "][i])
                            if(i==0 and (not re.match("^[0-9]*$",pNumber) or len(pNumber)==0)):
                                break
                            elif(i==1 and (not re.match("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-\.]+\.[a-zA-Z0-9-.]+",pNumber) or len(pNumber)==0)):
                                break
                            create[i].append(pNumber)

                create[i] = list(set(create[i]))#UNIQUE
            #enter Custom Fields & Categories
            if(create[2]==None):
                create[2]={}
                if(not silence):
                    while(True):
                        pField = input("Custom Field (Press Enter To End): ")
                        pVal = input("Categories (Press Enter To End): ")
                        if(len(pVal)==0):
                            break
                        if(pField[:2]=="{{"):
                            pField=pField[2:]
                        if(len(pField)==0):
                            pField="{{systemDefault"
                        create[2][pField] = create[2].get(pField,[])
                        create[2][pField].append(pVal)
            if(cover):
                if(update):
                    cover="update"
                else:
                    cover="cover"
            else:
                cover="blend"
            self.con.addPerson(name,cover,create)
        elif(mode == "F"):
            searchWords = None
            if(len(types)>0 and types[0][0]=="-q"):
                searchWords=types[0][1]
                ind_tmp = len(searchWords)-1
                while(ind_tmp>=0):
                    searchWords[ind_tmp] = searchWords[ind_tmp].lower()
                    ind_tmp-=1
            else:
                searchWords = curDataInput
                if(len(curDataInput)==0):
                    print("Invalid query!")
                    self.showHelp([2])
            #print(searchWords)
            self.con.fuzzySerch(searchWords)
        elif(mode == "M"):
            moded = {}
            lastCommand = "-n"
            name = ""
            phone = None#modify only one phone number
            email = None#modify only one email number
            oriInformation:dict = None
            modTag = None
            modTagOnce = None#mod a tag's which category
            for t in types:
                if(t[0]=="-o" and len(t[1])>0):
                    moded[lastCommand] = t[1]
                elif(t[0]=="-n" and len(t[1])>0):
                    lastCommand=t[0]
                    name = t[1][0]
                elif((t[0]=="-p" or t[0]=="-e")):
                    lastCommand=t[0]
                    if(len(t[1])>0):
                        if(t[0]=="-p"):
                            phone=t[1][0]
                        else:
                            email=t[1][0]
                elif(t[0]=="-c" and len(t[1])>0):
                    lastCommand=t[0]
                    modTag = t[1][0]
                    if(len(t[1])>1):
                        modTagOnce = t[1][1]
            if(len(name)==0 or not self.con.contacts.get(name)):
                self.showHelp([3])
                return True
            else:
                def basicIndex(lst,val):
                    l = len(lst)
                    i_ = 0
                    while(i_<l):
                        if lst[i_] == val:
                            return i_
                        i_+=1
                    return None
                #create a copy to avoid change to originalData
                oriInformation = deep_copy(self.con.contacts.get(name))
                if(moded.get("-n")):
                    name=moded["-n"][0]
                if(moded.get("-p")):
                    if(phone):
                        pos = basicIndex(oriInformation["number"],phone)
                        if(pos):
                            oriInformation["number"][pos]=moded["-p"][0]
                    else:
                        oriInformation["number"]=moded["-p"]
                if(moded.get("-e")):
                    if(email):
                        pos = basicIndex(oriInformation["email"],email)
                        if(pos):
                            oriInformation["email"][pos]=moded["-e"][0]
                    else:
                        oriInformation["email"]=moded["-e"]
                if(moded.get("-c")):
                    if(modTagOnce):
                        pos = basicIndex(oriInformation["tags"][modTag],modTagOnce)
                        if(pos):
                            oriInformation["tags"][modTag][pos]=moded["-c"][0]
                    else:
                        oriInformation["tags"][modTag] = moded["-c"]
                for number in oriInformation["number"]:
                    if(not re.match("^[0-9]*$",number)):
                        print("Invalid phone number modification")
                        return True
                for email in oriInformation["email"]:
                    if(not re.match("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",email)):
                        print("Invalid email modification")
                        return True
                self.con.deletePerson(oriInformation["name"])
                self.con.addPerson(name,"cover",[oriInformation["number"],oriInformation["email"],oriInformation["tags"]])
        elif(mode=="D"):
            if(len(curDataInput)==0):
                self.showHelp([4])
                return True
            self.con.deletePerson(curDataInput)
        elif(mode=="H"):
            query_ = []
            for t in types:
                if(t[0]=="-q" and len(t[1])>0):
                    query_ = t[1]
                    break
            try:
                for i in range(len(query_)):
                    query_[i] = int(query_[i])
            except:
                print("Invalid parameter")
            else:
                self.showHelp(query_)
        else:
            print("Invalid Command, please use 'H' to get help.")
            print("Do you want to continue? (Y/N)")
            return self.con.getUserInput()
        return True
    
    
con = Console("./o.O")
con.waitForInput()
        