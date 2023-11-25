import JSON
import TRIE
class Contact:
    tagRefresh,cateRefresh=True,True
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
    
    
    def tagFilter(self,categoryList:list):
        #过滤表取交集，输出
        if Contact.tagRefresh==True:
            Contact.tagdict(self)
        tagDict=Contact.tagDict
        set1=set(tagDict[categoryList[0]])
        for category in categoryList[1:]:
            set2=set(tagDict[category])
            set1=set1 & set2
            print(set1)
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
                        if tag!='{{systemDefault':
                            info+=tag
                            for category in self.contacts[name][keys][tag]:
                                info+=category
                else:
                    info+=self.contacts[name][keys]
                info+=chr(0)
            Contact.infoDict[name]=info.lower()  
            
            
    def furryserch(self,search:str):
        if type(search)==list:
            root=TRIE.TrieNode()
            TRIE.buildTrie(root,search)                          
            TRIE.buildFailPointers(root)
            for name in Contact.infoDict:
                if(TRIE.search(name,root)):
                    Contact.showOnePeople(self,name) 
        else:
            search=search.lower()
            for name in Contact.infoDict:
                if search in Contact.infoDict[name]:
                    Contact.showOnePeople(self,name)
class Console:
    def __init__(self,path:str):
        # 初始化方法，接受一个路径作为参数，创建一个Contact对象
        self.con = Contact(path)
    def waitForInput(self):
        # 等待用户输入的方法，循环执行exec方法，直到用户按下Ctrl+C或者输入空字符串
        res=True
        try:
            while(res):
                command = input("CONTACT >>> ")
                res=self.exec(command)
        except KeyboardInterrupt:
            # 捕获键盘中断异常，保存数据并退出
            print("\n\nSAVING&QUITTING...")
            self.con.save()
        else:
            # 用户输入空字符串，保存数据并退出
            print("\n\nSAVING&QUITTING...")
            self.con.save()
    def exec(self,command:str):
        # 执行用户输入的命令的方法，接受一个字符串作为参数，返回一个布尔值表示是否继续执行
        """
        Args:
            command (str): 用户输入的命令，格式为 mode [-option value,...] data
            【以下的选项仅代表例子，实际的效果请自己写】
            mode (str): 命令的模式，可以是a(添加),d(删除),s(搜索),u(更新),l(列出),q(退出) 
            option (str): 命令的选项，可以是-n(姓名),-p(电话),-e(邮箱),-a(地址),-g(分组),-i(索引)
            value (str): 选项的值，可以是任意字符串，如果包含空格或逗号，需要用引号括起来
            data (str): 命令的数据，可以是任意字符串，如果包含空格或逗号，需要用引号括起来
        Returns:
            bool: 是否继续执行，如果停止，则返回False，否则返回True
        """
        if(len(command)==0):
           # 如果命令为空，返回False
           return False
        if(command[-1]!=" "):
            # 如果命令最后一个字符不是空格，添加一个空格
            command+=" "
        strLen = len(command)
        quoting=[]#space in quote doesnt split
        # 定义一个列表，用于存储引号的类型，用于判断是否在引号内
        qLen = 0
        # 定义一个变量，用于记录引号的数量
        mode = command[0]
        # 定义一个变量，用于存储命令的模式，取命令的第一个字符
        types = []
        # 定义一个列表，用于存储命令的选项和值，格式为[[-option,[value,...]],...]
        curDataInput = ""
        # 定义一个变量，用于存储命令的数据
        tmpValue = ""
        # 定义一个变量，用于临时存储命令的分割部分
        ind = 1
        # 定义一个变量，用于记录命令的当前索引，从1开始
        while(ind<strLen):
            # 循环遍历命令的每个字符
            if(command[ind]=="\"" or command[ind]=="'"):
                # 如果当前字符是双引号或单引号
                # type of quote marks:
                #    "''"
                #    "'"
                if(qLen>0 and quoting[qLen-1]==command[ind]):
                    # 如果引号列表不为空，且最后一个引号和当前引号相同，说明是引号的结束，从列表中弹出
                    quoting.pop()
                    qLen-=1
                elif(qLen>1 and quoting[qLen-2]==command[ind]):
                    # 如果引号列表有两个以上的元素，且倒数第二个引号和当前引号相同，说明是嵌套的引号的结束，从列表中弹出两个元素
                    quoting.pop()
                    quoting.pop()
                    qLen-=2
                else:
                    # 否则，说明是引号的开始，将当前引号加入列表
                    quoting.append(command[ind])
                    qLen+=1
                if(qLen==0 and len(tmpValue)>0 and (tmpValue[0]=="\"" or tmpValue[0]=="'")):
                    # 如果引号列表为空，且临时变量不为空，且临时变量的第一个字符是引号，说明是一个完整的引号字符串，去掉首尾的引号
                    tmpValue = tmpValue[1:-1]
            if(qLen==0):
                # 如果不在引号内
                if(command[ind]==" " or command[ind]==","):
                    # 如果当前字符是空格或逗号，说明是一个分割符
                    if(len(tmpValue)>0):
                        # 如果临时变量不为空，说明是一个有效的部分
                        if(tmpValue[0]=="-"):
                            # 如果临时变量的第一个字符是减号，说明是一个选项，将其加入选项列表，格式为[-option,[]]
                            types.append([tmpValue,[]])
                        else:
                            # 否则，说明是一个值
                            if(len(types)>0):
                                # 如果选项列表不为空，说明是一个选项的值，将其加入选项列表的最后一个元素的值列表，格式为[-option,[value,...]]
                                types[-1][1].append(tmpValue)
                            else:
                                # 否则，说明是命令的数据，将其赋值给数据变量
                                curDataInput = tmpValue
                        # 清空临时变量
                        tmpValue=""
                else:
                    # 如果当前字符不是分割符，将其加入临时变量
                    tmpValue+=command[ind]
            else:
                # 如果在引号内，将当前字符加入临时变量
                tmpValue+=command[ind]
            # 索引加一，继续循环
            ind+=1