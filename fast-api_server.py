from fastapi import File, UploadFile, FastAPI
import uvicorn
from fastapi.responses import FileResponse
from NVDI_Custom import get_nvdi_map_of_area
app = FastAPI()

@app.get('/')
def main_page():
    return {"message": "Hello, this page is empty move to /docs to see what I have"}

@app.post("/NVDI")
async def get_body(file: UploadFile = File(description="JSON file with fromat like GeoJSON")):
    try:
        content = await file.read()
        with open('json_dir/map.geojson', 'wb') as file:
            file.write(content)
        get_nvdi_map_of_area('json_dir/map.geojson')
    except Exception:
        return {'message': "File is not correct"}

    return FileResponse('imgs/map.png')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)


