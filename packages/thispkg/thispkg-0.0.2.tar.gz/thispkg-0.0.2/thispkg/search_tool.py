from __future__ import annotations

from datetime import datetime
from functools import cached_property
from typing import Any, Callable, Coroutine, Literal, Optional, TypeVar, Union
import numpy as np
from numpy.typing import NDArray
import spacy  # type: ignore
from pydantic import Field
from .odm import Embedding, DocumentObject,_Query # type: ignore
from .docs import RawDoc
from .schema import AutoChunkingStrategy
from .docs import load_document, Key

T = TypeVar("T", bound=RawDoc)


class SentenceChunker(AutoChunkingStrategy):
	type: Literal["sentence"] = Field(default="sentence")  # type: ignore
	max_chunk_size_tokens: int = Field(
		default=2,
		description="The size of the paragraph in terms of number of sentences",
	)
	chunk_overlap_tokens: int = Field(
		default=0, description="The number of sentences to overlap between paragraphs"
	)
	lang: Literal["en", "es"] = Field(
		default="en", description="The language of the text"
	)

	def sentence_no(self, text: str) -> int:
		return len(list(self.language_model(text).sents))

	@cached_property
	def language_model(self):
		if self.lang == "en":
			return spacy.load("en_core_web_sm")
		elif self.lang == "es":
			return spacy.load("es_core_news_sm")
		else:
			raise ValueError("Language not supported")

	def _chunk_paragraph(self, text: str):
		sentences = list(self.language_model(text).sents)
		for i in range(0, len(sentences), self.max_chunk_size_tokens):
			chunk = sentences[i : i + self.max_chunk_size_tokens]
			yield chunk

	def _apply_overlap(self, text: str):
		paragraphs = list(self._chunk_paragraph(text))
		overlap = self.chunk_overlap_tokens
		for i in range(len(paragraphs)):
			chunk = paragraphs[i]
			if i > 0:
				overlap_chunk = paragraphs[i - 1][-overlap:]
				chunk = overlap_chunk + chunk
			yield " ".join([sentence.text for sentence in chunk])

	def chunk(self, text: str):
		for chunk in self._apply_overlap(text):
			yield chunk

	def load(self, key: Key, source: str):
		for chunk in load_document(key, source):
			yield chunk


class FileObjectDocumentChunk(Embedding):
	file_id: str = Field(...)
	vector_store_id: str = Field(...)


class VectorStoreFileDocument(DocumentObject):
	file_id: str = Field(...)
	usage_bytes: int = Field(default=0)
	created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
	vector_store_id: str
	status: Literal["in_progress", "completed", "cancelled", "failed"] = Field(
		default="in_progress"
	)
	last_error: Optional[Any] = Field(default=None)
	chunking_strategy: Optional[AutoChunkingStrategy] = Field(
		default_factory=SentenceChunker
	)
	file_type: Key = Field(...)


class FileSearchTool(DocumentObject):
	vector_store_id: str = Field(...)
	file_id: str = Field(...)
	chunking_strategy: SentenceChunker = Field(default_factory=SentenceChunker)

	async def upsert(
		self,
		embedding_function: Callable[
			[str], Coroutine[None, None, NDArray[Union[np.float32, np.float64, np.float128, np.float16]]]
		],*,
		document_type: Key,
		document_src: str
	):
		for sub_chunk in load_document(document_type, document_src):
			for chunk in self.chunking_strategy.chunk(sub_chunk):
				embedding_result = await embedding_function(chunk)
				doc = await FileObjectDocumentChunk(
						vector_store_id=self.vector_store_id,
						embedding=embedding_result, content=chunk, file_id=self.file_id
					).put(vector_store_id=self.vector_store_id)

				yield doc.content

	async def search(self, embedding_function: Callable[[str], Coroutine[None, None, NDArray[Union[np.float32, np.float64, np.float128, np.float16]]]],*,query:str, topK:int=10):
		vector = await embedding_function(query)
		q: _Query = {"vector": vector, "topK": topK}
		return Embedding.search(vector_store_id=self.vector_store_id, query=q, algorithm="cosine")