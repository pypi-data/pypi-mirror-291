from typing import Literal, Union, List
from typing_extensions import TypedDict, Required
import numpy as np
from numpy.typing import NDArray

class Embedding(TypedDict, total=False):
    vector: Required[NDArray[Union[np.float32, np.float64, np.float128, np.float16]]]
    id: Required[str]
    content: Required[str]

class Query(TypedDict, total=False):
    vector: Required[NDArray[Union[np.float32, np.float64, np.float128, np.float16]]]
    topK: Required[int]

class Result(TypedDict, total=False):
    id: Required[str]
    score: Required[float]

def similarity_search(
    *,
    query: Query,
    embeddings: List[Embedding],
    algorithm: Literal["cosine", "euclidean", "dot"]
) -> List[Result]:
    """
    Computes the similarity between a query embedding and a list of embeddings using the specified algorithm.

    Parameters:
        query (Query): The query embedding and the number of results to return.
        embeddings (List[Embedding]): The list of embeddings to compare against the query.
        algorithm (Literal['cosine', 'euclidean', 'dot']): The similarity algorithm to use.

    Returns:
        List[Result]: The list of results with the id and score.
    """
    ...
