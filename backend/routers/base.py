from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings

from backend.utils import get_logger as logger


class FileData(UploadFile):
    """
    Represents the result of an upload operation
    Attributes:
        file (Bytes): File saved to memory
        path (Path | str): Path to file in local storage
        url (HttpUrl | str): A URL for accessing the object.
        size (int): Size of the file in bytes.
        filename (str): Name of the file.
        status (bool): True if the upload is successful else False.
        error (str): Error message for failed upload.
        message: Response Message
    """
    path: Path | str = ''
    url: HttpUrl | str = ''
    status: bool = True
    error: str = ''
    message: str = ''


class CloudUpload(ABC):
    """
    Methods:
        upload: Uploads a single object to the cloud
        multi_upload: Upload multiple objects to the cloud
    Attributes:
        config: A config dict
    """

    def __init__(self, config: BaseSettings | None = None):
        """
        Keyword Args:
            config (dict): A dictionary of config settings
        """
        self.config = config

    async def __call__(
        self,
        file: UploadFile | None = None,
    ) -> FileData:
        try:
            if file:
                return await self.upload(file=file)
            else:
                return FileData(
                    status=False,
                    error='No file or static provided',
                    message='No file or static provided',
                )
        except Exception as err:
            return FileData(
                status=False,
                error=str(err),
                message='File upload was unsuccessful',
            )

    @abstractmethod
    async def upload(self, *, file: UploadFile) -> FileData:
        """"""


class Local(CloudUpload):
    """
    Local storage for FastAPI.
    """

    async def upload(self, *, file: UploadFile) -> FileData:
        """
        Upload a file to the destination.
        Args:
            file UploadFile: File to upload
        Returns:
            FileData: Result of file upload
        """
        try:
            dest = (
                self.config.static_path / f'{file.filename}'
            )
            file_object = await file.read()
            with open(f'{dest}', 'wb') as fh:
                fh.write(file_object)
            await file.close()
            return FileData(
                path=dest,
                message=f'{file.filename} saved successfully',
                content_type=file.content_type,
                size=file.size,
                filename=file.filename,
            )
        except Exception as err:
            logger.error(
                f'Error uploading file: {err} in {self.__class__.__name__}'
            )
            return FileData(
                status=False, error=str(err), message=f'Unable to save file'
            )
