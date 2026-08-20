# 🤖 RAG-Based Company Report Question Answering System

## 📌 Project Overview

This project is an **AI-powered Retrieval-Augmented Generation (RAG) and Agentic AI system** that allows users to ask questions about company reports.

The system can intelligently decide how to handle a user's query. Depending on the question, it can:

* 🔍 Search company PDF reports
* 🧮 Perform mathematical calculations
* 💬 Provide direct answers to general questions

For document-related questions, the system retrieves relevant information from company PDF reports using a **Qdrant vector database** and generates an answer based on the retrieved context.

### Example

**Question:**

> What are the greenhouse gas reduction initiatives of JSW?

The system identifies the company, searches the relevant company report, retrieves relevant information, and generates an answer based on the available context.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────┐
                         │   User Query    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Agent Decision  │
                         │      Node       │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
      ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
      │ Search Company│   │   Calculator  │   │ Direct Answer │
      │   Documents   │   │     Tool      │   │     Node      │
      └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
              │                   │                   │
              ▼                   ▼                   ▼
      ┌───────────────┐            │                   │
      │ Relevant Docs │            │                   │
      └───────┬───────┘            │                   │
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Agent Generation│
                         │      Node       │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Final Answer   │
                         └─────────────────┘
```

---

# 🔄 RAG Pipeline Architecture

```text
PDF Reports
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
User Question
       │
       ▼
┌──────────────┐
│ Retriever    │
└──────┬───────┘
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
```

---

# ✨ Features

## 📄 RAG Features

* Load multiple company PDF reports.
* Split documents into smaller chunks.
* Generate embeddings for document chunks.
* Store embeddings in Qdrant Vector Database.
* Perform semantic similarity search.
* Retrieve relevant information based on user questions.
* Generate answers using Google FLAN-T5.
* Support multiple company reports.

## 🤖 Agent Features

The project also includes an agent workflow that decides how to process a user's request.

### 🔍 Document Search Tool

For questions related to company reports, the agent:

1. Detects the company.
2. Searches the relevant documents.
3. Retrieves relevant information.
4. Sends the context to the generation node.
5. Generates the final answer.

Example:

```text
Question:
What are the sustainability initiatives of JSW?

Agent selected:
search_documents
```

---

### 🧮 Calculator Tool

The agent can detect mathematical expressions and use a calculator tool.

Example:

```text
Question:
2500 * 45
```

Output:

```text
Agent selected: calculator

Calculator result: 112500
```

---

### 💬 Direct Answer Node

For general conversational questions that do not require document search or calculation, the agent provides a direct response.

Example:

```text
Question:
Hello, how are you?
```

Output:

```text
Agent selected: direct_answer
```

---

# 🛠️ Technologies Used

* Python
* LangChain
* LangGraph / Agent Workflow
* Qdrant
* Hugging Face Transformers
* Sentence Transformers
* Google FLAN-T5
* PyPDF
* PyTorch

---

# 📂 Project Structure

```text
Rag_Project_1/
│
├── data/
│   ├── jsw.pdf
│   └── godrej.pdf
│
├── agent.py
├── agent_app.py
├── agent_graph.py
├── agent_nodes.py
├── agent_state.py
│
├── app.py
├── document_loader.py
├── embeddings.py
├── retriever.py
├── text_splitter.py
├── vector_store.py
│
├── graph.py
├── nodes.py
├── state.py
├── tools.py
├── test_tool.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

> **Note:** The `qdrant_data/` folder is generated locally when the vector database is created and is excluded from Git using `.gitignore`.

---

# ⚙️ How the Project Works

## 1️⃣ Load Documents

Company PDF reports are loaded from the `data/` directory.

Example:

```text
data/
├── jsw.pdf
└── godrej.pdf
```

---

## 2️⃣ Split Documents into Chunks

The PDF content is divided into smaller chunks.

This improves retrieval because the system can search for relevant sections instead of processing an entire document at once.

---

## 3️⃣ Generate Embeddings

Each document chunk is converted into a numerical vector representation.

```text
Text
  ↓
Embedding Model
  ↓
Vector Representation
```

---

## 4️⃣ Store Vectors in Qdrant

The generated vectors are stored in the **Qdrant Vector Database**.

```text
Document Chunks
       ↓
   Embeddings
       ↓
Qdrant Vector Store
```

---

## 5️⃣ Agent Decision

When the user enters a query, the agent determines the appropriate action.

