## 🥰About

This is repository of "Face Similarity Judgement App"

https://face-similarity-judgement.streamlit.app/

## 🐋Docker

- docker is required

### Deploy server

```bash
# Please set the .env file before executing it.
docker compose up -d
```

### Build image

```bash
# Please change the username and tag correctly.
docker build -t uttechcenter/face-similarity-judgement:v1.0.0 .
```

## 🐍Conda

- conda or miniconda is required

### Create venv

```bash
conda create --name face_similarity_judgement python=3.11
```

### Activate venv

```bash
conda activate face_similarity_judgement
```

### Install libs

```bash
# Please activate venv before executing it.
pip install -r requirements.txt
```

### Deploy server

```bash
# Please activate venv before executing it.
streamlit run server.py
```
