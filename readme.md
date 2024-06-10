## Evaluacion Teórica

#### DynamoDB

1. **Explica la diferencia entre una clave de partición y una clave de ordenación en DynamoDB.**

   - **Clave de partición (Partition Key):** Es la clave primaria simple que define la partición donde los datos se almacenarán. DynamoDB usa el valor de la clave de partición como una entrada para una función hash interna. Este valor determina en qué partición física se almacenarán los datos, distribuyendo la carga y escalando de manera eficiente.
   - **Clave de ordenación (Sort Key):** Cuando se usa en conjunto con una clave de partición, forma una clave primaria compuesta. La clave de ordenación permite almacenar múltiples elementos con la misma clave de partición pero con diferentes valores de clave de ordenación. Esto permite organizar los datos de manera jerárquica y realizar consultas más complejas dentro de un conjunto de datos que comparten la misma clave de partición.

2. **¿Qué estrategias usarías para garantizar la vitalidad de la data de la aplicación en una base de datos DynamoDB distribuida?**

   - **Control de versiones:** Utilizar atributos de versión en los ítems para manejar actualizaciones concurrentes y evitar inconsistencias.
   - **Índices Secundarios Globales (GSI):** Para mejorar la disponibilidad y velocidad de acceso a diferentes vistas de los datos.
   - **Copia de Seguridad y Recuperación:** Implementar backups automáticos y recuperación ante desastres para asegurar que los datos no se pierdan.
   - **Replicación entre regiones:** Utilizar DynamoDB Global Tables para replicar datos automáticamente entre regiones y mejorar la disponibilidad y resistencia a fallos.
   - **Monitoreo y Alerta:** Configurar Amazon CloudWatch para monitorear métricas de DynamoDB y configurar alarmas para detectar y responder a problemas de rendimiento o disponibilidad.

#### Cognito

1. **¿Cuáles son los principales componentes de Amazon Cognito y cómo se utilizan en una aplicación?**

   - **User Pools:** Proporcionan servicios de registro y autenticación para usuarios. Permiten gestionar usuarios y sus atributos, y soportan autenticación multifactor, verificación de email y teléfono, entre otros.
   - **Identity Pools:** Permiten obtener credenciales temporales para acceder a otros servicios de AWS, permitiendo que los usuarios autenticados e invitados accedan a los recursos de AWS de manera segura.
   - **Federated Identities:** Permiten a los usuarios iniciar sesión con identidades externas como Facebook, Google, Amazon o cualquier proveedor de identidad compatible con OpenID Connect (OIDC).

2. **Describe el proceso de autenticación y autorización en Cognito.**

   - **Autenticación:** El usuario ingresa sus credenciales (por ejemplo, usuario y contraseña) y Cognito verifica estos datos contra el User Pool. Si la autenticación es exitosa, se emiten tokens (ID token, Access token y Refresh token).
   - **Autorización:** Los tokens obtenidos tras la autenticación se utilizan para autorizar las solicitudes del usuario. El Access token se utiliza para acceder a recursos protegidos por Cognito, mientras que los Identity Pools usan estos tokens para proporcionar credenciales temporales que permiten al usuario acceder a otros servicios de AWS.

#### Lambda, Step Functions y AppSync

1. **¿Cuál es la función de AWS Lambda en el contexto de un backend serverless?**

   AWS Lambda permite ejecutar código en respuesta a eventos sin aprovisionar o gestionar servidores. En un backend serverless, Lambda puede ejecutar lógica de negocio en respuesta a solicitudes HTTP, eventos de bases de datos, colas de mensajes, cambios en almacenamiento S3, entre otros.

2. **Explica cómo usar AWS Step Functions para orquestar flujos de trabajo en aplicaciones serverless.**

   AWS Step Functions permite diseñar y ejecutar flujos de trabajo compuestos por una secuencia de tareas, donde cada tarea puede ser una función Lambda u otros servicios de AWS. Permite manejar las ejecuciones, errores y tomar decisiones basadas en la lógica de negocio definida en el flujo de trabajo.

3. **¿Qué es AWS AppSync y cómo se relaciona con GraphQL?**

   AWS AppSync es un servicio que simplifica el desarrollo de aplicaciones mediante la gestión de datos en tiempo real y offline con GraphQL. AppSync proporciona una API GraphQL para interactuar con datos en DynamoDB, Lambda, y otros servicios, permitiendo a los desarrolladores definir el esquema y resolver las consultas de manera eficiente.

## Evaluacion Practica

### 1. Estructura del Proyecto

Primero definimos arquitectura y una estructura de carpetas para organizar el proyecto:

#### Arquitectura Propuesta

1. **Frontend:** Puede ser una aplicación web o móvil que interactúe con la API.
2. **API Gateway:** AWS AppSync para manejar las solicitudes GraphQL.
3. **Autenticación:** Amazon Cognito para la autenticación y autorización de usuarios.
4. **Funciones Backend:** AWS Lambda para implementar la lógica de negocio y las operaciones CRUD.
5. **Orquestación:** AWS Step Functions para manejar flujos de trabajo complejos.
6. **Base de Datos:** Amazon DynamoDB para almacenamiento de datos.
7. **Almacenamiento de Esquema:** Esquema GraphQL almacenado en el código fuente.
8. **Infraestructura como Código:** AWS SAM para definir y desplegar la infraestructura.

