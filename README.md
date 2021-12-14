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
