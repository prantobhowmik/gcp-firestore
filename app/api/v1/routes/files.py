from fastapi import APIRouter, UploadFile, File, Form, Body

from app.models.file_model import (
    FileUploadRequest,
    FileMetadataUpdate,
    FileReplaceRequest,
    FileUploadResponse,
    GetFilesResponse,
    FileUpdateResponse,
    DeleteFileResponse
)

from app.services.firestore_service import (
    service_upload_file,
    service_get_all_files,
    service_replace_file,
    service_update_metadata,
    service_delete_file
)


router = APIRouter()


@router.post("/", response_model=FileUploadResponse)
async def upload(
    file: UploadFile = File(...),
    file_name: str = Form(...)
):
    req = FileUploadRequest(file_name=file_name)
    return await service_upload_file(file, req)


@router.get("/", response_model=GetFilesResponse)
async def get_all():
    return await service_get_all_files()


@router.put("/{file_id}", response_model=FileUpdateResponse)
async def replace_file(
    file_id: str,
    file: UploadFile = File(...),
    file_name: str = Form(...)
):
    req = FileReplaceRequest(file_name=file_name)
    return await service_replace_file(file_id, file, req)


@router.patch("/{file_id}", response_model=FileUpdateResponse)
async def update_meta(
        file_id: str,
        payload: FileMetadataUpdate = Body(...)
):
    return await service_update_metadata(file_id, payload)


@router.delete("/{file_id}", response_model=DeleteFileResponse)
async def delete(file_id: str):
    return await service_delete_file(file_id)
