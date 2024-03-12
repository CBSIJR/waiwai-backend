from logging import Logger

from fastapi import APIRouter, Depends, UploadFile, status

from backend.utils import get_logger

router = APIRouter(
    prefix='/words/{word_id}/uploads',
    tags=['Uploads'],
)


@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def create_upload_file(
    word_id: int, file: UploadFile, logger: Logger = Depends(get_logger)
):
    logger.debug(file.filename)
    # return {"filename": file.filename}
