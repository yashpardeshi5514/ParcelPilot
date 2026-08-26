import chromadb


DB_DIR = "chroma_db"


client = chromadb.PersistentClient(
    path=DB_DIR
)

collection = client.get_or_create_collection(
    name="parcelpilot_documents"
)


def search_documents(query, n_results=5):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    output = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        output.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"]
        })

    return output