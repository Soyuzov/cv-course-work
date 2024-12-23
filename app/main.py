from app.services import recognize_text
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import aiofiles

app = FastAPI()

@app.post("/get-text")
async def extract_text(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    image_path = os.path.join(temp_dir, file.filename)

    try:
        # Сохранение загруженного файла асинхронно
        async with aiofiles.open(image_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        # Вызов функции распознавания текста
        text = recognize_text(image_path)

        if not text:
            raise HTTPException(status_code=404, detail="No text found in the image.")

        # Удаление временного файла
        os.remove(image_path)

        # Фильтрация пустых строк
        text_lines = [line for line in text.splitlines() if line.strip()]

        return JSONResponse(content={"extracted_text": text_lines})

    except Exception as e:
        # Обработка ошибок и удаление временного файла в случае ошибки
        if os.path.exists(image_path):
            os.remove(image_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
