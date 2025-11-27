from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


# ---------- Request Models ----------

class FileUploadRequest(BaseModel):
    file_name: str = Field(..., min_length=1)


class FileReplaceRequest(BaseModel):
    file_name: str = Field(..., min_length=1)


class FileMetadataUpdate(BaseModel):
    file_name: Optional[str] = None




# ---------- Response Models ----------

class FileData(BaseModel):
    file_id: str
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class FileUploadResponse(BaseModel):
    status: str
    message: str
    data: FileData


class GetFilesResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, FileData]


class FileUpdateResponse(BaseModel):
    success: bool
    message: str
    data: FileData


class DeleteFileResponse(BaseModel):
    success: bool
    message: str
