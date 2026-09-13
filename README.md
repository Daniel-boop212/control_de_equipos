# Manual de usuario - Gestion Clinica

## 1. Presentacion

Gestion Clinica es una aplicacion para registrar servicios, equipos, hojas de vida, mantenimientos, alertas, documentos PDF, imagenes y copias de seguridad relacionadas con la gestion de equipos de una clinica.

Este manual explica como abrir el programa y como usar sus funciones principales desde el punto de vista del usuario.

[Agregar imagen: pantalla principal de la aplicacion]

## 2. Como abrir el programa si se recibe en un ZIP

Si recibes la aplicacion comprimida en un archivo `.zip`, sigue estos pasos:

1. Ubica el archivo ZIP recibido.
2. Haz clic derecho sobre el ZIP.
3. Selecciona `Extraer todo`.
4. Elige una carpeta de destino, por ejemplo el Escritorio o Documentos.
5. Abre la carpeta extraida.
6. Entra en la carpeta `GestionClinica`.
7. Haz doble clic en `GestionClinica.exe`.

Importante: no abras el programa directamente desde dentro del ZIP. Primero debes extraerlo.

Tambien es importante conservar completa la carpeta `GestionClinica`. No muevas solamente el archivo `.exe`, porque la aplicacion necesita sus carpetas internas para funcionar correctamente.

[Agregar imagen: carpeta extraida con GestionClinica.exe]

## 3. Pantalla principal

Al abrir la aplicacion veras una pantalla dividida en dos zonas principales:

- Panel izquierdo: muestra el logo de la clinica, el nombre que se usara en los PDF y la lista de servicios.
- Panel derecho: muestra categorias, botones de datos, ayuda, alertas, dashboard, filtros, lista de equipos y detalles.

En la parte superior puedes elegir la categoria del equipo que vas a crear. Las categorias disponibles son:

- Biomedico
- Computo
- Refrigeracion
- Muebles y enseres
- Comunicacion

[Agregar imagen: partes de la pantalla principal]

## 4. Cambiar logo y nombre de la clinica para los PDF

La aplicacion permite personalizar el logo y el nombre que aparecen en los PDF generados.

### Cambiar el logo

1. En el panel izquierdo, ubica el logo.
2. Haz clic en el boton pequeno con icono de configuracion junto al logo.
3. Selecciona una imagen desde tu computador.
4. Confirma la seleccion.
5. El logo se actualizara en la pantalla y se usara tambien en los PDF.

Formatos recomendados:

- `.png`
- `.jpg`
- `.jpeg`

Si no eliges ningun logo desde la aplicacion, se usara el logo predeterminado ubicado en:

`assets/logo_clinica.jpg`

Si deseas cambiar el logo predeterminado antes de entregar o compilar la aplicacion, reemplaza ese archivo por tu logo manteniendo el mismo nombre:

`logo_clinica.jpg`

[Agregar imagen: boton para cambiar logo]

### Cambiar el nombre de la clinica

1. En el panel izquierdo, debajo o junto al logo, veras el nombre de la clinica.
2. Haz clic en el boton pequeno de edicion junto al nombre.
3. Escribe el nombre que quieres que aparezca en los PDF.
4. Acepta el cambio.

Desde ese momento, los PDF nuevos usaran ese nombre.

Si no hay ningun nombre configurado, la aplicacion usara como nombre predeterminado:

`Clinica`

[Agregar imagen: cambio de nombre de la clinica]

## 5. Servicios

Los servicios sirven para organizar los equipos por areas de la clinica. Algunos ejemplos son:

- Urgencias
- UCI
- Hospitalizacion
- Cirugia
- Consulta externa
- Laboratorio

### Crear un servicio

1. En el panel izquierdo, haz clic en `Agregar servicio`.
2. Escribe el nombre del servicio.
3. Acepta.
4. El servicio aparecera en la lista.

[Agregar imagen: agregar servicio]

### Seleccionar un servicio

Haz clic sobre el nombre del servicio en el panel izquierdo. Al seleccionarlo, la tabla mostrara los equipos asociados a ese servicio.

### Borrar un servicio

1. Selecciona el servicio en el panel izquierdo.
2. Haz clic en `Borrar servicio`.
3. Confirma la accion si estas seguro.

Advertencia: al borrar un servicio, tambien se eliminan los equipos asociados a ese servicio.

## 6. Equipos

Los equipos son los elementos que se registran dentro de cada servicio.

### Agregar un equipo

1. Selecciona primero el servicio donde se va a registrar el equipo.
2. En la parte superior, elige la categoria del equipo.
3. Haz clic en `Agregar`.
4. Llena el formulario.
5. Adjunta una imagen si lo deseas.
6. Haz clic en `Guardar`.

