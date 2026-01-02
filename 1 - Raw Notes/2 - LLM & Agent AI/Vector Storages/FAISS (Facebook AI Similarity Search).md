Date: 2025-10-26
Course:
Tags: [[ML]] [[AI]] [[Vector Storages]] [[Database]] [[Local]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

## NOTE -> It's a local file
# Content

FAISS (Facebook AI Similarity Search) is an open-source library developed by Facebook AI Research for efficient similarity search and clustering of dense vectors. It is a crucial component in many applications requiring fast retrieval of similar items from large datasets, such as recommendation systems, image search, and natural language processing tasks like Retrieval-Augmented Generation (RAG) in Large Language Models (LLMs).

Key Features and Concepts:
- **Vector Similarity Search:** 
    FAISS's primary function is to find the nearest neighbors of a query vector within a large collection of high-dimensional vectors. This is essential for tasks where semantic similarity or proximity in a vector space is important.
    
- **Indexing Methods:** 
    FAISS offers a variety of indexing methods, each optimized for different trade-offs between speed, accuracy, and memory usage.
    - **IndexFlatL2:** A simple, exhaustive search that calculates the Euclidean distance (L2 norm) between the query and all indexed vectors, offering perfect accuracy but slower performance for large datasets.
    - **IndexIVFFlat:** An Inverted File Index (IVF) that clusters vectors during indexing, allowing for faster searches by only examining relevant clusters, at the cost of potential approximation.
    - **IndexPQ (Product Quantization):** Optimizes for memory usage and speed by compressing vectors, sacrificing some precision.
    - Other indices like IndexHNSWFlat, IndexLSH, and IndexScalarQuantizer also exist for specific use cases.

- **Scalability:** 
    FAISS is designed to handle extremely large datasets, including billions of vectors, by employing techniques like vector quantization and efficient memory management.

- **Flexibility:** 
    It provides a toolkit of primitives for searching, clustering, compressing, and transforming vectors, allowing for customization and optimization based on specific application needs.
    
- **Integration:** 
    FAISS can be integrated into various workflows, particularly with embedding models to create vector databases for semantic search and retrieval applications. Libraries like LangChain.js also support its use as a local vector store.


### Import from Langchain Community
```python
from langchain_community.vectorstores import FAISS
```

### Example
```python
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub


load_dotenv()


def load_pdf_to_faiss(file_path: str, faiss_index_folder_path: str):
    """load the local PDF file and create a FAISS vector store,
    then save it to a local path.

    Args:
        file_path (str): the pdf file path
        faiss_index_folder_path (str): the path to save the faiss index
    """
    # Load your PDF document
    loader = PyPDFLoader(file_path=file_path)
    doc_list = loader.load()

    txt_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50, separator="\n"
    )

    txt_list = txt_splitter.split_documents(documents=doc_list)
    print(f"Created {len(txt_list)} chunks from the document.")

    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small"
    )

    faiss_index = FAISS.from_documents(documents=txt_list, embedding=embeddings)

    faiss_index.save_local(faiss_index_folder_path)
    print(f"FAISS index saved to {faiss_index_folder_path}")


def retrieve_and_answer(faiss_index_folder_path: str, query: str):
    """Load the FAISS vector store from local path,
    retrieve relevant documents and answer the query.

    Args:
        faiss_index_folder_path (str): the path to load the faiss index
        query (str): the question to ask
    """

    faiss_index = FAISS.load_local(
        folder_path=faiss_index_folder_path,
        embeddings=OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small"
        ),
        allow_dangerous_deserialization=True,
    )

    retrieval_qa_chat_prompt = hub.pull(
        "langchain-ai/retrieval-qa-chat",
    )

    # Create a chain for passing a list of Documents to a model.
    combined_docs_chain = create_stuff_documents_chain(
        llm=ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0),
        prompt=retrieval_qa_chat_prompt,
    )

    retrieval_chain = create_retrieval_chain(
        retriever=faiss_index.as_retriever(),
        combine_docs_chain=combined_docs_chain,
    )

    result = retrieval_chain.invoke({"input": query})

    print(f"Questions: {result['input']}", sep="\n")
    print(f"Answer: {result['answer']}", sep="\n")
    print(f"Context: {result['context']}", sep="\n")


if __name__ == "__main__":
    print("Starting the ingestion...")
    faiss_index_folder_path = "./faiss_index"
    load_pdf_to_faiss(
        file_path="/Users/jinyuchen/Downloads/package.pdf",
        faiss_index_folder_path=faiss_index_folder_path,
    )
    print("Ingestion completed.")

    print("Starting the retrieval and answer...")
    retrieve_and_answer(
        faiss_index_folder_path=faiss_index_folder_path,
        query="When I can get the severance from Capital One?",
    )
    print("Retrieval and answer completed.")

```
# Note


# Reference

