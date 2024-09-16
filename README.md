# aIO-adapter
Monolithic repository for the development of the aIO adapter PCB implemented at the ICRR.  
The structure is the following:      
```
/aIO-adapter
  /packages
    /stable
      /src
    /app2
      /src
    /app3
      /src
    /app4
      /src
  /scripts
  /config
  /docs

```
The `packages` folder contains the `stable` version of the firmware and all other experimental versions (`app1`, `app2`, etc.).  
Common scripts or tools shared among various versions can be placed in the `scripts` folder. 
Configuration files can be placed in the `config` folder.  
All the documentation abou the elements and the development of the PCB can be placed in the `docs` folder.

