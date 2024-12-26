#!/bin/bash

echo "Compilando el archivo rud.rs..."
rustc rud.rs -o rud

if [ $? -ne 0 ]; then
    echo "Error en la compilación. Por favor, revisa el código y vuelve a intentarlo."
    exit 1
fi

echo "Moviendo el binario a /usr/local/bin..."
sudo mv rud /usr/local/bin

echo "Dando permisos de ejecución al binario..."
sudo chmod +x /usr/local/bin/rud

echo "Instalación completada. Ahora puedes ejecutar el comando 'rud' desde cualquier lugar."
