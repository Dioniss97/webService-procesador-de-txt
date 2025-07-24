# Procesador de TXT para GladToLink (G2L)

Este proyecto es un servicio web desarrollado con FastAPI que recibe archivos de texto (TXT) en formato Base64, los procesa según reglas específicas y devuelve los datos en formato JSON. Está preparado para desplegarse fácilmente en [Render](https://render.com/).

## Características principales
- **Recibe** archivos TXT en Base64 mediante una petición POST.
- **Decodifica** el contenido y procesa línea a línea.
- **Descarta** las líneas que empiezan por `91REME` (cierres de lote).
- **Divide** cada línea válida en campos usando bloques de dos o más espacios como delimitador.
- **Devuelve** los datos en formato JSON, etiquetando los campos como `Value 1`, `Value 2`, etc.
- **Optimizado** para Render y preparado para manejar múltiples peticiones concurrentes.
- **Documentación interactiva** disponible en `/docs`.

## Estructura de archivos
- `main.py`: Código principal del servicio FastAPI.
- `requirements.txt`: Dependencias necesarias.
- `Procfile`: Comando de inicio para Render.
- `README.md`: Este archivo.

## Despliegue en Render
1. Sube el proyecto a un repositorio de GitHub.
2. Entra en [Render](https://dashboard.render.com/) y crea un nuevo "Web Service".
3. Selecciona tu repositorio y rama.
4. Render instalará automáticamente las dependencias y lanzará el servicio.

## Uso del servicio
### Endpoint principal
- **POST** `/process`
- **Cuerpo (JSON):**
  ```json
  {
    "file_b64": "<contenido_base64_del_txt>"
  }
  ```
- **Respuesta:**
  - Si hay un solo registro:
    ```json
    {
      "record": {
        "Value 1": "...",
        "Value 2": "..."
      }
    }
    ```
  - Si hay varios registros:
    ```json
    {
      "records": [
        { "Value 1": "...", "Value 2": "..." },
        { "Value 1": "...", "Value 2": "..." }
      ]
    }
    ```

### Ejemplo de petición (usando curl)
```sh
curl -X POST https://<TU_DOMINIO_RENDER>/process \
  -H "Content-Type: application/json" \
  -d '{"file_b64": "U29jaW8gICBBcGVsbGlkbyAgICBMb3MgQ2FtcG9zCk1hbnphbmEgICBNYWRyaWQgICBCYXJjZWxvbmE="}'
```

### Documentación interactiva
Accede a `/docs` en tu dominio de Render para probar el endpoint y ver la documentación generada automáticamente.

## Prueba local
1. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
2. Lanza el servidor:
   ```sh
   uvicorn main:app --reload
   ```
3. Accede a [http://localhost:8000/docs](http://localhost:8000/docs) para probar el servicio.

## Gestión de errores
- Si el Base64 es inválido o el archivo está vacío/no tiene líneas válidas, se devuelve un error claro y descriptivo.

## Licencia
MIT 