# nPy
#### Instrucciones para sistemas Windows
nPy es una interfaz configurable capaz de lanzar cualquier aplicación gráfica o de consola, y que ofrece una forma amigable para ingresar parámetros y definir secuencias.

## Iniciar nPy
Para iniciar nPy, hacé doble click en el ícono del escritorio, o buscá nPy.exe en el directorio nPy en el disco local de tu PC: C:\nPy\, D:\nPy\, etc.

## Pantalla principal
![main](https://user-images.githubusercontent.com/4999277/58023510-53e39000-7ae6-11e9-85ba-ca8a580b49aa.png)

En la pantalla principal se puede ver:
 - Un menú superior desde donde se lanzan las aplicaciones configuradas (En la imagen de ejemplo dice "Ejemplos, Neutrónica").
 - A la izquierda, un panel lateral para explorar directorios, que permite ser ocultado.
 - Una serie de pestañas (Process, Text Editor, Application) y estamos en la primera.
 - Un campo "Current process" que muestra el programa que está actualmente en ejecución.
 - Un campo "Standard output" que muestra las salidas que devuelven los programas al ejecutarse.

Los botones en el sector inferior permiten:
 - Kill process: finaliza el proceso que corra actualmente.
 - Copy to editor: copia el contenido de la salida standard al editor de texto incorporado.
 - Clean terminal: vacía el contenido de los campos Current process y Standard output.

## Lanzar una aplicación
![parametro string](https://user-images.githubusercontent.com/4999277/58023504-534af980-7ae6-11e9-8a57-c79dc2457b28.png)

Para lanzar una aplicación previamente configurada, basta con elegir una opción del menú superior y luego seleccionar la aplicación deseada. Si la aplicación a lanzar no requiere parámetros, ésta se lanza inmediatamente. Si por el contrario hacen falta parámetros y éstos están debidamente configurados, aparecerá en pantalla un pequeño diálogo como el de la imagen solicitando los parámetros antes de lanzar. En la imagen del ejemplo, lanzamos el comando **ping**, previamente configurado, y nos solicita una dirección IP.

#### Archivos y directorios como parámetros

![parametro file y dir](https://user-images.githubusercontent.com/4999277/58023503-534af980-7ae6-11e9-8628-7c36b1ddec8c.png)

Muchos programas requieren la ruta de un archivo o directorio como parámetro. nPy admite una configuración especial de parámetros con este fin. Al lanzar una aplicación que requiera archivos o directorios como parámetros, veremos una pantalla como la de la imagen, que nos permitirá seleccionar un archivo o directorio explorando el sistema de archivos del sistema.

#### Máscara para extensiones de archivo

Cuando el parámetro a indicar sea un archivo, es posible configurar a nPy para que sólo liste los archivos de la extensión indicada para facilitar la búsqueda.

#### Luego de lanzar

![salida](https://user-images.githubusercontent.com/4999277/58023505-534af980-7ae6-11e9-8dad-f44e25af20e2.png)

Si el programa generó una salida, ésta se mostrará en el campo Standar output, tal como se muestra en la imagen. En este ejemplo lanzamos **ping 192.168.2.78** y la salida del comando se ve en la parte inferior con fondo gris.

## Editor de texto

![text_editor](https://user-images.githubusercontent.com/4999277/58023509-53e39000-7ae6-11e9-9ba7-297360d4a96f.png)

En la segunda pestaña de nPy, se puede encontrar un editor de texto simple incorporado. El editor cuenta con las opciones básicas de un editor de texto:
 - Nuevo, Abrir, Guardar, Guardar como, imprimir.
 - Copiar, cortar, pegar, deshacer y rehacer.
 - Permite buscar un texto en todo el archivo así como reemplazar todas las apariciones de un texto en el archivo.
 - permite abrir varios archivos simultáneamente en diferentes pestañas.
 - Permite cambiar el tamaño de la letra
 - Permite optar por cortar la línea al llegar al final de la hoja y seguir abajo (Wrap lines) o bien coloca una barra de desplazamiento lateral cuando el texto se exceda del tamaño del editor.

## Configuraciones

### Seleccionar directorio de trabajo

![environment](https://user-images.githubusercontent.com/4999277/58023507-53e39000-7ae6-11e9-8255-9f181a3b7780.png)

Cuando nPy lanze un programa cuyos parámetros necesitan archivos, éste los buscará por defecto en el directorio de trabajo actual. Es posible cambiar el directorio de trabajo desde la solapa Application -> Environment. Para cambiarla se debe clickear en Update (a la derecha) y seleccionar el directorio desde el sistema de archivos local.

La opción "Treeview path" indica el directorio raíz (nivel más alto) del árbol de directorios del panel lateral. El "working directory" debe estar contenido dentro del "Treeview path"

### Agregar, quitar o modificar programas al menú

![tabla](https://user-images.githubusercontent.com/4999277/58023506-534af980-7ae6-11e9-8e9b-95cf9048b957.png)

Modificar los programas que aparecen listados en el menú, se hace de manera simple desde la solapa la solapa Application -> Sequence Table. Más instrucciones al respecto serán provistas en el manual para el administrador.


## Instalación de nPy
Para instalar nPy en un nuevo sistema, basta con copiar el directorio de nPy que contiene nPy.exe, la tabla de secuencias y eventualmente otros programas anexos para ejecutar dentro de nPy.

Consejo: Al copiar una tabla de secuencias de una computadora hacia otra, revisá que las direcciones absolutas que figuren allí sean válidas en el nuevo sistema. 