Si el formulario muestra campos obligatorios, debes completarlos antes de guardar.

[Agregar imagen: boton Agregar y formulario]

### Categorias de equipos

#### Equipo biomedico

Permite registrar informacion como:

- Imagen del equipo
- Codigo del equipo
- Registro sanitario
- Codigo del prestador
- Registro de importacion
- Nombre del equipo
- Marca
- Modelo
- Serie
- Ubicacion
- Fecha de adquisicion
- Factura
- Fecha de instalacion
- Vencimiento de garantia
- Costo
- Vida util
- Proveedor
- Telefono y contacto del proveedor
- Especificaciones tecnicas
- Tipo de equipo
- Forma de adquisicion
- Fuente de alimentacion
- Frecuencia de mantenimiento
- Si requiere calibracion
- Recomendaciones del fabricante

Campos obligatorios principales:

- Codigo del equipo
- Nombre del equipo
- Marca
- Modelo
- Serie

#### Equipo de computo

Permite registrar informacion como:

- Imagen
- Nombre
- Marca
- Modelo
- Serie
- Fecha de compra
- Garantia
- Proveedor
- Procesador
- Marca del monitor
- Serie del monitor
- Tipo de equipo

Campos obligatorios principales:

- Nombre
- Marca
- Modelo
- Serie

#### Equipo de refrigeracion

Permite registrar informacion como:

- Imagen
- Nombre
- Marca
- Modelo
- Serie
- Tipo
- Capacidad
- Fecha de compra
- Proveedor
- Garantia
- Vida util
- Telefono del proveedor
- Ubicacion

Campos obligatorios principales:

- Nombre
- Marca
- Modelo
- Serie

#### Muebles y enseres

Permite registrar informacion como:

- Imagen
- Nombre
- Tipo de elemento
- Marca
- Modelo
- Color
- Material
- Cantidad
- Estado
- Fecha de compra
- Garantia
- Proveedor
- Telefono del proveedor

Campos obligatorios principales:

- Nombre
- Tipo de elemento

#### Equipo de comunicacion

Permite registrar informacion como:

- Imagen
- Nombre
- Marca
- Modelo
- Serie
- Fecha de compra
- Garantia
- Proveedor
- Procesador
- Marca monitor
- Serie monitor
- Tipo

Campos obligatorios principales:

- Nombre
- Marca
- Modelo
- Serie

## 7. Buscar y filtrar equipos

La pantalla de equipos tiene opciones para encontrar informacion rapidamente.

### Buscar por nombre

1. Selecciona un servicio.
2. Escribe parte del nombre del equipo en el campo `Buscar`.
3. La tabla se actualizara mostrando los resultados.

### Filtrar por categoria

1. Selecciona un servicio.
2. Usa el selector de categoria del filtro.
3. Puedes elegir una categoria especifica o `Todas`.

[Agregar imagen: buscador y filtro]

## 8. Ver detalles de un equipo

1. Selecciona un servicio.
2. Haz clic sobre un equipo en la tabla.
3. Se abrira el panel de detalles.

En el panel de detalles puedes ver:

- Hoja de vida del equipo
- Datos registrados
- Historial de mantenimientos
- Documentos PDF adjuntos, cuando existan

Tambien puedes usar el boton `Detalles` para mostrar u ocultar el panel.

[Agregar imagen: panel de detalles]

## 9. Editar un equipo

1. Selecciona el equipo en la tabla.
2. Haz clic en `Editar`.
3. Modifica los datos necesarios.
4. Haz clic en `Guardar`.

La aplicacion conserva el historial de mantenimientos y documentos asociados al equipo.

## 10. Borrar un equipo

1. Selecciona el equipo en la tabla.
2. Haz clic en `Borrar`.
3. Confirma la eliminacion si estas seguro.

Advertencia: borrar un equipo elimina su registro de la lista. Antes de eliminar informacion importante, se recomienda exportar datos o conservar una copia de seguridad.

## 11. Mantenimientos

Los mantenimientos permiten llevar el historial de revisiones de cada equipo.

### Registrar un mantenimiento

1. Selecciona un equipo en la tabla.
2. Haz clic en `Mantenimiento`.
3. Registra la informacion solicitada.
4. Indica la fecha del mantenimiento y la fecha del proximo mantenimiento.
5. Escribe el responsable y la descripcion.
6. Haz clic en `Guardar`.

Tipos de mantenimiento disponibles:

- Preventivo
- Correctivo
- Calibracion
- Otro

[Agregar imagen: formulario de mantenimiento]

### Adjuntar PDF de mantenimiento o calibracion

En equipos de categoria `Biomedico`, el formulario de mantenimiento permite adjuntar:

