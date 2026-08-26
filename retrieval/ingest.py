from pathlib import Path
from pypdf import PdfReader
import chromadb


DATA_DIR = Path("data")
DB_DIR = Path("chroma_db")


client = chromadb.PersistentClient(
    path=str(DB_DIR)
)

collection = client.get_or_create_collection(
    name="parcelpilot_documents"
)


def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text
        })

    return pages


def chunk_text(text, chunk_size=1000, overlap=150):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def ingest_documents():

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    documents = []
    metadatas = []
    ids = []

    counter = 0

    for pdf_path in pdf_files:

        print(f"Processing: {pdf_path.name}")

        pages = extract_pdf_text(pdf_path)

        for page_data in pages:

            chunks = chunk_text(
                page_data["text"]
            )

            for chunk_index, chunk in enumerate(chunks):

                documents.append(chunk)

                metadatas.append({
                    "source": pdf_path.name,
                    "page": page_data["page"],
                    "chunk": chunk_index
                })

                ids.append(
                    f"{pdf_path.stem}_{page_data['page']}_{chunk_index}_{counter}"
                )

                counter += 1

    if not documents:
        print("No documents found.")
        return

    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(
        f"Successfully indexed {len(documents)} chunks."
    )


if __name__ == "__main__":
    ingest_documents()