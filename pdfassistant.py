import fitz  # PyMuPDF for PDF processing
import openai
import faiss
import numpy as np
import tiktoken
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFAssistant:
    def __init__(self, openai_api_key):
        """Initialize with a PDF file and OpenAI API key."""
        #self.pdf_path = pdf_path
        self.openai_api_key = openai_api_key
        #self.text_chunks = self._extract_and_split_text()
        #self.index, self.embeddings = self._create_vector_store()
    def get_pdf_text(pdf_docs):
        """
        Extracts text from an uploaded PDF file.

        Args:
            pdf_docs (UploadedFile or list): A single uploaded PDF or a list of uploaded PDFs.

        Returns:
            str: Extracted text from the PDFs.
        """
        text = ""

        # Ensure pdf_docs is a list
        if not isinstance(pdf_docs, list):
            pdf_docs = [pdf_docs]

        for pdf_file in pdf_docs:
            try:
                # Read directly from UploadedFile object
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"  # Add newline for readability
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {e}")

        return text.strip()



    def get_text_chunks(text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text)
        return chunks

    """ def _extract_and_split_text(pdf_path, chunk_size=300):
        #Extract text from a PDF and split it into chunks.
        doc = fitz.open(pdf_path)
        text = " ".join([page.get_text("text") for page in doc])
        doc.close()

        # Tokenize and split text into smaller chunks
        encoder = tiktoken.get_encoding("cl100k_base")
        tokens = encoder.encode(text)

        chunks = [
            encoder.decode(tokens[i : i + chunk_size]) for i in range(0, len(tokens), chunk_size)
        ]
        return chunks """
    #self.text_chunks = get_text_chunks(text)
    #@staticmethod
    #def _embed_text(self, text_list):
    #    """Generate OpenAI embeddings for a list of texts."""
    #    openai.api_key = self.openai_api_key
    #    response = openai.embeddings.create(
    #        input=text_list,
    #        model="text-embedding-ada-002"
    #    )
        #embeddings = [entry["embedding"] for entry in response["data"]]
        #return np.array(embeddings, dtype=np.float32)
    #    return [data.embedding for data in response.data]

       
    @staticmethod
    def _embed_text(text_chunks):  # Remove 'self'
        """Generate embeddings for text chunks."""
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text_chunks
        )
        return [data.embedding for data in response.data]

    #@staticmethod
    def _create_vector_store(self, text_chunks):
        """Create a FAISS vector store with OpenAI embeddings."""
        #embeddings = self._embed_text(text_chunks)
        embeddings = PDFAssistant._embed_text(text_chunks)
        embeddings = np.array(embeddings, dtype=np.float32)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, embeddings

    def search(self, query, top_k=3):
        """Perform a semantic search on the vector database."""
        query_embedding = self._embed_text([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.text_chunks[i] for i in indices[0]]
        return results

# Example usage
#if __name__ == "__main__":
#    pdf_path = "sample.pdf"  # Replace with your actual PDF file
#    openai_api_key = "your-api-key-here"  # Replace with your OpenAI API key

#    assistant = PDFAssistant(pdf_path, openai_api_key)
    
#    query = "What is the main topic of the document?"
#    results = assistant.search(query)
    
#    print("\nTop matching chunks:")
#    for res in results:
#        print("-", res)
