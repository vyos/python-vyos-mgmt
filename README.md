# VyRoute
A python library for VyOS routing setting

作者：Hochikong  
联系我：michellehzg@gmail.com（较少用） or 1097225749@qq.com

这是一个用于设置VyOS路由功能的Python库，目前仅仅提供了静态路由，RIP和OSPF的功能，以后有需要会增加BGP的部分，如果你有兴趣，可以试着clone一份增加你想要的功能，比如BGP和网络接口设置。

在后面我还会继续开发实现VyOS的防火墙、VPN配置的库。

##备注
已经打包好的egg文件在：[https://github.com/Hochikong/vyroute/tree/master/dist](https://github.com/Hochikong/vyroute/tree/master/dist)  

可以下载并用easy_install安装egg包

下面我会给出这个库的使用说明和注意事项：

本库依赖于Exscript库，可以在github上找到

本库基于Apache License2.0协议开源

##设计
这个库主要是为了可编程、满足远程管理VyOS路由功能的需求而编写，目前实现了RIP、静态、OSPF三种AS内部协议配置的功能。  

库中只有两个类，Router和BasicRouter类，BasicRouter继承Router并重写成员方法。当我们使用这个库时，传入具体的VyOS路由的地址、用户名和相应的密码以实例化BasicRouter类，然后我们就可以通过类的成员方法对路由器进行远程控制

和管理员手动操作VyOS一样，首先要登陆VyOS并进入configure模式才能进行配置，配置完毕后要提交并保存才退出管理。

类中有一个status的成员变量，为一个python字典，记录着该路由实例的状态：

	self.__status = {"object": None, "commit": None, "save": None, "configure": None}

在一开始实例化时，所有状态都为none，当用户执行login后，object会变为“login”状态，进入configure模式后，configure会变为“Yes”状态。期间任何对路由实例的配置操作都会把commit和save的状态改为“No”，不过如果前面有尚未提交的修改，后续的修改并不会再次改写commit和save的状态，而是保持“No”。一旦用户打算退出configure模式，如果不加入强制退出的参数，则会检查commit和save的状态，确保两个状态都变为“Yes”才允许退出。如果用户执行logout，所有状态都会变为None，而object会变为“logout”

在用户进入configure模式后，就可以着手配置相关的路由功能，比如设置静态路由等，大部分函数都要输入数据进行配置，在这里我用的是一个python字典作为数据载体，返回的结果也以字典为载体：

	>>> data = {'config':'std'}
	>>> vyos1.delete_route(data)
	{'Error': 'Nonsupport protocols type.'}

因此绝大多数的函数都只有一个data参数，但是各种data的格式是不同的，用户需要按照下面我提供的说明输入才能正确配置，如果数据有错误，由于Exscript的问题，执行函数后会很迟才返回一个超时Error，然后在你执行下个命令时会把前面的错误的原因返回（VyOS返回的错误原因），此时你需要把刚刚的命令再执行一遍：

	>>> vyos1.delete_route({'config':'all'})
	{'Error': InvalidCommandException('Device said:\nset protocols ospf default-information originate always\r\nWARNING: terminal is not fully functional\r\n\r-  (press RETURN)\r\r\r\x07\x1b[m\r\n  Configuration path: [protocols ospf default-information originate always] already exists\x1b[m\r\n\x1b[m\r\n\r[edit]\r\r\nvyos@vyos# elete protocols\r\n\r\n  Invalid command: [elete]\r\n\r\n[edit]\r\r\nvyos@vyos# ',)}
	>>> vyos1.delete_route({'config':'all'})
	{'Result': 'Delete successfully.'}


在这个库中，如果配置成功（不返回错误，但不意味着你配置一定可以起作用，比如你把静态路由的下一跳设错地址，虽然VyOS不会提示你错，但是的确是用不了的）会返回一个字典，键为“Result”，如果是错误则为“Error”：

错误：

	>>> data = {'config':'std'}
	>>> vyos1.delete_route(data)
	{'Error': 'Nonsupport protocols type.'}

正确：

	>>> vyos1.login()
	{'Result': 'Login successfully.'}

当用户使用这个库进行高级开发时可以单单靠结果的键判断是否成功。


#函数解释
##login():  
没有任何参数
  
返回一个字典：  
登陆成功：{'Result': 'Login successfully.'}  
失败：{"Error": "Connect Failed."}  
如果是其他错误则会返回一个字典，其值为相关的python异常

用户使用这个登陆实例化的路由对象，前提是你已经实例化一个路由：

	>>> from vyroute.Router import BasicRouter
	>>> vyos1 = BasicRouter('172.16.77.184','vyos:vyos')
	>>> vyos1.login()
	{'Result': 'Login successfully.'}

##logout()
没有任何参数

返回一个字典：   
退出成功：{"Result": "Logout successfully."}   
如果是其他错误则会返回一个字典，其值为相关的python异常（后面每个函数都有这个，不再重复）  

用户使用这个退出一个路由实例，即close()一个连接：

	>>> vyos1.logout()
	{'Result': 'Logout successfully.'}

##status()
没有任何参数

返回一个字典，返回实例的内部状态

##configure()
没有任何参数

返回一个字典：  
进入成功：{"Result": "Active configure mode successfully."}  
如果你已经在configure模式：{"Error": "In configure mode now!"}  
如果你没有login：{"Error": "Router object not connect to a router."}（后面每个函数都会检查这个，本文档不再重复此部分）

用户使用这个进入configure模式，前提是你已经登入VyOS实例：

	>>> vyos1.configure()
	{'Result': 'Active configure mode successfully.'}


##commit_config()	
没有任何参数  

返回一个字典：  
提交成功：{"Result": "Commit successfully."}  
如果commit为None：{"Error": "You don't need to commit."}  
如果你已经提交过一次：{"Error": "You have committed!"}  
没在configure模式：{"Error": "Router not in configure mode!"}（后面的都会检查，不再重复）

用户使用这个提交配置，前提是你已经在configure模式：

	>>> vyos1.commit_config()
	{'Result': 'Commit successfully.'}

##save_config()
没有任何参数

返回一个字典：  
保存成功：{"Result": "Save successfully."}  
如果save状态为none：{"Error": "You don't need to save."}  
如果已经保存：{"Error": "You have saved!"}  
如果没提交：{"Error": "You need to commit first!"}  

用户用这个来保存配置，前提是你已经提交：

	>>> vyos1.save_config()
	{'Result': 'Save successfully.'}

##exit_config(force=False)
参数force：布尔值True或者False，默认为False，如果force为真，则不管是否已经提交和保存都退出，为假则要求先提交再保存才能退出

返回一个字典：  
退出成功：{"Result": "Exit configure mode successfully."}  
没提交、没保存的返回请参考前面

用户用这个退出configure模式，前提是你在configure模式

##lo(data)  
参数data：字典数据  
数据范例：{'config':'1.1.1.1/32'}

返回一个字典：  
配置成功：{"Result": "Modify successfully."}

用户用这个创建VyOS loopback接口lo的一个新地址（不能修改默认值，与新地址共存），通常用这个地址（除去掩码）作为路由ID

##delete_route(data)
参数data：字典数据  
数据范例：{'config':'rip'/'static'/'ospf'/'all'}  
config的值仅可以为rip、static、ospf和all，all将会删除VyOS中protocols的全部内容，而其他参数会删除对应协议的全部配置内容。因为VyOS中部分条件相同的新设置可以覆盖原有的设置，建议修改某个错误的设置时要用回更正后的原命令修改。

返回一个字典：  
删除成功：{"Result": "Delete successfully."}  
不支持的config值：{"Error": "Nonsupport protocols type."}

用户用这个删除不想要的路由配置内容，但是要慎重使用

##static_route(data)
参数data：字典数据  
数据范例：{'config':{'target':'10.20.10.0/24','next-hop':'10.20.10.1','distance':'1'},}  
这个函数相当于执行set protocols static route next-hop distance

返回一个字典：  
配置成功：{"Result": "Configured successfully"}  

用户用这个设置静态路由，这是静态路由设置的基础

##rip_route(data)
参数data：字典数据  
数据范例：{'config':'192.168.10.0/24',}  
这个函数相当于执行set protocols rip network和set protocols rip redistribute connected

返回一个字典：  
{"Result": "Configured successfully"}

用户用这个来设置RIP协议的路由，执行宣告网络范围和路由重发布

##ospf_area(data)
参数data：字典数据  
数据范例：{'config'：{'area':'0','network':'192.168.10.0/24'},}  
这个函数相当于执行set protocols ospf area network

返回一个字典：
{"Result": "Configured successfully"}

用户用这个来设置OSPF区域和相应的网络

##router_id(data)
参数data：字典数据  
数据范例：{'config':{'id':'1.1.1.1'},}  
这个函数相当于执行set protocols ospf parameters router-id

返回一个字典：  
{"Result": "Configured successfully"}

用户用这个设置路由ID，可以用新增的lo地址去掉掩码来当ID

##ospf_redistribute(data)
参数data：字典数据  
数据范例： {'config':{'type':'2'},}  
这个函数相当于执行set protocols ospf redistribute connected metric-type和set protocols ospf redistribute connected route-map CONNECT

返回一个字典：  
{"Result": "Configured successfully"}

用户用这个来进行路由重发布

##ospf_adjacency()
没有任何参数  
这个函数相当于执行set protocols ospf log-adjacency-changes

返回一个字典：  
{"Result": "Configured successfully"}

用户用这个激活路由协议邻接关系变化日志功能

##ospf\_default\_route(data)
参数data：字典数据  
数据范例：{'config':{'metric':'10','metric-type':'2'},}  
这个函数相当于执行set protocols ospf default-information originate always、set protocols ospf default-information originate metric和set protocols ospf default-information originate metric-type

返回一个字典：  
{"Result": "Configured successfully"}

用户用这个发布默认路由

##ospf\_route\_map(data)
参数data：字典数据
数据范例：{'config':{'rule':'10','interface':'lo'},}  
这个函数相当于执行set policy route-map CONNECT rule action permit和set policy route-map CONNECT rule match interface

返回一个字典：  
{"Result": "Configured successfully"}

用户用这个来设置route-map







   


