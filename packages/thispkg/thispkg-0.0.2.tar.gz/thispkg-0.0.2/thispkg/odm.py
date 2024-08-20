from __future__ import annotations
from functools import cached_property
from typing import Any, Union, Optional, Annotated
import os
import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, computed_field, WithJsonSchema, Field
from typing_extensions import TypedDict, Required
from types import coroutine

from .ouid import ouid
from .utils import  get_logger
from .similarity_search.similarity_search import similarity_search
from .base.quipubase import Quipu

PREFIX = "/tmp/"

logger = get_logger("DocumentObject >")


class DocumentObject(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
        "extra": "allow",
    }

    @computed_field(return_type=str)
    @cached_property
    def object(self) -> str:
        return self.__class__.__name__.lower()

    @classmethod
    def generate_id(cls) -> str:
        return ouid(cls.__name__)

    @computed_field(return_type=str)
    @property
    def id(self) -> str:
        return ouid(self.__class__.__name__)

    @classmethod
    @coroutine
    def get(cls, *, vector_store_id: str, id: str):
        try:
            db = cls.db(vector_store_id=vector_store_id)
            yield
            data = db.get_doc(id=id)
            if data:
                return cls.model_validate(data)
            else:
                return None
        except KeyError:
            raise ValueError(f"DocumentChunk with id {id} not found.")
        except Exception as e:
            raise e

    @classmethod
    @coroutine
    def scan(cls, *, vector_store_id: str):
        db = cls.db(vector_store_id=vector_store_id)
        yield
        return [
            cls.model_validate(i)  # pylint: disable=E1101
            for i in db.scan_docs(limit=100, offset=0)
        ]

    @classmethod
    @coroutine
    def find(
        cls, *, vector_store_id: str, limit: int = 25, offset: int = 0, **kwargs: Any
    ):
        db = cls.db(vector_store_id=vector_store_id)
        response = db.find_docs(limit=limit, offset=offset, kwargs=kwargs)
        yield
        return [cls.model_validate(i) for i in response]

    @classmethod
    @coroutine
    def delete(cls, *, vector_store_id: str, id: str):
        try:
            cls.db(vector_store_id=vector_store_id).delete_doc(id)
            yield
        except KeyError:
            raise ValueError(f"DocumentChunk with id {id} not found.")
        except Exception as e:
            logger.error("Error deleting DocumentChunk. %s", e)
            raise e

    @classmethod
    @coroutine
    def destroy(cls, *, vector_store_id: str):
        try:
            os.remove(PREFIX + vector_store_id)
            yield
        except Exception as e:
            logger.error("Error destroying DocumentChunk. %s", e)
            raise e

    @classmethod
    @coroutine
    def create_database(cls, *, vector_store_id: str):
        try:
            cls.db(vector_store_id=vector_store_id)
            yield
        except Exception as e:
            logger.error("Error creating DocumentChunk database. %s", e)
            raise e

    @classmethod
    def db(cls, *, vector_store_id: str):
        return Quipu(PREFIX + vector_store_id)

    @coroutine
    def put(self, *, vector_store_id: str):
        try:
            self.db(vector_store_id=vector_store_id).put_doc(self.id, self.model_dump())
            yield
            return self
        except Exception as e:
            logger.error("Error setting DocumentChunk. %s", e)
            raise e


class Embedding(DocumentObject):
    content: str = Field(...)
    embedding: Annotated[
        NDArray[Union[np.float32, np.float64, np.float128, np.float16]],
        WithJsonSchema({"type:": "array", "items": {"type": "number"}}),
    ]

    @classmethod
    def model_validate(
        cls, 
        *,
        obj: dict[str, Any], 
        strict: Optional[bool] = None,  
        from_attributes: Optional[bool] = None,
        context: Optional[dict[str, Any]] = None
    ) -> Embedding:
        # Ensure the embedding is correctly parsed as a NumPy array
        try:
            embedding = np.array(obj.get("embedding"), dtype=np.float32)  # Default to float32 for consistency
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid embedding data: {e}")

        # Handle missing or malformed data gracefully
        if not embedding.size:
            raise ValueError("Embedding cannot be empty.")

        return Embedding(
            id=obj.get("id", cls.generate_id()),  # Generate a default ID if not provided
            object=obj.get("object", "embedding"),  # Default to 'embedding' if not provided
            content=obj.get("content", ""),  # Provide a default empty string for content
            embedding=embedding,
        )
