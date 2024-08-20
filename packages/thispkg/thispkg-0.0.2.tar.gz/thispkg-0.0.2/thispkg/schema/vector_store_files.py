from datetime import datetime
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class AutoChunkingStrategy(BaseModel):
    type: str = Field(default="auto")
    max_chunk_size_tokens: int = Field(default=800, ge=100, le=4096)
    chunk_overlap_tokens: int = Field(default=400, ge=50, le=2048)


class StaticChunkingProperties(BaseModel):
    max_chunk_size_tokens: int = Field(default=800, ge=100, le=4096)
    chunk_overlap_tokens: int = Field(default=400, ge=50, le=2048)


class StaticChunkingStrategy(BaseModel):
    type: Literal["static"] = Field(default="static")
    static: StaticChunkingProperties


class CreateVectorStoreFile(BaseModel):
    file_id: str = Field(
        ...,
        description="A File ID that the knowledge store should use. Useful for tools like file_search that can access files.",
    )
    chunking_strategy: Optional[Union[AutoChunkingStrategy, StaticChunkingStrategy]] = (
        Field(
            default=None,
            description="The chunking strategy used to chunk the file(s). If not set, will use the auto strategy.",
        )
    )


class VectorStoreFile(BaseModel):

    model_config = {"extra": "allow"}
    id: str
    object: Literal["vector_store.file"] = Field(
        default="vector_store.file", description="The object type"
    )
    usage_bytes: int = Field(
        default=0,
        description="The total knowledge store usage in bytes. Note that this may be different from the original file size.",
    )
    created_at: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description="The Unix timestamp (in seconds) for when the knowledge store file was created.",
    )
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the File is attached to."
    )
    status: Literal["in_progress", "completed", "cancelled", "failed"] = Field(
        default="in_progress", description="The status of the knowledge store file."
    )
    last_error: Optional[Any] = Field(
        default=None,
        description="The last error associated with this knowledge store file. Will be null if there are no errors.",
    )
    chunking_strategy: Optional[Union[AutoChunkingStrategy, StaticChunkingStrategy]] = (
        Field(default=None, description="The strategy used to chunk the file.")
    )


class ListVectorStoreFiles(BaseModel):
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the files belong to."
    )
    limit: Optional[int] = Field(
        default=20,
        ge=1,
        le=100,
        description="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.",
    )
    order: Optional[Literal["asc", "desc"]] = Field(
        default="desc",
        description="Sort order by the created_at timestamp of the objects.",
    )
    after: Optional[str] = Field(
        default=None, description="A cursor for use in pagination."
    )
    before: Optional[str] = Field(
        default=None, description="A cursor for use in pagination."
    )
    filter: Optional[Literal["in_progress", "completed", "failed", "cancelled"]] = (
        Field(default=None, description="Filter by file status.")
    )


class RetrieveVectorStoreFile(BaseModel):
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the file belongs to."
    )
    file_id: str = Field(..., description="The ID of the file being retrieved.")


class DeleteVectorStoreFile(BaseModel):
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the file belongs to."
    )
    file_id: str = Field(..., description="The ID of the file to delete.")


class VectorStoreFileBatch(BaseModel):
    id: str = Field(
        ..., description="The identifier, which can be referenced in API endpoints."
    )
    object: Literal["vector_store.file_batch"] = "vector_store.file_batch"
    created_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the knowledge store files batch was created.",
    )
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the File is attached to."
    )
    status: Literal["in_progress", "completed", "cancelled", "failed"] = Field(
        ..., description="The status of the knowledge store files batch."
    )
    file_counts: dict[str, int] = Field(
        ..., description="The number of files in different states."
    )


class CreateVectorStoreFileBatch(BaseModel):
    vector_store_id: str = Field(
        ...,
        description="The ID of the knowledge store for which to create a File Batch.",
    )
    file_ids: List[str] = Field(
        ...,
        description="A list of File IDs that the knowledge store should use. Useful for tools like file_search that can access files.",
    )
    chunking_strategy: Optional[Union[AutoChunkingStrategy, StaticChunkingStrategy]] = (
        Field(
            default=None,
            description="The chunking strategy used to chunk the file(s). If not set, will use the auto strategy.",
        )
    )


class RetrieveVectorStoreFileBatch(BaseModel):
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the file batch belongs to."
    )
    batch_id: str = Field(..., description="The ID of the file batch being retrieved.")


class CancelVectorStoreFileBatch(BaseModel):
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the file batch belongs to."
    )
    batch_id: str = Field(..., description="The ID of the file batch to cancel.")


class ListVectorStoreFilesInBatch(BaseModel):
    vector_store_id: str = Field(
        ..., description="The ID of the knowledge store that the files belong to."
    )
    batch_id: str = Field(
        ..., description="The ID of the file batch that the files belong to."
    )
    limit: Optional[int] = Field(
        default=20,
        ge=1,
        le=100,
        description="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.",
    )
    order: Optional[Literal["asc", "desc"]] = Field(
        default="desc",
        description="Sort order by the created_at timestamp of the objects.",
    )
    after: Optional[str] = Field(
        default=None, description="A cursor for use in pagination."
    )
    before: Optional[str] = Field(
        default=None, description="A cursor for use in pagination."
    )
    filter: Optional[Literal["in_progress", "completed", "failed", "cancelled"]] = (
        Field(default=None, description="Filter by file status.")
    )


class SimilaritySearchResult(BaseModel):
    id: str
    file_id: str
    score: float
    label: str
