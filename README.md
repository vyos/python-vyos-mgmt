#VyMGMT
A python library for VyOS configurations

This python library is used for VyOS configurations.  

Use this library to send the configuration commands to VyOS. 

##Note
###Version:0.1 
 
###Author:Hochikong  
 
###Contact me:hochikong@foxmail.com(usually use) or michellehzg@gmail.com(Inconvenient in Mainland China)  

###License:MIT   
  
###Requirement:pexpect(pxssh)  

##Basic Example
Set a description for eth0:   

    >>> from vymgmt.router import Router
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

##Something you should know
1.Only admin level user can use this library to login and execute all configuration methods.  

2.When you initialize the Router class,the second parameters is 'username:password'.  

3.set() and delete() method is the core function of this library,you can just use a same configuration command on VyOS to set or delete a specify configuration.But you should take a look at the Basic Example and All Methods sections.  
 
#All Methods
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

#Exceptions
##vymgmt.base\_exceptions.exceptions\_for\_commit.CommitFailed()

This exception class is for commit() failures due to some mistakes in your configurations.  

When this exception raise,the error message from VyOS will displayed.

##vymgmt.base\_exceptions.exceptions\_for\_commit.CommitConflict()

This exception class is for commit() failures due to the commit conflicts when more than one users committing their configurations at the same time.

When this exception raise,the error message from VyOS will displayed.
 
##vymgmt.base\_exceptions.exceptions\_for\_set\_and\_delete.ConfigPathError()

This exception class is for set() and delete() failures due to configuration path error.  

What is configuration path error?

This configuration is correct:

	vyos.set("protocols rip network xxx")

This is wrong:

	vyos.delete("ethernet interface eth1 address")

The wrong one will raise this exception and display the error message:

	Configuration path: [ethernet] is not valid
  	Delete failed

When this exception raise,the error message from VyOS will displayed.

##vymgmt.base\_exceptions.exceptions\_for\_set\_and\_delete.ConfigValueError()

This exception class is for set() and delete() failures due to value error.  

This exception will raise when your configuration has wrong value,such as:

	vyos.set("interfaces ethernet eth1 address '192.168.225.2")   #No netmask

When this exception raise,the error message from VyOS will displayed.

##vymgmt.base_exceptions.CommonError()

This exception class is for all failures which do not covered by exceptions above.

When this exception raise,the error message from VyOS will displayed. 





