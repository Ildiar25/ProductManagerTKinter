
# Gestor de Productos

---

---

En este ejercicio guiado vamos a crear una *aplicación de escritorio*
y la conectaremos a una **base de datos** para almacenar, editar y
eliminar elementos mediante consultas *SQL*.

El objetivo de este ejercicio es observar el manejo de ventanas en la *aplicación* y
el uso de **Python** utilizando la librería **Tkinter** y **SQLite3**.

Una vez abierta dicha ***aplicación***, el usuario deberá encontrar una 
*interfaz visual* que le permita realizar las siguientes acciones.

---

### ///// Contenido Obligatorio /////
- **Crear:** Añadir un nuevo producto a la base de datos
- **Modificar:** Cambiar los datos almacenados en dicho producto
- **Eliminar:** Quitar el producto de la base de datos


### ///// Contenido Optativo /////
- **Más Widgets:** Añadir cualquier widget más que no sea *label*, *button*, 
*entry* o *treeview*
- **Mejorar:** Se da la opción de poder mejorar la interfaz visual
- **Categorizar:** Se puede añadir un campo para incluir una categoría
- **Cantidad**: Añadir un campo que controle el *stock* en almacén
- **Implementar SQLAlchemy**: Implementar SQLAlchemy sobre SQL para poder cambiar 
base de datos sin necesidad de tocar código

---

**NOTA:** *Todo el trabajo en código se ha realizado en inglés para poner en práctica el
desarrollo en dicho idioma.*

---

<p style="text-align:center"> * * * * * * </p>


## Estructura del proyecto
¿Qué estructura deberá tener esta aplicación?
En esta ocasión

- `assets/... :` Las imágenes usadas en nuestra aplicación.
  - `assets/new-product-icon.ico:` Icono de ventana temporal.
  - `assets/product-manager-icon.ico:` Icono de la aplicación.
  - `assets/images/... :` Imágenes utilizadas en este documento.
- `database/products.db:` Almacena la base de datos donde se sincronizan los productos.
- `.gitignore:` Archivos ignorados en el control de versiones. 
- `app.py:` Inicia la aplicación.
- `models.py:` Almacena las clases necesarias de dicho proyecto, en este caso la clase `MainWindow`.
- `README.md:` Este documento.
- `requirements.txt:` Registro de versiones del stack technológico necesario para usar el programa.

---
***Estructura del directorio principal:***

![Espacio de trabajo completo](/assets/images/tree-structure.png "Directorio Principal")

---

<p style="text-align:center"> * * * * * * </p>

## Principales Casos de Uso

- **Añadir producto:**

Esta característica se encargará de pedir al usuario que ingrese unos 
**valores obligatorios**. Cuando el usuario pulse el botón ***'guardar'***,
la función llamada 'add_product()' se encargará de añadir dicho producto
mediante una consulta ***SQL***.

---

***Añadir producto 'Lenovo':***

![Creación de un nuevo producto 'lenovo'](/assets/images/add-example.png "Añadir producto")
> El usuario inserta los datos a guardar y selecciona su categoría.

***Comprobación en Base de Datos:***

![Comprobar si 'Lenovo' se encuentra en la base de datos](/assets/images/update-example-02.png "Revisión en base de datos")
> Aparece dicho producto en la base de datos ya almacenado.

***Actualiza productos en la aplicación:***

![Actualiza la visual de la base de datos](/assets/images/update-example-01.png "Actualización entorno visual")
> Aparece dicho producto en la base de datos ya almacenado.

---

- **Eliminar producto:**

Esta característica permite al usuario elegir un producto de la tabla mostrada.
Una vez elegido, si pulsa el botón inferior donde se lee **BORRAR**, la información
de dicho producto se enviará a la función 'del_product()' para que pueda procesarse
una consulta **SQL** de eliminación. Después se actualizará la visual de la base de
datos en la interfaz del usuario.

---

***Seleccionar 'Impresora Prusa' de la tabla:***

![Seleccionar 'Impresora Prusa' de la tabla](/assets/images/del-example-01.png "Seleccionar producto")
> Como se puede observar, se selecciona toda la fila.

***Eliminación del producto:***

![Comprobar si 'Impresora Prusa' se ha eliminado](/assets/images/del-example-02.png "Actualización entorno visual")
> La tabla de productos mostrada se actualiza y el producto ya no se encuentra.

