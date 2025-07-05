import os
import json
import tempfile
from google.cloud import storage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# --- CONFIGURATION ---
GCP_PROJECT_ID = "sommas-508843"
RAW_DATA_BUCKET = "raw-data-sommas-508843"
PROCESSED_DATA_BUCKET = "processed-data-sommas-508843"
# ---------------------

def process_document(blob, bucket_name):
    """
    Downloads a file from GCS, determines its type, and uses the appropriate
    document loader and chunking strategy.
    """
    # Use a context manager for robust temporary file handling
    _, file_extension = os.path.splitext(blob.name)
    with tempfile.NamedTemporaryFile(suffix=file_extension) as temp_file:
        file_path = temp_file.name
        blob.download_to_filename(file_path)

        print(f"Processing document: {blob.name}")

        # Document-aware loading based on file extension
        if file_extension.lower() == ".pdf":
            loader = PyPDFLoader(file_path)
        elif file_extension.lower() == ".txt":
            loader = TextLoader(file_path)
        else:
            print(f"Skipping unsupported file type: {blob.name}")
            return []

        documents = loader.load()

        # Document-aware chunking strategy as per the ASRR Plan [cite: 58]
        if "emergent_intelligence_framework" in blob.name:
            # Special, fine-grained chunking for the foundational text [cite: 65]
            print("-> Applying special chunking for foundational text.")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        else:
            # Standard chunking for scientific texts and technical docs [cite: 59, 62]
            print("-> Applying standard chunking.")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)

        chunks = text_splitter.split_documents(documents)

        return chunks

def main():
    """
    Main function to orchestrate the preprocessing pipeline.
    """
    storage_client = storage.Client(project=GCP_PROJECT_ID)
    raw_bucket = storage_client.bucket(RAW_DATA_BUCKET)
    
    all_processed_chunks = []

    # Iterate through all files in the raw data bucket
    for blob in raw_bucket.list_blobs():
        # Get the text chunks from the document
        chunks = process_document(blob, RAW_DATA_BUCKET)

        # For each chunk, create a JSON object with content and metadata
        for chunk in chunks:
            # This step is critical for accurate citations later 
            chunk_json = {
                "content": chunk.page_content,
                "source": blob.name  # Metadata extraction [cite: 68]
            }
            all_processed_chunks.append(json.dumps(chunk_json))

    if not all_processed_chunks:
        print("No documents were processed. Exiting.")
        return

    # Combine all JSON strings into a single JSONL file content
    jsonl_content = "\n".join(all_processed_chunks)
    
    # Upload the processed JSONL file to the processed data bucket [cite: 73, 74]
    processed_bucket = storage_client.bucket(PROCESSED_DATA_BUCKET)
    output_blob_name = "processed_corpus.jsonl"
    output_blob = processed_bucket.blob(output_blob_name)
    
    print(f"\nUploading {len(all_processed_chunks)} chunks to gs://{PROCESSED_DATA_BUCKET}/{output_blob_name}")
    output_blob.upload_from_string(jsonl_content, content_type="application/jsonl")
    print("✅ Preprocessing and upload complete.")


if __name__ == "__main__":
    main()