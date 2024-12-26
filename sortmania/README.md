# Proyecto de Clasificación de Archivos

Este proyecto utiliza la API de x.AI para clasificar y mover archivos desde un directorio de origen a un directorio de destino basado en instrucciones específicas.

## Requisitos

- Python 3.x
- Módulos: `os`, `shutil`, `json`, `openai`, `time`

## Configuración

1. Instala las dependencias necesarias:

    ```bash
    pip install openai
    ```

2. Configura tu clave API de x.AI en el script:

    ```python
    XAI_API_KEY = "tu-clave-api-aqui"
    ```

3. Installación

    ```bash
    git clone https://github.com/GendryC/scripts.git && cd scripts/sortmania && sudo ./install.sh
    ```

## Uso

1. Ejecuta el script:

    ```bash
    sortmania
    ```

2. Introduce las rutas de los directorios de origen y destino cuando se te solicite.

3. Introduce cualquier instrucción adicional para la clasificación de archivos.

## Ejemplo de `file_instructions.json`

El archivo `file_instructions.json` debe contener las instrucciones de clasificación en formato JSON. Aquí tienes un ejemplo:

```json
{
    "txt": "text_files",
    "jpg": "images",
    "png": "images",
    "peliculas": "agrupar por genero"
}
