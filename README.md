#VyRoute
A python library for VyOS routing service setting

This python library is used for VyOS routing service configuration,now it provide Static, RIP, OSPF and simple BGP configuration functions to users.

##Note
###Version:0.1 
 
###Author:Hochikong  
 
###Contact me:hochikong@foxmail.com(usually use) or michellehzg@gmail.com(Inconvenient in Mainland China)  

###License:MIT   
  
###Requirement:pexpect(pxssh)  

##Overview
Now,SDN is a technologies trend.Like Openflow and switch controller,they provide us with centralized control and programmable features.But adminstrators of VyOS still need to login the system and 
configure services manually.I need a tool which can configure router service remotely and user can write a program to control the system like SDN controller.So I decide to write this library.Up to now,it just provide static, RIP, OSPF and BGP router configuration function.

There are two classes in library:Router and BasicRouter.Router is a parent class,BasicRouter inherit parent class.When we use this library,we should use VyOS's address and user information to initialize a BasicRouter,then we can use member methods to control the system.
Just like administrators configure services,in this lib you also need to enter configure mode,execute configuration,commit it and save it.

BasicRouter has a member variable(python dictionary) "status",it store a router substance's status.

	self.__status = {"status": None, "commit": None, "save": None, "configure": None}

When it finish initialization,all values in "status" are None.When a 
user login the substance,the value of "status" in self.__status will change to "login".When the user execute configure(),he will enter configure mode and value of "configure" will change to "Yes",during configure mode,all configuration method will change the value of "commit" and "save" to "no",when user finish a operation but not commit,the following method will not change the value of "commit" and "save".  

When the user want to exit configure mode,only he have commit and save the configuration can he exit configure mode,the value of "commit" and "save" must change to "Yes".If he don't want to save the configuration,he should use exit_config(force=True) to exit.If the user execute logout(),"status" will change to "logout" and the others will change to None.  

When you use this library,the methods you can only use in configure mode will return a message or an exception.Exceptions usually cause by the environment,maybe.If your parameters is correct,it will return a string message:

	"Result : Configured successfully"

If there are any mistakes in the parameters,the method will return a string error message which return by VyOS system.

	>>> vyos.lo('1.1.1.1')
	'set interfaces loopback lo address 1.1.1.1\r\n\x1b[?1h\x1b=\r\x1b[m\r\n  "1.1.1.1" is not a valid value of type "ipv4net or ipv6net"\x1b[m\r\n  Value validation failed\x1b[m\r\n  Set failed\x1b[m\r\n\x1b[m\r\n\r\x1b[K\x1b[?1l\x1b>'	

This kind of error message,high-level application should use print to feedback to user. 

	>>> print(vyos.lo('1.1.1.1'))
	set interfaces loopback lo address 1.1.1.1

	  "1.1.1.1" is not a valid value of type "ipv4net or ipv6net"
	  Value validation failed
	  Set failed

IMPORTANT:Some method will execute more than one command at once.If there are any mistake in your input,those methods will return a 
dictionary includes all error messages cause by your invalid input. High-level application should print every error message in 
the dictionary.

##Basic example
I will show you how to configure a simple static router:  

Topo:  
test1---VyOS1———VyOS2---test2   

At first,test1 cannot ping test2:

	root@test1:~# ping 192.168.157.8
	PING 192.168.157.8 (192.168.157.8) 56(84) bytes of data.
	^C
	--- 192.168.157.8 ping statistics ---
	3 packets transmitted, 0 received, 100% packet loss, time 2016ms

test2 also cannot ping test1:

	root@test3:~# ping 192.168.225.3
	PING 192.168.225.3 (192.168.225.3) 56(84) bytes of data.
	From 192.168.157.7 icmp_seq=1 Destination Net Unreachable
	From 192.168.157.7 icmp_seq=2 Destination Net Unreachable
	c^C
	--- 192.168.225.3 ping statistics ---
	6 packets transmitted, 0 received, +2 errors, 100% packet loss, time 5023ms
 
So,let's use vyroute to set up a static router between test1 and test2:

