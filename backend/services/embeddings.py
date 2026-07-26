#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------

import asyncio 
from typing import List 
from openai import OpenAI,OpenAIError

from backend.config import settings 

client = OpenAI(api_key=settings.openai_api_key)
EMBEDDING_MODEL = settings.openai_embedding_model

async def embed_texts(texts : List[str]) -> List[List[float]]:
    """
        Embed a batch of text using OPENAI
        Args:
            texts(List[str]) : the text which neeed to embed 
        Returns:
            List[List[float]] : embeddings vectors
    """

    def _embed():
        results = [] 
        batch_size = 100 
        try:
            for i in range(0 , len(texts) , batch_size):
                batch = texts[i : i +batch_size]
                response = client.embeddings.create(model = EMBEDDING_MODEL , input = batch)
                results.extend([item.embedding for item in response.data])
            return results 
        except OpenAIError as e:
            raise RuntimeError(f"Embedding failed: {e}")
    return await asyncio.to_thread(_embed)

async def embed_query(query : str) -> List[float]:
    """
        Embed a single search query
        Args:
            query(str) : query that user ask
        Returns:
            List[float] : will return embedding for that query or question
    """
    return (await embed_texts([query]))[0]

async def embed_documents(text : List[str]) -> List[List[float]]:
    """
        Embed the list of text 
        Args:
            text(List[str]) : List of text which need to be embed
        Returns :
            return List[List[float]]
    """
    return await embed_texts(text)