- PDF de mantenimiento
- PDF de calibracion

Para adjuntarlos:

1. Abre el formulario de mantenimiento de un equipo biomedico.
2. Haz clic en `Cargar PDF mantenimiento` o `Cargar PDF calibracion`.
3. Selecciona el archivo PDF.
4. Guarda el mantenimiento.

Los archivos adjuntos quedaran visibles en el historial del equipo.

### Ver un PDF adjunto

1. Selecciona el equipo.
2. En el panel de detalles, busca el historial de mantenimientos.
3. Haz doble clic sobre el PDF adjunto.
4. El archivo se abrira con el visor de PDF predeterminado del computador.

### Editar un mantenimiento

1. Selecciona el equipo.
2. En el historial, haz clic derecho sobre el mantenimiento.
3. Selecciona `Editar mantenimiento`.
4. Realiza los cambios.
5. Guarda.

### Borrar un mantenimiento

1. Selecciona el equipo.
2. En el historial, haz clic derecho sobre el mantenimiento.
3. Selecciona `Borrar mantenimiento`.
4. Confirma la eliminacion.

## 12. Estados y alertas

La aplicacion muestra el estado de los equipos con colores e iconos.

Estados posibles:

- Azul: recien mantenido
- Verde: al dia
- Amarillo: proximo a vencer
- Rojo: vencido
- Gris o blanco: sin mantenimiento o sin programacion

El estado se calcula usando la fecha del proximo mantenimiento.

### Ver alertas

1. Haz clic en el boton `Alertas`.
2. La ventana mostrara los equipos que estan proximos a vencer o vencidos.
3. Revisa servicio, equipo, fecha y dias restantes.

Cuando existan alertas, el boton mostrara la cantidad de equipos pendientes.

[Agregar imagen: ventana de alertas]

## 13. Exportar hoja de vida en PDF

La hoja de vida en PDF resume la informacion del equipo.

Para exportarla:

1. Selecciona un servicio.
2. Selecciona un equipo en la tabla.
3. Haz clic en `Exportar PDF`.
4. Elige donde guardar el archivo.
5. Confirma.

El PDF incluira:

- Logo configurado o logo predeterminado
- Nombre de la clinica configurado o `Clinica`
- Datos principales del equipo
- Imagen del equipo, si existe
- Informacion detallada
- Historial de mantenimientos
- Fecha y hora de generacion

[Agregar imagen: exportacion de hoja de vida PDF]

## 14. Solicitudes de mantenimiento

La aplicacion incluye una pestaña llamada `Solicitudes de mantenimiento`.

Desde esta pestaña puedes llenar una solicitud con datos como:

- Fecha
- Responsable
- Tipo de mantenimiento
- Tipo de equipo
- Nombre del equipo
- Ubicacion
- Motivo del mantenimiento
- Fecha de reporte
- Fecha del mantenimiento
- Conclusion
- Responsable del mantenimiento
- Estado del equipo

### Exportar solicitud en PDF

1. Entra en la pestaña `Solicitudes de mantenimiento`.
2. Llena los campos necesarios.
3. Haz clic en `Exportar PDF`.
4. Elige donde guardar el archivo.
5. Confirma.

El PDF usara el mismo logo y nombre de clinica configurados para los demas PDF.

### Limpiar la solicitud

Haz clic en `Limpiar` para vaciar los campos y empezar una nueva solicitud.

[Agregar imagen: pestaña Solicitudes de mantenimiento]

## 15. Menu Datos

En la parte superior esta el boton `Datos`. Desde este menu puedes acceder a:

- Almacenamiento
- Exportar Excel
- Exportar datos
- Importar datos

[Agregar imagen: menu Datos]

## 16. Exportar equipos a Excel

Esta opcion crea un archivo Excel con la informacion de los equipos.

Para exportar:

1. Haz clic en `Datos`.
2. Selecciona `Exportar Excel`.
3. Elige si quieres exportar todos los equipos o solo una categoria.
4. Selecciona donde guardar el archivo.
5. Confirma.

El archivo generado tendra extension `.xlsx`.

## 17. Exportar datos de la aplicacion

Esta opcion sirve para crear una copia completa de los datos de la aplicacion en formato ZIP.

El ZIP puede incluir:

- Servicios
- Equipos
- Imagenes
- PDFs adjuntos
- Backups
- Logo configurado
- Nombre de la clinica configurado

Para exportar datos:

1. Haz clic en `Datos`.
2. Selecciona `Exportar datos`.
3. Elige donde guardar el archivo ZIP.
4. Confirma.

Se recomienda usar esta opcion para respaldos completos o para mover la informacion a otra instalacion.

[Agregar imagen: exportar datos]

## 18. Importar datos

