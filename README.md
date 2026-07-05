# 🤖 RAG Chatbot Pro

A professional **Retrieval-Augmented Generation (RAG) Chatbot** built with **Streamlit**, **Google Gemini AI**, **FAISS**, and **Sentence Transformers**.

The chatbot allows users to upload multiple documents, retrieve relevant information using vector search, and generate intelligent answers using Gemini AI.

---

## 📸 Demo

![RAG Chatbot](https://img.shields.io/badge/Streamlit-Live-red?logo=streamlit)

> Live Demo: *(Add your Streamlit URL here after deployment)*

---

## 🚀 Features

- 📄 Multi-document upload
  - PDF
  - DOCX
  - TXT
  - CSV
  - Excel

- 🤖 Gemini AI integration

- 🔍 FAISS Vector Search

- 🧠 Sentence Transformer Embeddings

- 💬 ChatGPT-style Interface

- 📚 Conversation Memory

- 📥 Export Chat
  - TXT
  - Markdown
  - PDF

- 📊 Analytics Dashboard

- ⚡ Fast Retrieval-Augmented Generation (RAG)

- 🌐 Streamlit Cloud Deployment

---

# 🏗 Project Architecture

```
                +----------------------+
                |   Upload Documents   |
                +----------+-----------+
                           |
                           |
                           ▼
                  Text Extraction
                           |
                           ▼
                    Text Chunking
                           |
                           ▼
          Sentence Transformer Embeddings
                           |
                           ▼
                  FAISS Vector Database
                           |
                           ▼
                    Similarity Search
                           |
                           ▼
                 Relevant Context Retrieved
                           |
                           ▼
                 Google Gemini AI Model
                           |
                           ▼
                  Intelligent Response
```

---

# 📂 Project Structure

```
RAG-Chatbot-Pro
│
├── app.py
├── rag.py
├── utils.py
├── analytics.py
├── export.py
├── speech.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/SivaPrasad110/RAG-Chatbot-Pro.git

cd RAG-Chatbot-Pro
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Key

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Get your API key from

https://aistudio.google.com/

---

# ▶ Run the Application

```bash
streamlit run app.py
```

Application will start at

```
http://localhost:8501
```

---

# 📚 Supported File Types

| Format | Supported |
|---------|-----------|
| PDF | ✅ |
| DOCX | ✅ |
| TXT | ✅ |
| CSV | ✅ |
| Excel | ✅ |

---

# 🧠 Technologies Used

- Python
- Streamlit
- Google Gemini AI
- FAISS
- Sentence Transformers
- NumPy
- Pandas
- PyPDF
- python-docx
- OpenPyXL
- ReportLab

---

# 📈 Workflow

1. Upload one or more documents
2. Extract text
3. Split into chunks
4. Generate embeddings
5. Store in FAISS
6. Search relevant chunks
7. Send context to Gemini
8. Display answer

---

# 📷 Screenshots

### Home Page

(Add Screenshot)

---

### Chat Interface

(Add Screenshot)

---

### Document Upload

(Add Screenshot)

---

# 🌐 Deployment

The application can be deployed on

- Streamlit Community Cloud
- Docker
- Render
- Railway
- Azure App Service
- AWS EC2

---

# 🛠 Future Improvements

- User Authentication
- Database Storage
- Persistent FAISS Index
- OCR Support
- Website URL Chat
- Image Understanding
- Streaming Responses
- Multi-language Support
- Chat History Database

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```
git checkout -b feature-name
```

3. Commit changes

```
git commit -m "Added new feature"
```

4. Push

```
git push origin feature-name
```

5. Open a Pull Request

---

# 👨‍💻 Author

**Siva Prasad**

GitHub:

https://github.com/SivaPrasad110

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

# 📜 License

This project is licensed under the MIT License.
