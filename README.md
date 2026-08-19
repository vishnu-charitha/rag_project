📌 Project Overview

This project is a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about company reports.

The system retrieves relevant information from company PDF reports using a vector database and generates an answer based only on the retrieved context.

For example:

Question:
What are the greenhouse gas reduction initiatives of JSW?

The system searches the company reports and retrieves the relevant content before generating an answer.

🏗️ RAG Architecture
                 ┌──────────────┐
                 │  PDF Reports │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Document     │
                 │ Loading      │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Text         │
                 │ Chunking     │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Embeddings   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Qdrant       │
                 │ Vector Store │
                 └──────┬───────┘
                        │
                        ▼
User Question ───► Retriever
                        │
                        ▼
                 Relevant Context
                        │
                        ▼
                 ┌──────────────┐
                 │ FLAN-T5 LLM  │
                 └──────┬───────┘
                        │
                        ▼
                   Final Answer
✨ Features
Load company PDF reports.
Split documents into smaller chunks.
Generate embeddings for document chunks.
Store embeddings in Qdrant Vector Database.
Perform semantic similarity search.
Retrieve relevant information based on user questions.
Generate answers using Google FLAN-T5.
Interactive command-line question answering.
Supports multiple company reports.
🛠️ Technologies Used
Python
LangChain
Qdrant
Hugging Face Transformers
Sentence Transformers
Google FLAN-T5
PyPDF
PyTorch
📂 Project Structure
Rag_Project_1/
│
├── data/
│   ├── jsw.pdf
│   └── godrej.pdf
│
├── qdrant_data/
│   └── company_reports
│
├── embeddings.py
├── ingest.py
├── retriever.py
├── rag_pipeline.py
├── requirements.txt
└── README.md
⚙️ How the Project Works
1. Load Documents

The company PDF reports are loaded from the data/ folder.

Example:

data/
├── jsw.pdf
└── godrej.pdf
2. Split Documents into Chunks

The PDF content is divided into smaller chunks so that relevant information can be efficiently retrieved.

3. Generate Embeddings

Each document chunk is converted into numerical vector representations using an embedding model.

Text → Embedding Model → Vector
4. Store Vectors in Qdrant

The generated vectors are stored locally in the Qdrant vector database.

qdrant_data/
5. Retrieve Relevant Documents

When the user asks a question, the question is converted into an embedding.

Qdrant then performs a similarity search to find the most relevant document chunks.

User Question
      ↓
Embedding
      ↓
Qdrant Similarity Search
      ↓
Relevant Documents
6. Generate Final Answer

The retrieved context and user question are passed to the FLAN-T5 model.

The model generates an answer based on the retrieved information.

🚀 Installation
1. Clone the Repository
git clone https://github.com/vishnu-charitha/your-repository-name.git
2. Navigate to the Project
cd Rag_Project_1
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment

Windows:

venv\Scripts\activate
5. Install Dependencies
pip install -r requirements.txt
📦 Required Libraries

Example requirements.txt:

langchain
langchain-community
langchain-qdrant
qdrant-client
sentence-transformers
transformers
torch
pypdf
▶️ Running the Project
Step 1: Create the Vector Database

Run the ingestion script:

python ingest.py

This will:

Load PDF documents.
Split them into chunks.
Generate embeddings.
Store the vectors in Qdrant.
Step 2: Test Document Retrieval

Run:

python retriever.py

Example output:

--- RESULT 1 ---


Source: data/jsw.pdf
Page: 31


Content:
JSW Steel has set an ambitious CO₂ emission reduction target...
Step 3: Run the RAG Pipeline

Run:

python rag_pipeline.py

You will see:

Ask a question (or type 'exit'):

Ask a question such as:

What are the greenhouse gas reduction initiatives of JSW?
💬 Example
User Question
What technologies does JSW use to reduce greenhouse gas emissions?
Retrieved Context

The system retrieves information from the JSW Steel Integrated Report, including:

Best Available Technologies (BAT)
Energy and process efficiency
Energy transition for decarbonisation
Improving raw material quality
Increasing the use of scrap for material circularity
Generated Answer
JSW uses Best Available Technologies (BAT) to improve its climate performance.


Its greenhouse gas reduction roadmap also focuses on:


1. Energy and process efficiency.
2. Energy transition for decarbonisation.
3. Improving raw material quality.
4. Increasing scrap usage to promote material circularity.
🔄 RAG Pipeline Flow
PDF Documents
     ↓
Document Loader
     ↓
Text Splitter
     ↓
Embedding Model
     ↓
Qdrant Vector Database
     ↓
User Question
     ↓
Similarity Search
     ↓
Relevant Context
     ↓
FLAN-T5 Model
     ↓
Final Answer
⚠️ Known Notes
Hugging Face Token Warning

You may see:

Warning: You are sending unauthenticated requests to the HF Hub.

The project can still work without a Hugging Face token. However, authentication may provide higher rate limits and faster downloads.

Model Warning

You may also see a warning related to:

tie_word_embeddings

This is a model configuration warning and does not necessarily prevent the RAG system from running.

🎯 Future Improvements
Add a Streamlit web interface.
Support more PDF documents.
Add source citations to generated answers.
Improve answer formatting.
Add chat history.
Implement metadata filtering.
Use a more powerful LLM.
Deploy the application.
👩‍💻 Author

N. Vishnu Charitha

GitHub: vishnu-charitha
LinkedIn: N. Vishnu Charitha
📄 License

This project is created for learning and educational purposes.
