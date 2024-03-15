from logging import Logger

from fastapi import APIRouter, Depends, UploadFile, status
from .base import FileData, Local
from backend.configs import Settings

from backend.utils import get_logger

settings = Settings()
router = APIRouter(
    prefix='/words/{word_id}/uploads',
    tags=['Uploads'],
)
local = Local(config=settings)


@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def create_upload_file(
    word_id: int, file: UploadFile, logger: Logger = Depends(get_logger)
):
    logger.debug(file)

    # @app.post('/local_upload', name='local_upload')
    # async def upload(static: list[FileData] = Depends(local)) -> list[FileData]:
    #     return static
    # return {"filename": file.filename}