Esta opcion permite cargar datos exportados previamente o datos desde una carpeta de instalacion antigua.

Para importar:

1. Haz clic en `Datos`.
2. Selecciona `Importar datos`.
3. Elige una de las opciones:
   - Archivo ZIP exportado
   - Carpeta de instalacion antigua
4. Selecciona el archivo o carpeta.
5. Lee la advertencia.
6. Confirma si estas seguro.

Advertencia: la importacion reemplaza los datos actuales por los datos importados. Antes de hacerlo, la aplicacion crea backups automaticos de los archivos actuales.

[Agregar imagen: importar datos]

## 19. Almacenamiento

La ventana de almacenamiento muestra cuanto espacio ocupan los datos de la aplicacion.

Para abrirla:

1. Haz clic en `Datos`.
2. Selecciona `Almacenamiento`.

Alli puedes ver:

- Tamaño de archivos JSON
- Tamaño de imagenes
- Tamaño de PDFs
- Total usado
- Porcentaje de uso frente a una capacidad recomendada
- Diagnostico general del almacenamiento
- Historial de backups disponibles

[Agregar imagen: ventana de almacenamiento]

## 20. Backups

La aplicacion genera copias de seguridad de los datos importantes cuando se realizan cambios.

En la ventana de almacenamiento puedes ver el historial de backups.

### Restaurar un backup

1. Abre `Datos`.
2. Selecciona `Almacenamiento`.
3. Busca la seccion de historial de backups.
4. Selecciona un backup.
5. Haz clic en `Restaurar seleccionado`.
6. Confirma la restauracion.

Advertencia: al restaurar un backup, el archivo actual sera reemplazado por la version del backup.

## 21. Ayuda dentro de la aplicacion

La aplicacion tiene un boton `Ayuda`.

Al hacer clic se abre una guia rapida con informacion sobre:

- Primeros pasos
- Equipos
- Mantenimientos
- Alertas
- PDF
- Almacenamiento
- Backups
- Consejos de uso

## 22. Recomendaciones de uso

- Crea primero los servicios antes de registrar equipos.
- Selecciona siempre el servicio correcto antes de agregar un equipo.
- Completa los campos obligatorios para evitar registros incompletos.
- Registra los mantenimientos apenas se realicen.
- Usa la fecha de proximo mantenimiento para que las alertas sean utiles.
- Adjunta PDFs de mantenimiento y calibracion cuando existan.
- Exporta datos periodicamente para conservar una copia completa.
- Antes de importar datos, verifica que estas usando el ZIP correcto.
- No elimines manualmente carpetas internas de la aplicacion.

## 23. Problemas frecuentes

### El programa no abre desde el ZIP

Extrae primero el ZIP. No ejecutes `GestionClinica.exe` directamente desde el archivo comprimido.

### El logo no aparece en los PDF

Verifica que hayas seleccionado una imagen valida desde la aplicacion. Si no configuraste un logo, revisa que exista:

`assets/logo_clinica.jpg`

### El nombre de la clinica no es el correcto en el PDF

Cambia el nombre desde el boton de edicion junto al nombre de la clinica en el panel izquierdo. Luego genera nuevamente el PDF.

### El icono del programa no cambia en Windows

Windows puede guardar iconos antiguos en cache. Si ya reemplazaste el icono y compilaste de nuevo, prueba desanclar la app de la barra de tareas y volver a abrir el ejecutable nuevo.

### No veo equipos en la tabla

Selecciona primero un servicio en el panel izquierdo. Tambien revisa que el filtro de categoria no este ocultando los equipos.

### No puedo guardar un equipo

Revisa si falta algun campo obligatorio. La aplicacion mostrara un aviso indicando cual campo falta.

### Las alertas no aparecen

Las alertas dependen de la fecha del proximo mantenimiento. Verifica que el equipo tenga un mantenimiento registrado con fecha proxima.

## 24. Archivos importantes para personalizacion

Estos archivos se usan para personalizar la aplicacion antes de compilar o entregar:

- Logo predeterminado para PDF: `assets/logo_clinica.jpg`
- Icono de la aplicacion y barra de tareas: `assets/logo_app.ico`
- Imagen alternativa de la app: `assets/logo_app.png`

Estos archivos se crean o actualizan desde la aplicacion cuando el usuario cambia configuracion:

- Logo elegido para PDF: `assets/logo_actual.txt`
- Nombre de la clinica para PDF: `assets/nombre_clinica.txt`

## 25. Cierre

Gestion Clinica esta pensada para mantener organizada la informacion de equipos, mantenimientos y documentos de soporte. El uso constante de servicios, estados, alertas, PDF y exportaciones ayuda a conservar un historial claro y facil de consultar.

