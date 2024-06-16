## About

Face Similarity Judgement App

## Deploy

### 1. Create python environment
```sh
conda create --name python311_face_similarity_judgement python=3.11
conda activate python311_face_similarity_judgement
```

### 2. Install python library
```sh
pip install -r requirements.txt
```

### 3. Set Port

```toml:.streamlit/config.toml
[server]
port = 50013
```

### 4. Deploy

```sh
streamlit run server.py
```
