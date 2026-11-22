# assistant_core_lab

Study Assistant for the CSC10014 course project (FIT, University of Science, VNU-HCM).
Pipeline: UI -> API -> data / retrieval / AI / tools -> response.

## Setup
```
python -m venv .venv
.venv\\Scripts\\activate          # Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
pip install -e .
copy .env.example .env             # Git Bash: cp .env.example .env
```

## Run the MVP (two terminals, both from the project root, venv activated)
Terminal 1 - the backend API (http://127.0.0.1:8000, docs at /docs):
```
uvicorn assistant_api.main:create_app --factory
```
Terminal 2 - the web UI (http://localhost:8501):
```
streamlit run ui/app.py
```
The UI talks to the backend only through HTTP. If the API is on another address, set `ASSISTANT_API_URL` before `streamlit run`.

## Run the tests
```
pytest -q
cd practice && pytest -q test_hello_streamlit.py
```

## Chat API (v1)
`POST /v1/chat` with `{"message": "...", "session_id": "..."}` returns
`{answer, intent, sources[], degraded, escalate, path, confidence, request_id}`.
`escalate: true` means the assistant does not know and the UI shows who can help (Training Office).
Errors: 422 invalid input, 429 too many requests.

## Lab 7 files
- `ui/app.py`, `ui/logic.py`, `ui/api_client.py` - Streamlit chat page (L1 sources, L2 status notes, F1 thumbs-down)
- `practice/hello_streamlit.py` - Streamlit warm-up U1-U4
- `worksheets/usability_checklist.md`, `worksheets/user_test_observations.md` - usability work
