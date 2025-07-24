from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Union
import base64
import re

app = FastAPI(title="Procesador de TXT para GladToLink", description="Servicio que recibe un archivo TXT en Base64, lo procesa y devuelve los datos en formato JSON.")

class TxtBase64Request(BaseModel):
    file_b64: str

@app.post("/process", response_model=Union[Dict[str, Any], Dict[str, List[Dict[str, Any]]]])
async def process_txt(request: TxtBase64Request):
    try:
        # Decodificar Base64
        try:
            decoded_bytes = base64.b64decode(request.file_b64, validate=True)
        except Exception:
            raise HTTPException(status_code=400, detail="El archivo no está en Base64 válido.")
        decoded_text = decoded_bytes.decode("utf-8", errors="replace")
        lines = decoded_text.splitlines()
        # Filtrar líneas que no empiezan por '91REME' y no vacías
        valid_lines = [line for line in lines if line.strip() and not line.startswith("91REME")]
        if not valid_lines:
            raise HTTPException(status_code=400, detail="El archivo está vacío o no contiene líneas válidas.")
        records = []
        for line in valid_lines:
            # Dividir por dos o más espacios
            fields = re.split(r"  +", line.strip())
            record = {f"Value {i+1}": value for i, value in enumerate(fields)}
            records.append(record)
        if len(records) == 1:
            return {"record": records[0]}
        else:
            return {"records": records}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(status_code=422, content={"detail": "El cuerpo de la petición no es válido o falta el campo 'file_b64'."}) 