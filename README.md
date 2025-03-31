# ai Image Generation

```
python -m venv venv
```

```
venv\Scripts\activate
```

# Running the api
uvicorn app:app --host 0.0.0.0 --port 8000

# Posting to the api
curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d "{\"text\": \"a studio ghibli orange cat\"}" --output output.png