Router1:

	>>> from vyroute.Router import BasicRouter
	>>> vyos = BasicRouter('192.168.225.2','vyos:vyos')
	>>> vyos.login()
	'Result : Login successfully.'
	>>> vyos.configure()
	'Result : Active configure mode successfully.'
	>>> vyos.static_route('192.168.225.0/24','192.168.225.2','1')
	'Result : Configured successfully'
	>>> vyos.static_route('192.168.157.0/24','192.168.10.6','1')
	'Result : Configured successfully'
	>>> vyos.commit()
	'Result : Commit successfully.'
	>>> vyos.save()
	'Result : Save successfully.'
	>>> vyos.exit()
	'Result : Exit configure mode successfully.'
	>>> vyos.logout()
	'Result : Logout successfully.'

Router2:

	>>> vyos1 = BasicRouter('192.168.10.6','vyos:vyos')
	>>> vyos1.login()
	'Result : Login successfully.'
	>>> vyos1.configure()
	'Result : Active configure mode successfully.'
	>>> vyos1.static_route('192.168.225.0/24','192.168.10.5','1')
	'Result : Configured successfully'
	>>> vyos1.static_route('192.168.157.0/24','192.168.157.7','1')
	'Result : Configured successfully'
	>>> vyos1.exit()
	'Error : You should commit first.'
	>>> vyos1.status()
	{'status': 'login', 'commit': 'No', 'save': 'No', 'configure': 'Yes'}
	>>> vyos1.commit()
	'Result : Commit successfully.'
	>>> vyos1.save()
	'Result : Save successfully.'
	>>> vyos1.status()
	{'status': 'login', 'commit': 'Yes', 'save': 'Yes', 'configure': 'Yes'}
	>>> vyos1.exit()
	'Result : Exit configure mode successfully.'
	>>> vyos1.status()
	{'status': 'login', 'commit': None, 'save': None, 'configure': 'No'}
	>>> vyos1.logout()
	'Result : Logout successfully.'

Check the network:
	
	root@test1:~# ping 192.168.157.8 -c 5
	PING 192.168.157.8 (192.168.157.8) 56(84) bytes of data.
	64 bytes from 192.168.157.8: icmp_seq=1 ttl=62 time=0.663 ms
	64 bytes from 192.168.157.8: icmp_seq=2 ttl=62 time=0.998 ms
	64 bytes from 192.168.157.8: icmp_seq=3 ttl=62 time=0.919 ms
	64 bytes from 192.168.157.8: icmp_seq=4 ttl=62 time=0.629 ms
	64 bytes from 192.168.157.8: icmp_seq=5 ttl=62 time=0.671 ms
	
	--- 192.168.157.8 ping statistics ---
	5 packets transmitted, 5 received, 0% packet loss, time 4002ms
	rtt min/avg/max/mdev = 0.629/0.776/0.998/0.151 ms

By ping we can know:test1 can ping test2 and test2 can ping test1,then we can check the VyOS:

	protocols {
    	static {
	        route 192.168.157.0/24 {
	            next-hop 192.168.10.6 {
	                distance 1
	            }
	        }
	        route 192.168.225.0/24 {
	            next-hop 192.168.225.2 {
	                distance 1
	            }
	        }
	    }
	}

Because we have save the configuration,so if you reboot the VyOS system but the static router still works.

If you change the configuration,you must commit and save it then you can exit configure mode.But you can use vyos.exit(force=Ture) to execute "exit discard" command. 

#All methods
##status():
Check the router object inner status.  

Return a dictionary include the status of BasicRouter instance.  

##login():
Login the VyOS system when you have create a new BasicRouter instance.  

##logout()
Logout the VyOS system.  

This method execute a close() on a connection.  

You can use this method logout a router substance.After logout,you can use the same instance to login again.  

##configure()
Enter the VyOS configure mode  

You must login the VyOS system before use this method.  

##commit()
Commit the configuration changes.  

You can use this method to commit your configuration.  

Due to configuration methods will change the value of the keys in self.__status.You should commit the configurations then can you save or exit.  

##save()
Save the configuration after commit.  

