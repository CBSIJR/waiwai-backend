import re
from typing import List, Union
from uuid import uuid4

from fastapi import UploadFile, status

from backend.schemas import AttachmentData, CustomHTTPException
from backend.utils import get_logger


class Local:
    async def __call__(self, file: UploadFile) -> AttachmentData:
        get_logger().debug(file)
        return await self.upload(file=file)

    @staticmethod
    async def upload(
        *, file: Union[UploadFile, List[UploadFile]]
    ) -> AttachmentData:
        file_type = file.content_type
        file_size = file.size
        file_name = re.sub(r'[^\w.]', '_', file.filename.lower())
        file_uuid = uuid4()
        if file is None:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Arquivo não encontrado.',
            )
        if not file_type or not (
            file_type.startswith('audio') or file_type.startswith('image')
        ):
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Tipo de arquivo inválido.',
            )
        if file_size == 0:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Arquivo inválido.',
            )
        if len(file_name) < 10 or len(file_name) > 200:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Nome de arquivo inválido.',
            )

        try:
            file_object: bytes = await file.read()
            filename = f'/{str(file_uuid)}-{file_name}'
            filedir = f'backend/static{filename}'
            with open(filedir, 'wb') as fh:
                fh.write(file_object)
            fh.close()
            await file.close()
            return AttachmentData(
                uuid=file_uuid,
                filename=filename,
                filedir=filedir,
                url=f'',
                content_type=file.content_type,
            )

        except Exception as e:
            raise CustomHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Erro ao salvar o arquivo: {str(e)}.',
            )
