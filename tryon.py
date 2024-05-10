import os
from s3 import upload_image_file_to_s3

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from gradio_client import Client, file

router = APIRouter()

class TryonRequest(BaseModel):
    input_img: str
    garm_img: str
    selected_area: str
    
class TryonResponse(BaseModel):
    output_img: str
    
client = Client("LPDoctor/IDM-VTON-demo", hf_token="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")

@router.get("/")
def hello():
    return {"message": "Hello virtualtryon! 👋"}

@router.post("/api/tryon", tags=["tryon"], response_model=TryonResponse)
async def tryon(
    request_body: TryonRequest
):
    print(
        f"Build virtual tryon api request > area: {request_body.selected_area}, imageUrl: {request_body.input_img}")
    
    pos_image_url = request_body.input_img
    gar_image_url = request_body.garm_img
    selected_area = request_body.selected_area
    
    # 传参api call
    prediction_result = client.predict(
        dict=file(pos_image_url),
        garm_img=file(gar_image_url),
        garment_des="",
        is_checked=True,
		is_checked_crop=True,
        denoise_steps=30,
		seed=42,
		area=selected_area,
		api_name="/tryon"
    )
    
    ctime = str(os.path.getctime(prediction_result)).replace('.','')
    file_name = os.path.basename(prediction_result)
    
    output = await upload_image_file_to_s3(prediction_result, f'{ctime}_{file_name}')
    return {"output_img": output}