You can use this method to save your configuration.  

##exit(force=False)
Exit VyOS configure mode.  

Example:  
force: True or False  

If force=True,this method will execute "exit discard" command and all your changes will lost.  

##lo(lo_addres)
Add a router loopback address.  

Example:  
lo_addres: '1.1.1.1/32'(all parameters are string)  

You can use this method to add a new VyOS loopback address for interface "lo".We usually use this new address as router id.  

##delete_route(route_type)
Delete router configurations.  

Example:  
route_type: 'rip'/'static'/'ospf'/'bgp'/'all'  

The value of "config" just "rip","static","ospf","bgp" and "all".Please remember "all" will delete all configuration in the section "protocols" in VyOS's configuration file.The others will delete the corresponding part of configuration in "protocols" section.  

You can use this method to delete router configuration but be careful.  

##static_route(network_range, next_hop, distance)
This method provide a basic static router configuration function,
and his method equal to "set protocols static route next-hop distance".  

Example:  
network_range: '10.20.10.0/24'  
next-hop: '10.20.10.1'  
distance: '1'  

You can use this method to configure a static router.  
##rip_route(network_range)
RIP router network setting,and this method equal to "set protocols rip network".  

Example:  
network_range: '10.20.10.0/24'  

You can use this method to add a network.

##rip_redistribute()
Execute "set protocols rip redistribute connected" command.  

You can use this method to execute routing redistribution.  

##ospf_area(area, network_range)
This method provide a OSPF area configuration function and this method equal to "set protocols ospf area network".  

Example:  
area: '0'  
network_range: '192.168.10.0/24'  

You can use this method to configure OSPF areas.  

##ospf_router_id(router_id)
This method provide a router id configuration function and this method equal to "set protocols ospf parameters router-id".  

Example:  
router_id: '1.1.1.1'  

You can use this method to configure router id.  

##ospf_redistribute(metric_type)
OSPF redistribute setting and this method equal to "set protocols ospf redistribute connected metric-type" and "set protocols ospf redistribute connected route-map CONNECT".  

Example:  
metric_type: '2'  

You can use this method to execute routing redistribution.  

##ospf_adjacency()
This method equal to "set protocols ospf log-adjacency-changes".  

##ospf\_default\_route(metric, metric_type)
This method execute the commands to configure default route and this method equal to "set protocols ospf default-information originate always","set protocols ospf default-information originate metric" and "set protocols ospf default-information originate metric-type".  

Example:  
metric: '10'  
metric-type: '2'  

You can use this method to configure default route.  

##ospf\_route\_map(data)
VyOS route-map setting when you configure a OSPF router and this method equal to "set policy route-map CONNECT rule action permit" and "set policy route-map CONNECT rule match interface".  

Example:  
rule: '10'  
interface: 'lo'  

You can use this method to configure route-map.  

##bgp_route(self_as, neighbor, multihop, remote_as, update_source)
VyOS BGP router basic setting and this method equal to "set protocols bgp neighbor ebgp-multihop","set protocols bgp neighbor remote-as" and "set protocols bgp neighbor update-source".  

Example:  
self_as: '65538'  
neighbor': '192.168.10.5'  
multihop': '2'  
remote_as': '65537'  
update_source': '192.168.10.6'  

You can use this method to configure neighbor,AS,remote-as and update-source and ebgp-multihop when you configure a BGP router.  

##bgp_network(self_as, network_range)
Add a network to BGP router and this method equals to "set protocols bgp network".  

Example:   
self_as: '65538'  
router_id: '10.20.10.0'  

This method is similar to rip_route.  

##bgp\_router\_id(self_as, router_id)
Set a router id for the router you login and this method equals to set protocols bgp parameters router-id".  

Example:  
self_as: '65538'  
router_id: '10.20.10.0'  

This method is similar to ospf\_router\_id.  

##bgp\_blackhole\_route(network_range)
Set a blackhole route and this method equals to "set protocols static route blackhole distance 254".  

Example:  
network_range: '10.20.10.0/24'  

You can use this method to configure blackhole route when you configure a BGP router.  


