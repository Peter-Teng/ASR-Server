from fastapi import APIRouter
from . import speaker, transcribe, denoise

router = APIRouter(prefix="/v1")

router.include_router(transcribe.router, tags=["Transcription router"])
router.include_router(speaker.router, tags=["User router"])
router.include_router(denoise.router, tags=["Denoise router"])