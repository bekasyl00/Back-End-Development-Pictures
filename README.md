# Pictures service

Flask REST microservice for the **Back-end Application Development Capstone Project**. It stores the supplied band's event-picture URLs and implements list, read, create, update and delete operations.

Based on the [official IBM starter](https://github.com/ibm-developer-skills-network/luggb-Back-End-Development-Pictures), commit `714d95ee32b59e104c37af9e5ecababde62a6efe`. The supplied tests, picture data, dependency declarations and Dockerfile are unchanged. Implementation and documentation were prepared with OpenAI Codex assistance; see [AI_ACKNOWLEDGEMENT.md](AI_ACKNOWLEDGEMENT.md).

## API

| Method | Route | Success response |
|---|---|---|
| GET | `/health` | 200, `{"status":"OK"}` |
| GET | `/count` | 200, `{"length":10}` for the initial dataset |
| GET | `/picture` | 200, JSON array of pictures |
| GET | `/picture/<id>` | 200, JSON picture |
| POST | `/picture` | 201, created picture and `Location` header |
| PUT | `/picture/<id>` | 200, updated picture |
| DELETE | `/picture/<id>` | 204, empty body |

A picture contains an integer `id` and the string fields `pic_url`, `event_country`, `event_state`, `event_city`, and `event_date`. POST and PUT accept a complete JSON resource. IDs must be nonnegative; PUT retains the ID in the URL. Invalid JSON, missing fields and mismatched IDs return JSON with status 400. Missing resources return `{"message":"picture not found"}` with status 404. Duplicate POST requests retain the lab's exact rule: status **302** with `{"Message":"picture with id <id> already present"}`.

The lab's POST example containing `/picture/<id>` conflicts with its overview, official starter and supplied tests; the implemented creation route is **POST `/picture`**.

## Setup and tests

The original Dockerfile targets Python 3.9.16. In an existing course lab, activate the provided Python environment and use the lab's dependency installation instructions. A minimal isolated environment for this in-memory service can also be created with a compatible Python:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --no-cache-dir Flask==2.1.2 Werkzeug==2.1.2 pytest==8.4.2
python -m pytest
```

The supplied suite contains **11 tests**. Its POST, duplicate, update and delete checks share application state, so run the complete suite in its supplied order. For the initial two endpoint checks:

```sh
python -m pytest -k 'test_health or test_count'
```

The broader original `requirements.txt` also contains database, quality and other course dependencies. The minimal command above installs the packages needed by this service and its supplied tests; it does not claim verification of that complete dependency set.

## Run

```sh
FLASK_APP=app python -m flask run --host=0.0.0.0 --port=5000
```

In a second terminal:

```sh
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/count
curl -i http://127.0.0.1:5000/picture/2
```

Using `FLASK_APP=app` is compatible with pinned Flask 2.1.2. The newer `--app` CLI flag shown in the lab requires a newer Flask release. The existing Dockerfile exposes port 3000; direct `python app.py` starts the starter's debug server on port 8080. Choose the matching URL for the selected launch command.

## Verification and limits

Verified locally on **22 October 2026** with Python **3.10.11**, Flask **2.1.2**, Werkzeug **2.1.2**, and pytest **8.4.2**, using a small dependency directory separate from this repository. The unchanged starter initially produced **2 passed, 9 failed**; the completed implementation produced **11 passed**. A separate real HTTP-server check exercised all seven routes, creation and duplicate handling, update/read-back, missing resources, malformed input, ID mismatch and the empty DELETE response. The server stopped after verification. These are local results; cloud deployment, GitHub publication and a course grade have not been verified by this check.

Pictures are loaded into a process-local list. Changes reset when the process restarts, and independent worker processes do not share changes. The existing `/count` handler's status 500 for an empty list is retained from the official starter. This is the course's in-memory exercise rather than a persistent database service.
