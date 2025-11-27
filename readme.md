# 🚀 GCP Firestore + FastAPI Backend

A clean, modular backend application built with **FastAPI**, **Firebase Storage**, and **Google Cloud Firestore**.  
This project demonstrates file upload, file replacement, metadata updates, and retrieval using a scalable architecture powered by **Pydantic models** and a clean service–layer pattern.

---

## ✨ Features

- 📁 Upload files to **Firebase Storage**
- 🗄 Store metadata in **Firestore**
- 🔄 Replace files (delete old → upload new)
- ✏️ PATCH metadata with full dynamic support
- 🔍 Retrieve all files with Pydantic-powered responses
- 🧱 Modern, scalable architecture:
  - Routes
  - Services
  - Models
  - Config
  - API versioning (`v1`)
- ⏱ Bangladesh timezone for timestamps
- 🔒 Secure credentials (fully `.gitignore` protected)

---


---

## 🛠 Installation & Setup

### 1️⃣ Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate

```
### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt

```
### 3️⃣ Add Firebase credentials

Place your Firebase Admin SDK key file at:
```bash
serviceAccountKey.json
```
### ⚠️ This file is excluded from Git using 
```bash
.gitignore.
```

### ▶️ Running the Server

```bash
uvicorn app.main:app --reload --port 8010
```
### API will be live at:
```bash
http://localhost:8010
```

### 🔥 API Endpoints (v1)


### POST /files/
Uploads file → Stores metadata → Returns info.

### GET /files/
Fetches all Firestore documents and formats them using Pydantic.

### PUT /files/{file_id}
Deletes old file → Uploads new one → Updates metadata.

### PATCH /files/{file_id}
Supports dynamic partial updates.

### DELETE /files/{file_id}
Deletes metadata from Firestore.

### 🔒 Security Notes
Never commit 
```bash
serviceAccountKey.json
```
.gitignore protects secrets + environment files
Firestore rules should be configured safely when deployed
### 🤝 Contributing
Pull requests are welcome!
For large changes, open an issue first so we can discuss improvements.
### 🧑‍💻 Author
Pranto Bhowmik

Building FastAPI + Firebase + GCP microservices 🚀
### 📄 License
MIT License.
