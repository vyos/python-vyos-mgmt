#VyRoute

A python library for VyOS routing service setting

Author:Hochikong  
Contact me:1097225749@qq.com(usually use) or michellehzg@gmail.com(Inconvenient in China mainland)  

This python library is used for VyOS routing service configuration,now it only provide static,RIP and 
OSPF configuration function,I will add BGP function if necessary.If you are interested in this project,you can clone and add features you
want,such as BGP and interfaces setting.

I will continue develop other libraries used for firewall and VPN service configuration.

##Comment
I have build an .egg file in [https://github.com/Hochikong/vyroute/tree/master/dist.](https://github.com/Hochikong/vyroute/tree/master/dist.)    

You can clone this reposity install it or just download .egg file to install by easy_install.  

This lib relies on Exscript,you can find it on github.  

MIT opensource license applies to whole library.  

##Requirement
Exscript

##Design
Now,SDN is a technologies trend.Like Openflow and switch controller,they provide us with centralized control and programmable features.But adminstrators of VyOS still need to login the system and 
configure services manually.I need a tool which can configure router service remotely and user can write a program to control the system like SDN controller.So I decide to write this library.Up to now,it just provide static,RIP and OSPF router configuration function.

There are two classes in library:Router and BasicRouter.Router is a parent class,BasicRouter inherit parent class and rewrite its memeber 
methods.When we use this library,we should use VyOS's address and user information to initialize a BasicRouter,then we can use member methods to control the system.
Just like administrators configure services,in this lib you also need to enter configure mode,execute configuration,commit it and save it.

BasicRouter has a member variable(python dictionary) "status",it store a router substance's status.

	self.__status = {"object": None, "commit": None, "save": None, "configure": None}

When it finish initialization,all values in "status" are None.When a 
user login the substance,the value of "object" will change to "login".When the user execute configure(),he will enter configure mode and value of "configure" will change to "Yes",during configure mode,all configuration method will change the value of "commit" and "save" to "no",when user finish a operation but not commit,the following method will not change the value of "commit" and "save".  

When the user want to exit configure mode,only he have commit and save the configuration can he exit configure mode,the value of "commit" and "save" must change to "Yes".If he don't want to save the configuration,he should use exit_config(force=True) to exit.If the user execute logout(),"object" will change to "logout" and the others will change to None.  

When the user enter configure mode,he can use some methods to set up a router.But most of methods should use a configuration data as an input parameter.A configuration data is a python dictionary which include keys and values. Every method will return a result data,similar to the method's input.

	>>> data = {'config':'std'}
	>>> vyos1.delete_route(data)
	{'Error': 'Nonsupport protocols type.'}

Therefore most of methods only have one "data" parameter,but different methods' input data are different.If input data have any mistakes,due to Exscript,the method will return a timeout exception 
after few seconds,then the error reason(from VyOS) will be return when you execute next configuration.So you should execute the former configuration one more time.

	>>> vyos1.delete_route({'config':'all'})
	{'Error': InvalidCommandException('Device said:\nset protocols ospf default-information originate always\r\nWARNING: terminal is not fully functional\r\n\r-  (press RETURN)\r\r\r\x07\x1b[m\r\n  Configuration path: [protocols ospf default-information originate always] already exists\x1b[m\r\n\x1b[m\r\n\r[edit]\r\r\nvyos@vyos# elete protocols\r\n\r\n  Invalid command: [elete]\r\n\r\n[edit]\r\r\nvyos@vyos# ',)}
	>>> vyos1.delete_route({'config':'all'})
	{'Result': 'Delete successfully.'}

In this library,if methods return a information without any mistakes,it doesn't means your configuration is proper(an available router) and it only means your input data is valid.

###Correct:

	>>> vyos1.login()
	{'Result': 'Login successfully.'}

###Error:

	>>> data = {'config':'std'}
	>>> vyos1.delete_route(data)
	{'Error': 'Nonsupport protocols type.'}

In the return of all methods,if it configures successfully,the key of return is "Result".If there any mistakes,the key is"Error".The user can judge whether his configuration is vaild or successful by the only key in return.

##Usage example
We can try to execute a static router confinguration but we don't save it

	>>> from vyroute.Router import BasicRouter
	>>> vyos1 = BasicRouter('172.16.77.184','vyos:vyos')
	>>> vyos1.login()
	{'Result': 'Login successfully.'}
	>>> vyos1.status()
	{'commit': None, 'object': 'login', 'configure': None, 'save': None}
	>>> vyos1.configure()
	{'Result': 'Active configure mode successfully.'}
	>>> static = {'config':{'target':'10.20.10.0/24','next-hop':'10.20.10.1','distance':'1'},}
	>>> vyos1.static_route(static)
	{'Result': 'Configured successfully'}
	>>> vyos1.commit_config()
	{'Result': 'Commit successfully.'}
	>>> vyos1.exit_config(force=True)
	{'Result': 'Exit configure mode successfully.'}
	>>> vyos1.status()
	{'commit': None, 'object': 'login', 'configure': 'No', 'save': None}
	>>> vyos1.logout()
	{'Result': 'Logout successfully.'}
	>>> vyos1.status()
	{'commit': None, 'object': 'logout', 'configure': None, 'save': None}

If you reboot VyOS,you will find the configuration disappears.If you regret your actions,you want to configure again and save it,you can use "vyos1" continue your work.

    >>> vyos1.login()
	{'Result': 'Login successfully.'}
	>>> vyos1.status()
	{'commit': None, 'object': 'login', 'configure': None, 'save': None}
	>>> vyos1.static_route(static)
	{'Error': 'You are not in configure mode.'}
	>>> vyos1.configure()
	{'Result': 'Active configure mode successfully.'}
	>>> vyos1.static_route(static)
	{'Result': 'Configured successfully'}
	>>> vyos1.exit_config()
	{'Error': 'You should commit first.'}
	>>> vyos1.commit_config()
	{'Result': 'Commit successfully.'}
	>>> vyos1.exit_config()
	{'Error': 'You should save first.'}
	>>> vyos1.save_config()
	{'Result': 'Save successfully.'}
	>>> vyos1.status()
	{'commit': 'Yes', 'object': 'login', 'configure': 'Yes', 'save': 'Yes'}
	>>> vyos1.exit_config()
	{'Result': 'Exit configure mode successfully.'}
	>>> vyos1.logout()
	{'Result': 'Logout successfully.'}

Now your configuration will be saved.

#All methods
##login():
No input  

Return a dictionary:   
Login successfully:{'Result': 'Login successfully.'}  
Failed:{"Error": "Connect Failed."}  

If there any mistakes,it will return an dictionary and the value is a python exception.(Every method below has this return when an exception rises,so I will ignore this when I explain following methods.)

You should create a router substance then you can use this method to login.

	>>> from vyroute.Router import BasicRouter
	>>> vyos1 = BasicRouter('172.16.77.184','vyos:vyos')
	>>> vyos1.login()
	{'Result': 'Login successfully.'}

##logout()
No input  

Return a dictionary:  
Logout successfully:{"Result": "Logout successfully."}

This method execute a close() on a connection.

You can use this method logout a router substance.

##status()
No input  

Return a dictionary,return the status of router substance.

##configure()
No input  

Return a dictionary:  
Enter configure mode successfully:{"Result": "Active configure mode successfully."}  
If you already in configure mode:{"Error": "In configure mode now!"}  
If you still not login:{"Error": "Router object not connect to a router."}  

You can use this method enter configure mode,but you should login a substance first.

	>>> vyos1.configure()
	{'Result': 'Active configure mode successfully.'}

##commit_config()
No input  

Return a dictionary:  
Commit successfully:{"Result": "Commit successfully."}  
If "commit" is None:{"Error": "You don't need to commit."}  
If you have commit before:{"Error": "You have committed!"}  
If you are not in configure mode:{"Error": "Router not in configure mode!"}  
If you still not login:{"Error": "Router object not connect to a router."}  

Every methods below will check whether you have login and enter configure mod,if not it will return a error info and you can read the content of return from here.I will ignore these return when I explain following methods.

You can use this method to commit your configuration.

	>>> vyos1.commit_config()
	{'Result': 'Commit successfully.'}

##save_config()
No input  

Return a dictionary:
Save successfully:{"Result": "Save successfully."}  
If "save" is None:{"Error": "You don't need to save."}  
If you have save before:{"Error": "You have saved!"}  
If you still not commit:{"Error": "You need to commit first!"}  

You can use this method to save your configuration.

	>>> vyos1.save_config()
	{'Result': 'Save successfully.'}

##exit_config(force=False)
Parameter "force":  
True or False.The default value is False,if you don't want to save your configuration you should use "force=True" as input.

Return a dictionary:  
Exit successfully:{"Result": "Exit configure mode successfully."}  

If you do not commit and save,please read the 6th explanation to get more infomation.

##lo(data)
Parameter "data":a dictionary  
Example:{'config':'1.1.1.1/32'}  

Return a dictionary:  
Configure successfully:{"Result": "Modify successfully."}  

You can use this method to create a new VyOS loopback address for interface "lo".We usually use this new address as router id.

##delete_route(data)
Parameter "data":a dictionary  
Example:{'config':'all'}

The value of "config" just "rip","static","ospf" and "all".Please remember "all" will delete all configuration in the section "protocols" in VyOS's configuration file.The others will delete the corresponding part of configuration in "protocols" section.

Return a dictionary:  
Delete successfully:{"Result": "Delete successfully."}  
Invalid value:{"Error": "Nonsupport protocols type."}  

You can use this method delete router configuration but please be careful.

##static_route(data)
Parameter "data":a dictionary  
Example:{'config':{'target':'10.20.10.0/24','next-hop':'10.20.10.1','distance':'1'},}  

This method equal to "set protocols static route next-hop distance".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"}

You can use this method configure a static router.

##rip_route(data)
Parameter "data":a dictionary  
Example:{'config':'192.168.10.0/24',}  

This method equal to "set protocols rip network" and "set protocols rip redistribute connected".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"}  

You can use this method configure a RIP router and execute routing redistribution.

##ospf_area(data)
Parameter "data":a dictionary  
Example:{'config'：{'area':'0','network':'192.168.10.0/24'},}  

This method equal to "set protocols ospf area network".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"}  

You can use this method configure OSPF areas.

##router_id(data)
Parameter "data":a dictionary  
Example:{'config':{'id':'1.1.1.1'},}  

This method equal to "set protocols ospf parameters router-id".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"}

You can use this method configure router id.

##ospf_redistribute(data)
Parameter "data":a dictionary  
Example: {'config':{'type':'2'},}  

This method equal to "set protocols ospf redistribute connected metric-type" and "set protocols ospf redistribute connected route-map CONNECT".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"}  

You can use this method execute routing redistribution.

##ospf_adjacency()
No input

This method equal to "set protocols ospf log-adjacency-changes".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"}

##ospf\_default\_route(data)
Parameter "data":a dictionary  
Example:{'config':{'metric':'10','metric-type':'2'},}  

This method equal to "set protocols ospf default-information originate always","set protocols ospf default-information originate metric" and "set protocols ospf default-information originate metric-type".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"}  

You can use this method configure default route.

##ospf\_route\_map(data)
Parameter "data":a dictionary  
Example:{'config':{'rule':'10','interface':'lo'},}  

This method equal to "set policy route-map CONNECT rule action permit" and "set policy route-map CONNECT rule match interface".

Return a dictionary:  
Configure successfully:{"Result": "Configured successfully"} 

You can use this method configure route-map.

==================================================================================

# VyRoute
一个用于VyOS路由服务设置的库

作者：Hochikong  
联系我：michellehzg@gmail.com（较少用） or 1097225749@qq.com

这是一个用于设置VyOS路由功能的Python库，目前仅仅提供了静态路由，RIP和OSPF的功能，以后有需要会增加BGP的部分，如果你有兴趣，可以试着clone一份增加你想要的功能，比如BGP和网络接口设置。

在后面我还会继续开发实现VyOS的防火墙、VPN配置的库。

##备注
已经打包好的egg文件在：[https://github.com/Hochikong/vyroute/tree/master/dist](https://github.com/Hochikong/vyroute/tree/master/dist)  

可以下载并用easy_install安装egg包

下面我会给出这个库的使用说明和注意事项：

本库依赖于Exscript库，可以在github上找到

本库基于MIT协议开源

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







   