***Comprobación en base de datos:***

![Comprobar la eliminación en la base de datos](/assets/images/del-example-03.png "Información de la base de datos")
> Se puede observar que el producto ha sido eliminado correctamente.

---

- **Modificar producto:**

Para su modificación, el usuario deberá seleccionar un producto de la tabla mostrada.
Una vez seleccionado, pulsará el botón **MODIFICAR** que realizará la siguiente acción:
> - Creará una nueva ventana.
> - Proporcionará los datos actuales de dicho producto y unos campos a rellenar por el usuario
> - Realizar un control de flujo para saber si el usuario a introducido dichos valores
una vez pulse el botón **ACTUALIZAR**.
> - Enviará los valores antiguos y los nuevos mediante una consulta **SQL** a ña base de datos
> - Guardará los cambios
> - Cerrará automáticamente la ventana.

---

***Modificar producto 'Lenovo':***

![Muestra todos los productos](/assets/images/new-window-example-01.png "Producto seleccionado")
> Seleccionamos el producto a modificar y le damos al botón.

***Se abre la nueva ventana:***

![Nueva ventana de modificación](/assets/images/new-window-example-02.png "Ventana edición")
> Como se puede observar, se abre una nueva ventana con campos a rellenar.

***Actualiza la vista general:***

![Actualización visual](/assets/images/new-window-example-03.png "Gestor de productos")
> Como se puede observar, al editar un producto podemos ver que sus datos han sido actualizados.

***Comprobación en Base de Datos:***

![Comprobar los datos del producto 'Lenovo'](/assets/images/new-window-example-04.png "Revisión en base de datos")
> El producto se ha actualizado con éxito.

---

- **Categorizar:**

Para categorizar una producto, tan solo habrá que desplegar el menú en la creación 
de uno nuevo.

---

- **Ordenar por categoría:**

Este caso de uso hará que cada _'heading'_ de la tabla pueda ordenar los productos
en orden ascendente o descendente según su característica.
Por tanto, al pulsar sobre **nombre**, obtendremos los productos ordenados.
La misma acción podrá encontrarse en **precio**, **categoría** y **stock**

---

***Orden según 'stock' de forma descendente:***

![Ejemplo orden descentende](/assets/images/order-example-01.png "Orden descendente")
> Se ven los productos ordenados de forma descendente según su cantidad en stock.

***Orden según 'precio' de forma ascendente:***

![Ejemplo orden ascendente](/assets/images/order-example-02.png "Orden ascendente")
> Se ven los productos ordenados de forma ascendente según su precio.

---

<p style="text-align:center"> * * * * * * </p>

## Guía de Instalación

Antes de realizar el testeo de la aplicación, se deberá tener en cuenta los siguientes
requisitos. Para ello se muestran a continuación todas las librerías utilizadas
y el lenguaje principal de programación.

---

### Stack Tecnológico Principal

- **Python:** Como lenguaje de programación principal
- **TKinter:** Como framework para escritorio
- **SQLite:** Como lenguaje de la base de datos

### Stack Tecnológico Secundario

- **Pycharm:** Como IDE de programación
- **Virtualenvi**: Como entorno virtual

### Preparación del entorno

1. Asegúrate de tener instalado ***Python*** en tu equipo. Puedes descargarlo
desde [aquí](https://www.python.org/downloads/).
2. Copia o descarga el repositorio del proyecto.
3. Ve al directorio principal del proyecto y crea un nuevo entorno virtual
con el siguiente comando: `py -m venv .venv`.
4. Actívalo usando `.venv\Scripts\activate`.
5. Ahora instala las dependencias necesarias mediante el archivo **requirements.txt**
usando el comando `pip install –r requirements.txt`.
6. Comprueba que **Tkinter** esté funcionando perfectamente con `python -m tkinter`.
Se brirá una ventanita de pruebas.
7. Una vez finalizado todo el proceso, ya se puede iniciar el archivo `app.py`:

```bash
py app.py
```
## Créditos finales

Autor: ***Joan Pastor Vicéns***

[Mi Github](https://github.com/Ildiar25) ~~~~~
[Mi LinkedIn](https://www.linkedin.com/in/joan-pastor-vicens-aa5b4a55)