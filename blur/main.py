from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image, ImageFilter
import io

app = FastAPI()

@app.post("/blur")
async def blur(file: UploadFile = File(...), radius: int = 15):
    image = Image.open(io.BytesIO(await file.read()))
    out = image.filter(ImageFilter.GaussianBlur(radius))

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
