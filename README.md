# Fast_API

## 2. Consultar todos los datos

| No | Propiedad             | Detalle                              |
| -- | --------------------- | ------------------------------------ |
| 1  | Description           | Endpoint de Bienvenida               |
| 2  | Summary               | Regresa los contactos paginados      |
| 3  | Method                | GET                                  |
| 4  | Endpoint              | `/v1/contactos/`                     |
| 5  | Authentication        | N/A                                  |
| 6  | Query param           | limit:int&skip:int                   |
| 7  | Path param            | N/A                                  |
| 8  | Data                  | N/A                                  |
| 9  | Status code           | 200                                  |
| 10 | Response              | JSON con mensaje y fecha/hora        |
| 11 | Response type         | `application/json`                   |
| 12 | Status code (error)   | N/A                                  |
| 13 | Response type (error) | N/A                                  |
| 14 | Response (error)      | N/A                                  |
| 15 | cURL                  | `curl -X GET http://127.0.0.1:8000/` |





## 

| Campo       | Tipo         | Descripción                |
| ----------- | ------------ | -------------------------- |
| id_contacto | INTEGER (PK) | Identificador del contacto |
| nombre      | VARCHAR(100) | Nombre del contacto        |
| email       | VARCHAR(100) | Correo electrónico         |
| telefono    | VARCHAR(10)  | Número telefónico          |


##

| Propiedad        | detalle |
| ---------------- | ----- |
| response type    | application/json  |
| Status Code      | N/A   |
| Response Type    | N/A   |
| Response (error) | N/A   |
| cURL                  | `curl -X GET http://127.0.0.1:8000/` |




##


{
  "message": "Bienvenido a la API de la agenda",
  "datetime": "2026-02-09 11:17"
}


##

1. Descripcion 
2. Summary 
3. Version v1 
4. Method - post 
5. En point - /v1/contactos/{id-contacto}
6. Query param - id-contacto
7. Path param - id-contacto
8. Data NA
9. Status code 202
10. Reponse Type application/json
12. satus code.   400
13. reponse type´´    application/json
14. response(error)   {"error": "
                      error al buscar el registro}  
15. CURL 
curl -X GET http://127.0.0.1:8000/v1/contactos/3




"- Response 
no  hay registro 
{ "table" : "contactos",
"item"m: {},
"count": 0,
"datatime": timestamp,
"massage" : "contacto no encontrado"
}   



## 
1- Crear una BD en SQlite3 de nombre agendadb
2- Crear la tabla "contatcos" con los campos (id-contacto,nombre,telefono,email)
3- Insertar 100 registros
4- Programar el endpoint v1/contactos?limit&skit usando fast api 

    TODO: conectar con las base de datos agenda.db
    TODO: consultar los registros de la tabla contactos
    TODO: Formatear la respuesta con el siguiente schema:
    TODO: Responder la peticion