```text
User Query
    │
    ▼
Agent Decision Node
    │
    ├── Company Question ──► Search Documents
    │
    ├── Mathematical Query ─► Calculator Tool
    │
    └── General Question ───► Direct Answer
```

---

## 6️⃣ Search Company Documents

For document-related questions:

```text
User Question
       ↓
Company Detection
       ↓
Document Search
       ↓
Similarity Search
       ↓
Relevant Context
```

---

## 7️⃣ Generate the Final Answer

The retrieved context and user question are passed to the answer generation workflow.

```text
Relevant Context
       +
User Question
       ↓
FLAN-T5 / Generation Model
       ↓
Final Answer
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/vishnu-charitha/rag_project.git
```

## 2. Navigate to the Project

```bash
cd Rag_Project_1
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

## 4. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Step 1: Create the Vector Database

Run the ingestion or vector creation process:

```bash
python app.py
```

Depending on the project configuration, this process will:

* Load PDF documents.
* Split documents into chunks.
* Generate embeddings.
* Store vectors in Qdrant.

---

## Step 2: Run the RAG Application

```bash
python app.py
```

You can ask questions about the available company reports.

Example:

```text
What are the greenhouse gas reduction initiatives of JSW?
```

---

## Step 3: Run the Agent System

```bash
python agent_app.py
```

You will see:

```text
Ask a question (or type 'exit'):
```

### Document Search Example

```text
What are the sustainability initiatives of JSW?
```

The system may produce:

```text
--- AGENT DECISION NODE ---

Agent selected: search_documents

--- SEARCH DOCUMENTS TOOL ---

Company detected: JSW

--- AGENT GENERATION NODE ---

FINAL ANSWER:
...
```

### Calculator Example

```text
2500 * 45
```

Output:

```text
--- AGENT DECISION NODE ---

Agent selected: calculator

--- CALCULATOR TOOL ---

Expression: 2500 * 45

Calculator result: 112500
```

### Direct Answer Example

```text
Hello, how are you?
```

Output:

```text
--- AGENT DECISION NODE ---

Agent selected: direct_answer

--- DIRECT ANSWER NODE ---

FINAL ANSWER:
I'm fine.
```

To exit:

```text
exit
```

---

# 💬 Example RAG Question

### Question

```text
What technologies does JSW use to reduce greenhouse gas emissions?
```

### Retrieved Information

The system can retrieve information related to:

* Best Available Technologies (BAT)
* Energy and process efficiency
* Energy transition for decarbonisation
* Improving raw material quality
* Increasing scrap usage for material circularity

### Generated Answer

```text
JSW uses Best Available Technologies (BAT) to improve its climate performance.

Its greenhouse gas reduction roadmap also focuses on:

1. Energy and process efficiency.
2. Energy transition for decarbonisation.
3. Improving raw material quality.
4. Increasing scrap usage to promote material circularity.
```

---

# 🔀 Agent Workflow Example

```text
                USER QUERY
                     │
                     ▼
             ┌───────────────┐
             │ Agent Decision│
             └───────┬───────┘
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
 Search Documents  Calculator   Direct Answer
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
             Agent Generation
                     │
                     ▼
               FINAL ANSWER
```

---

# ⚠️ Known Notes

## Hugging Face Token Warning

You may see a warning similar to:

```text
Warning: You are sending unauthenticated requests to the Hugging Face Hub.
```

The project can still work without a Hugging Face token. Authentication may provide higher rate limits and faster model downloads.

## Model Warning

You may also see warnings related to model configuration, such as:

```text
tie_word_embeddings
```

These warnings do not necessarily prevent the application from running.

---

# 🎯 Future Improvements

* [ ] Add a Streamlit web interface.
* [ ] Add more company reports.
* [ ] Add source citations to generated answers.
* [ ] Improve answer formatting.
* [ ] Add chat history and memory.
* [ ] Implement metadata filtering.
* [ ] Add more agent tools.
* [ ] Integrate external APIs.
* [ ] Use a more powerful LLM.
* [ ] Add tool calling with dynamic agent decisions.
* [ ] Deploy the application.

---

# 👩‍💻 Author

**N. Vishnu Charitha**

* GitHub: https://github.com/vishnu-charitha
* LinkedIn: https://www.linkedin.com/in/vishnu-charitha-60b3b5294/

---

# 📄 License

This project is created for **learning and educational purposes**.

---

⭐ If you found this project useful, consider giving the repository a star!
