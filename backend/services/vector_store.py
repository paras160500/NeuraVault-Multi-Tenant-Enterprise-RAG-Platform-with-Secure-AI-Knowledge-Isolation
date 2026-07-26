#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------

import asyncio
from typing import List, Dict, Any 
from pinecone import Pinecone, ServerlessSpec
from backend.config import settings 

#---------------------Singleton Pinecone Client-------------------------
_pc : Pinecone | None = None
_index = None

#-------------------------Main Function Logic----------------------------

def _get_client() -> Pinecone:
    """
        Getting singleton client object which can use multiple times
    """
    # Telling that this is global variable ref 
    global _pc 
    # Check if the _pc initialize or not 
    if _pc is None:
        _pc = Pinecone(api_key=settings.pinecone_api_key)
    return _pc 


def get_index():
    """
        Making the index if its not there, getting the name of the index
        from the env variable
    """
    # make it global
    global _index
    # check if the _index is there or not 
    if _index is None:
        # getting client
        pc = _get_client()
        # Getting the index name list 
        existing = [i.name for i in pc.list_indexes()]
        # If the name of our index is not in the existing 
        if settings.pinecone_index_name not in existing:
            # Create index first 
            pc.create_index(
                name = settings.pinecone_index_name,
                dimension = 1536,                               # We are using openai 
                metric = "cosine",
                spec=ServerlessSpec(cloud="aws",region=settings.pinecone_environment)
            )
        # make the _index
        _index = pc.Index(settings.pinecone_index_name)
    return _index 


#-------------------------Vector Operations----------------------------

class VectorStore:
    """
        All operations are scoped to a user's namespace = user_id
        This guarantees complete tenant isoldation inside a single Pinecone index
    """

    def __init__(self , namespace : str):
        self.namespace = namespace
        self.index = get_index()


    async def upsert_chunks(self, vectors: List[Dict[str , Any]]) -> int:
        """
            For upserting the chunks to the vectorstore
            Args:
                vectors(List[Dict[str,Any]]): list of {"id" : str,"values" : List[float], "metadata" : dict}
            Returns:
                number of upserted vectors
        """
        # This function takes time because of the self.index.upsert that is not async its sync function
        # So that will block that whole thread so we have to user asyncio.to_thread
        def _upsert():
            batch_size = 100 
            total = 0 

            for i in range(0 , len(vectors) , batch_size):
                batch = vectors[i : i + batch_size]
                self.index.upsert(vectors = batch , namespace=self.namespace)
                total += len(batch)
            return total 

        return await asyncio.to_thread(_upsert)


    async def query(self , vector : List[float] , top_k : int = 5 , filter : Dict | None = None) -> List[Dict[str,Any]]:
        """
            for querying the pinecone and getting the result of the query
            Returns list of matches with id, score, metadata.
            Args:
                vector(List[float]) : the query which is converted into embeddings
                top_k(int) : top items 
                filter(dict) : Filters
            Returns:
                Query result of matches in the form of List[Dict[str,Any]]
        """

        def _query():
            # First lets make a dict having all the needed parameters in dict because we have
            # a filter a optional so sometime that can be none so for that we use this dict **kwargs method
            kwargs = dict(
                vector = vector,
                top_k = top_k,
                namespace = self.namespace,
                include_metadata = True 
            )

            if filter:
                kwargs['filter'] = filter 

            return self.index.query(**kwargs)

        result = await asyncio.to_thread(_query)
        return [
            {
                "id" : m.id,
                "score" : m.score,
                "text" : m.metadata.get("text" , ""),
                "source" : m.metadata.get("source" , ""),
                "chunk_index" : m.metadata.get("chunk_index" , 0)
            } for m in result.matches
        ]


    async def delete_by_source(self, source : str):
        """
            Delete all vectors belonging to a specific document
            Args:
                source(str) : Name of the document.
        """

        def _delete():
            results = self.index.query(
                vector = [0.0] * 1536,
                top_k = 10000,
                namespace = self.namespace,
                filter = {"source" : {'$eq' : source}},
                include_metadata=False
            )
            ids = [m.id for m in results.matches]
            if ids:
                self.index.delete(ids=ids , namespace=self.namespace)

        await asyncio.to_thread(_delete)


    async def delete_namespace(self):
        """
            Delete whole namespace
        """
        def _delete_namespace():
            self.index.delete(delete_all=True , namespace=self.namespace)

        await asyncio.to_thread(_delete_namespace)


    async def namespace_stats(self) -> Dict[str,Any]:
        """
            get the information of a particular namespace
        """
        stats = await asyncio.to_thread(self.index.describe_index_stats)
        ns = stats.namespaces.get(self.namespace , {})
        return {
            "vector_count" : ns.get("vector_count" , 0),
            "namespace" : self.namespace
        }