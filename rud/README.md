# CRUD y arquitectura modular

Este proyecto proporciona un script en Rust para crear y gestionar estructuras de API REST automáticamente, con soporte para cambiar extensiones de archivos de manera recursiva.

## Instalación

Para instalar el script, sigue estos pasos:

1. Clona el repositorio y entra al directorio:
   ```bash
   git clone https://github.com/GendryC/scripts.git   
   cd scripts/rud
   ```  
   
2. Ejecuta el script como sudo  
	```bash
	./install.sh  
	```  
3. Copia  
	```bash  
	git clone https://github.com/GendryC/scripts.git && cd scripts/rud && sudo ./install.sh
	```
---
## Uso

Para crear la estructura base de un nuevo módulo:
```bash
rud -n <nombre-del-modulo>
```
	
Para crear un nuevo servicio dentro de un módulo:
```bash  
rud -s <nombre-del-modulo> <nombre-del-servicio>
```  

Para crear un nuevo modelo y DTO dentro de un módulo:
```bash  
rud -m <nombre-del-modulo> <nombre-del-modelo>  
```
Para crear un nuevo controlador dentro de un módulo:  
```bash
rud -c <nombre-del-modulo> <nombre-del-controlador>  
```
Para cambiar las extensiones de los archivos dentro de un módulo:  
```bash
rud -e <lenguaje> <nombre-del-modulo>  
```
