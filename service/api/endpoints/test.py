from fastapi import APIRouter, UploadFile, HTTPException
from PIL import Image
from io import BytesIO
import numpy as np


test_router =  APIRouter()
@test_router.get("/test")
def testing(im: UploadFile):
    
    return {"testing":"testing"}