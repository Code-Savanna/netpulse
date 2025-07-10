from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_devices():
    return [{"device_name": "Router"}, {"device_name": "Switch"}]
