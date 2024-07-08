from pinecone import Index, init

from config.logger import log

class VectorDatabase():

    def __init__(self,  vectorKey: str, vectorEnv: str, vectorIndex: str):
        log.info(f"Connecting To Vector Database @ Host: {vectorEnv}")
        init(api_key=vectorKey, environment=vectorEnv)
        self.instance = Index(vectorIndex)

    def query(self, embeddings, topK, namespace):
        self.instance.query(queries=[embeddings.tolist()], top_k=topK, namespace=namespace)

    def update(self, vectorName, embeddings, chunk, namespace):
        self.instance.upsert(vectors=[(vectorName, embeddings.tolist(), chunk)], namespace=namespace)