import json
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal, Required, TypedDict
from ..odm import DocumentObject


class ExpiresAfter(TypedDict):
    anchor: Required[str]
    days: Required[int]


def expires_after():
    return json.dumps({"anchor": "created_at", "days": 7})


class CreateVectorStore(BaseModel):
    file_ids: Optional[list[str]] = Field(
        default=None,
        description="List of file IDs to be added to the knowledge store, useful for tools like `file search` that can access files",
    )
    name: Optional[str] = Field(..., description="Name of the knowledge store")
    expires_after: Optional[ExpiresAfter] = Field(
        default=None, description="The expiration policy for a knowledge store"
    )
    chunking_strategy: Optional[Any] = Field(
        default=None, description="The strategy for chunking the input data."
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Metadata associated with the knowledge store"
    )


class ListVectorStore(BaseModel):
    """Query Parameters, used to fetch a subset of knowledge stores metadata got from PostgreSQL"""

    limit: Optional[int] = Field(default=20, gt=0, le=100)
    order: Optional[Literal["asc", "desc"]] = Field(
        default="desc", description="Order of the knowledge stores fetched"
    )
    after: Optional[str] = Field(
        default=None,
        description="Id of the last knowledge store fetched from the previous request",
    )
    before: Optional[str] = Field(
        default=None,
        description="Id of the first knowledge store fetched from the previous request",
    )


class RetrieveVectorStore(BaseModel):
    """Path Parameters, used to fetch a specific knowledge store metadata got from PostgreSQL"""

    vector_store_id: str = Field(
        ...,
        description="The ID of the knowledge store to be retrieved, a PATH parameter",
    )


class ModifyVectorStore(BaseModel):
    """Path Parameters, used to update a specific knowledge store metadata got from PostgreSQL"""

    name: str = Field(default=None, description="Name of the knowledge store")
    expires_after: Optional[ExpiresAfter] = Field(
        default_factory=expires_after,
        description="The expiration policy for a knowledge store",
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Metadata associated with the knowledge store"
    )


class DeleteVectorStore(BaseModel):
    """Path Parameters, used to delete a specific knowledge store metadata got from PostgreSQL"""

    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store to be deleted, a PATH parameter"
    )


class FileCount(TypedDict):
    in_progress: int
    completed: int
    failed: int
    cancelled: int
    total: int


def file_count():
    return json.dumps(
        {
            "in_progress": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0,
            "total": 0,
        }
    )


class VectorStore(DocumentObject):
    created_at: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description="The timestamp of the knowledge store creation",
    )
    name: str = Field(..., description="Name of the knowledge store")
    usage_bytes: int = Field(
        default=0, description="The total number of bytes used by the knowledge store"
    )
    file_counts: FileCount = Field(
        default_factory=file_count,
        description="The number of files in different states",
    )
    status: Literal["expired", "in_progress", "completed"] = Field(
        default="in_progress", description="The status of the knowledge store"
    )
    expires_after: Optional[ExpiresAfter] = Field(
        default=None, description="The expiration policy for a knowledge store"
    )
    expires_at: Optional[int] = Field(
        default=None, description="The timestamp of the knowledge store expiration"
    )
    last_active_at: Optional[int] = Field(
        default=None,
        description="The timestamp of the last activity on the knowledge store",
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Metadata associated with the knowledge store"
    )
