# Phoenix
Linux Post Enumeration Framework

```
@@@@@@@   @@@  @@@   @@@@@@   @@@@@@@@  @@@  @@@  @@@  @@@  @@@
@@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@ @@@  @@@  @@@  @@@
@@!  @@@  @@!  @@@  @@!  @@@  @@!       @@!@!@@@  @@!  @@!  !@@
!@!  @!@  !@!  @!@  !@!  @!@  !@!       !@!!@!@!  !@!  !@!  @!!
@!@@!@!   @!@!@!@!  @!@  !@!  @!!!:!    @!@ !!@!  !!@   !@@!@! 
!!@!!!    !!!@!!!!  !@!  !!!  !!!!!:    !@!  !!!  !!!    @!!!  
!!:       !!:  !!!  !!:  !!!  !!:       !!:  !!!  !!:   !: :!! 
:!:       :!:  !:!  :!:  !:!  :!:       :!:  !:!  :!:  :!:  !:!
::        ::   :::  ::::: ::  :: ::::   ::    ::   ::  ::   ::: 
:         :    : :   : :  :   : :: ::   ::     :    :  :     ::
```
------
## Phoenix Help

The available commands in the Framework yet.

```
Phoenix > help

Command                 Description
----------------------  -------------------------------------------------
help                    Show this menu
list [type]             List all available [modules, listeners, sessions]
use [name/number]       Use a selected module
info [module]           Shows info for a specified module
interact [name/number]  Interact with active session
search [term]           Search in the modules
exit                    Exit from the application
```

**Listing Modules**

```
Phoenix > list modules

  #  Name                   Type    Command       Description
---  ---------------------  ------  ------------  ----------------------
  0  native/tcp_listener    Native  tcp_listener  Tcp Listener
  1  AAA                    Native  almafa        Teszt ModuleAA
  2  native/post/querysuid  Native  querysuid     Query SUID executables
  3  native/tcp_connect     Native  tcp_connect   Tcp Connector
```

**Using Modules**

```
Phoenix > list modules

  #  Name                   Type    Command       Description
---  ---------------------  ------  ------------  ----------------------
  0  native/tcp_listener    Native  tcp_listener  Tcp Listener
  1  AAA                    Native  almafa        Teszt ModuleAA
  2  native/post/querysuid  Native  querysuid     Query SUID executables
  3  native/tcp_connect     Native  tcp_connect   Tcp Connector

Phoenix > use 0
Phoenix(native/tcp_listener)> options

Name    Value    Required    Description
------  -------  ----------  ---------------------
LHOST   0.0.0.0  True        The host to listen on
LPORT   9001     True        The port to listen on

Phoenix(native/tcp_listener)> set lport 9002
[+] LPORT ==> 9002
Phoenix(native/tcp_listener)> options

Name    Value    Required    Description
------  -------  ----------  ---------------------
LHOST   0.0.0.0  True        The host to listen on
LPORT   9002     True        The port to listen on

Phoenix(native/tcp_listener)> 

```

**Running the module**

```
Phoenix(native/tcp_listener)> run
[+] Listening on 0.0.0.0:9002
[+] Client Connected with address 127.0.0.1 ==> 4KYMOZKU
Phoenix(native/tcp_listener)> bg
Phoenix > list sessions

  #  Name      Remote Address    Client Type    Platform    Hostname    Username
---  --------  ----------------  -------------  ----------  ----------  ----------
  0  4KYMOZKU  127.0.0.1:55792   Native         Linux       kali        isap

Phoenix > interact 0
Session(4KYMOZKU) > 
```
