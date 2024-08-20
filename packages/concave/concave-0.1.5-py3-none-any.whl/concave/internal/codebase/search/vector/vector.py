# import os
#
# from llama_index.core import VectorStoreIndex, StorageContext, Document
# from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
# from llama_index.core.storage.docstore import SimpleDocumentStore
# from llama_index.core.vector_stores import VectorStoreQuery
# from llama_index.vector_stores.milvus import MilvusVectorStore
#
#
# class VectorSearchRes:
#
#     def __init__(self, raw):
#         self.nodes = raw.nodes
#         self.similarities = raw.similarities
#         self.ids = raw.ids
#
#     def print(self):
#         print("=" * 30)
#         print("| VECTOR SEARCH RESULTS")
#         print(f"| Found {len(self.nodes)} nodes")
#         print("=" * 30)
#         for i, node in enumerate(self.nodes):
#             index = str(i + 1).rjust(4, " ")
#             print(f"{index}  | {self.similarities[i]} {node.metadata['symbol']}")
#
#
# class VectorSearcher:
#
#     def __init__(self, path):
#         files = os.listdir(path)
#
#         uri = None
#         for file in files:
#             if file.startswith("vector") and file.endswith(".db"):
#                 uri = os.path.join(path, file)
#                 break
#
#         if uri is None:
#             raise FileNotFoundError(f"Path {path} does not contain vector*.db")
#
#         self._vector_store = MilvusVectorStore(
#             uri=uri, dim=1536, overwrite=False
#         )
#         from llama_index.embeddings.voyageai import VoyageEmbedding
#
#         if "VOYAGE_API_KEY" not in os.environ:
#             raise ValueError(
#                 "VOYAGE_API_KEY environment variable is not set. Please set it to your Voyage API key."
#             )
#
#         self._embed_model = VoyageEmbedding(
#             model_name="voyage-code-2",
#             voyage_api_key=os.environ.get("VOYAGE_API_KEY"),
#             truncation=True,
#             embed_batch_size=128,
#         )
#
#     def search(self, query, top_k=500):
#         query_embedding = self._embed_model.get_query_embedding(query)
#         query_bundle = VectorStoreQuery(
#             query_str=query,
#             query_embedding=query_embedding,
#             similarity_top_k=top_k
#         )
#         result = self._vector_store.query(query_bundle)
#
#         return VectorSearchRes(result)
#
#
# class VectorIndexer:
#     documents = []
#
#     def __init__(self, name):
#         self._vector_store = MilvusVectorStore(
#             uri=f"./{name}.db", dim=1536, overwrite=True
#         )
#         self._docstore = SimpleDocumentStore()
#
#         from llama_index.embeddings.voyageai import VoyageEmbedding
#
#         if "VOYAGE_API_KEY" not in os.environ:
#             raise ValueError(
#                 "VOYAGE_API_KEY environment variable is not set. Please set it to your Voyage API key."
#             )
#
#         self._embed_model = VoyageEmbedding(
#             model_name="voyage-code-2",
#             voyage_api_key=os.environ.get("VOYAGE_API_KEY"),
#             truncation=True,
#             embed_batch_size=128,
#         )
#
#         self.embed_pipeline = IngestionPipeline(
#             transformations=[self._embed_model],
#             docstore_strategy=DocstoreStrategy.UPSERTS_AND_DELETE,
#             docstore=self._docstore,
#             vector_store=self._vector_store,
#         )
#
#     def add_document(self, text, metadata=None):
#         self.documents.append(Document(
#             text=text,
#             mimetypes="text/x-python",
#             metadata=metadata,
#         ))
#
#     def commit(self, show_progress=False):
#         self.embed_pipeline.run(show_progress=show_progress, documents=self.documents, num_workers=1)
#         self.documents = []
