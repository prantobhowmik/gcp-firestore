import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from firebase_admin import storage, firestore
from fastapi import HTTPException

from app.models.file_model import (
    FileUploadRequest,
    FileReplaceRequest,
    FileMetadataUpdate,
    FileData
)

def get_db():
    """Return Firestore client after Firebase app is initialized."""
    return firestore.client()


def now_bd():
    return datetime.now(ZoneInfo("Asia/Dhaka"))



# Upload File
async def service_upload_file(file, req: FileUploadRequest):
    db = get_db()

    file_id = str(uuid.uuid4())
    file_path = f"uploads/{req.file_name}-{file_id}"

    bucket = storage.bucket()
    blob = bucket.blob(file_path)

    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()

    data = FileData(
        file_id=file_id,
        file_name=req.file_name,
        file_path=file_path,
        file_url=blob.public_url,
        created_at=now_bd()
    )

    db.collection("files").document(file_id).set(data.dict())

    return {
        "status": "success",
        "message": "File uploaded successfully",
        "data": data
    }



# Get All Files
async def service_get_all_files():
    db = get_db()
    docs = db.collection("files").stream()

    files = {}

    for doc in docs:
        raw = doc.to_dict()

        try:
            # Try using Pydantic
            file_data = FileData(**raw)
        except Exception:
            # Force minimal fallback
            file_data = FileData(
                file_id=raw.get("file_id", doc.id),
                file_name=raw.get("file_name"),
                file_path=raw.get("file_path"),
                file_url=raw.get("file_url"),
                created_at=raw.get("created_at"),
                updated_at=raw.get("updated_at")
            )

        files[doc.id] = file_data

    return {
        "success": True,
        "message": "Files retrieved successfully",
        "data": files
    }




# Replace File
async def service_replace_file(file_id: str, file, req: FileReplaceRequest):
    db = get_db()

    doc_ref = db.collection("files").document(file_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="File not found")

    old_data = doc.to_dict()

    bucket = storage.bucket()

    old_blob = bucket.blob(old_data["file_path"])
    old_blob.delete()

    new_path = f"uploads/{req.file_name}-{file_id}"
    blob = bucket.blob(new_path)

    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()

    updated_dict = {
        "file_id": file_id,
        "file_name": req.file_name,
        "file_path": new_path,
        "file_url": blob.public_url,
        "updated_at": now_bd()
    }

    doc_ref.update(updated_dict)

    updated_data = FileData(**{**old_data, **updated_dict})

    return {
        "success": True,
        "message": "File updated successfully",
        "data": updated_data
    }


# Update Metadata
async def service_update_metadata(file_id: str, req: FileMetadataUpdate):
    db = get_db()

    doc_ref = db.collection("files").document(file_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="File not found")

    # Convert Pydantic to dict, including unknown fields
    metadata = req.model_dump(exclude_unset=True)

    # Add updated_at always
    metadata["updated_at"] = now_bd()

    # Update Firestore
    doc_ref.update(metadata)

    updated_data = FileData(**doc_ref.get().to_dict())

    return {
        "success": True,
        "message": "File updated successfully",
        "data": updated_data
    }


# Delete File
async def service_delete_file(file_id: str):
    db = get_db()

    doc_ref = db.collection("files").document(file_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="File not exists")

    doc_ref.delete()

    return {
        "success": True,
        "message": "File deleted successfully",
    }