#### Estructura Carpetas Propuesta

```
book-management-api/
├── src/
│   ├── manage_books.py
│   ├── manage_authors.py
│   ├── manage_genres.py
│   ├── assign_genres.py
├── template.yaml
└── requirements.txt
└── readme.md
```

### 2. Estructura de la Base de Datos

#### Tabla de Libros (`Books`)

- **BookID**: Identificador único del libro (clave de partición).
- **AuthorID**: Identificador único del autor del libro.
- **Titulo**: Título del libro.
- **FechaPublicacion**: Fecha de publicación del libro.
- **GeneroID**: Identificador único del género del libro.

#### Tabla de Autores (`Authors`)

- **AuthorID**: Identificador único del autor (clave de partición).
- **Nombre**: Nombre del autor.
- **Nacionalidad**: Nacionalidad del autor.

#### Tabla de Géneros (`Genres`)

- **GenreID**: Identificador único del género (clave de partición).
- **Nombre**: Nombre del género.

#### Tabla de Relación Libro-Género (`BookGenres`)

- **BookID**: Identificador único del libro (clave de partición).
- **GenreID**: Identificador único del género (clave de ordenación).

### Relaciones entre las Tablas

1. **Relación Libro-Autor**: La tabla `Books` y la tabla `Authors` están relacionadas a través del campo `AuthorID`.
2. **Relación Libro-Género**: La tabla `Books` y la tabla `Genres` están relacionadas a través de la tabla de relación `BookGenres`, que contiene las claves de los libros y los géneros correspondientes.

### Implementación en DynamoDB

- **Tabla de Libros (`Books`)**: Utiliza `BookID` como clave de partición.
- **Tabla de Autores (`Authors`)**: Utiliza `AuthorID` como clave de partición.
- **Tabla de Géneros (`Genres`)**: Utiliza `GenreID` como clave de partición.
- **Tabla de Relación Libro-Género (`BookGenres`)**: Utiliza `BookID` como clave de partición y `GenreID` como clave de ordenación.

### Modelo de Conceptos

El modelo se basa en un diseño desnormalizado que prioriza el acceso rápido a los datos sobre la normalización. Las tablas se diseñan teniendo en cuenta las consultas que se realizarán con mayor frecuencia, lo que minimiza la necesidad de realizar operaciones de lectura o escritura costosas.

Este enfoque de diseño se alinea con las mejores prácticas de DynamoDB, que favorecen la denormalización de los datos para optimizar el rendimiento y minimizar los costos de operación.

**Usando AWS CLI**
- Este comando copia el archivo `schema.graphql` al bucket S3 `book-management-api` en la carpeta `schema/`.

```bash
aws s3 cp book-management-api/schema/schema.graphql s3://book-management-api/schema/schema.graphql
```

### 3. Desarrollo de Funciones Lambda

**Funciones Lambda CRUD para Libros:**
- [Funcion Lambda Book ](book-management-api/src/manage_books.py)
- **CreateBook:** Para crear un libro.
- **ReadBook:** Para leer detalles de un libro.
- **UpdateBook:** Para actualizar detalles de un libro.
- **DeleteBook:** Para eliminar un libro.
- **BatchDeleteBooks:** Para eliminar múltiples libros.

**Funciones Lambda CRUD para Autores:**
- [Funcion Lambda Authors ](book-management-api/src/manage_authors.py)
- **CreateAuthor:** Para crear un autor.
- **ReadAuthor:** Para leer detalles de un autor.
- **UpdateAuthor:** Para actualizar detalles de un autor.
- **DeleteAuthor:** Para eliminar un autor.

**Funciones Lambda CRUD para Géneros:**
- [Funcion Lambda Genre ](book-management-api/src/manage_genres.py)
- **CreateGenre:** Para crear un género.
- **ReadGenre:** Para leer detalles de un género.
- **UpdateGenre:** Para actualizar detalles de un género.
- **DeleteGenre:** Para eliminar un género.

**Funciones Lambda para Gestionar Relaciones:**
- [Funcion Lambda Genre To Book ](book-management-api/src/assign_genres.py)
- **AssignGenreToBook:** Para asignar un género a un libro.
- **RemoveGenreFromBook:** Para eliminar un género de un libro.

### 4. Configuración de AppSync

**Schema GraphQL:**
- [Schema Graphql ](book-management-api/schema/schema.graphql)

### 5. Autenticación con Cognito

**Configuración de User Pools y Identity Pools:**
- Crear un User Pool para gestionar la autenticación de usuarios.
- Configurar Identity Pools para obtener credenciales temporales para acceder a los servicios de AWS.

### 6. Despliegue y Pruebas

**Despliegue:**
- Utilizar AWS SAM CLI para desplegar la infraestructura en AWS.
- Asegurarse de configurar los permisos necesarios para que Lambda, Step Functions y AppSync puedan interactuar con DynamoDB y Cognito.

* empaqueta la aplicación:

```sh
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket book-management-api
```

* despliega la aplicación:

```sh
sam deploy --template-file packaged.yaml --stack-name book-management-api --capabilities CAPABILITY_IAM
```

**Pruebas:**
- Validar las operaciones CRUD para libros, autores y géneros.
- Probar las consultas y mutaciones GraphQL para asegurar que funcionan correctamente y que los índices secundarios globales (GSI) optimizan el rendimiento.
