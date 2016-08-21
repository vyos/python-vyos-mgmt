#VyMGMT
A python library for VyOS configurations

This python library is used for VyOS configurations.Use this library to send the configuration to VyOS. 

##Note
###Version:0.1 
 
###Author:Hochikong  
 
###Contact me:hochikong@foxmail.com(usually use) or michellehzg@gmail.com(Inconvenient in Mainland China)  

###License:MIT   
  
###Requirement:pexpect(pxssh)  

##Basic example
Set a description for eth0:   

    >>> from vymgmt.Router import Router
    >>> vyos = Router('192.168.225.2','vyos:vyos')
    >>> vyos.login()
    'Result : Login successfully.'
    >>> vyos.configure()
    'Result : Active configure mode successfully.'
    >>> vyos.set("interfaces ethernet eth0 description 'eth0'")
    'Result : Configured successfully'
    >>> vyos.commit()
    'Result : Commit successfully.'
    >>> vyos.status()
    {'status': 'login', 'commit': 'Yes', 'save': 'No', 'configure': 'Yes'}
    >>> vyos.exit()
    'Error : You should save first.'
    >>> vyos.save()
    'Result : Save successfully.'
    >>> vyos.exit()
    'Result : Exit configure mode successfully.'
    >>> vyos.logout()
    'Result : Logout successfully.'

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

##set(config)
Basic 'set' method,execute the set command in VyOS.

Example:  
config: "interfaces ethernet eth0 description 'eth0'"

The minimal c method.

##delete(config)
Basic 'delete' method,execute the delete command in VyOS.

Example:  
config: "interfaces ethernet eth0 description 'eth0'"

The minimal configuration method.




