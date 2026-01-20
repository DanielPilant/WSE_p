# Supermarket Agent Client

This is the client-side desktop application for the Supermarket Agent project. It is built using Python and **PySide6** (Qt for Python).

## Table of Contents

- [Project Architecture](#project-architecture)
- [Folder Structure](#folder-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Backend Integration](#backend-integration)

## Project Architecture

The application follows a modular architecture designed for scalability and maintainability:

1.  **Micro-Frontend (MFE) inspired Components**: The UI is composed of self-contained modules located in `ui/components/`. Each component (e.g., `cart_mfe`, `chat_mfe`) follows the **Model-View-Presenter (MVP)** pattern:

    - **Model**: Manages state specific to the component.
    - **View**: Handles the visual elements (Qt Widgets).
    - **Presenter**: Contains business logic and acts as the middleman between the View and the Data/Application layers.

2.  **Core Application Logic**:

    - `AppController` (`core/app_controller.py`): The main window and "orchestrator" that wires different components together. It handles the flow of data between the Chat component and the Cart component.
    - `UI Worker` (`core/workers.py`): Uses `QThread` to perform long-running tasks (like fetching data) in the background, ensuring the UI remains responsive.

3.  **Data Layer**:
    - `Repository Pattern` (`data/repositories/`): Abstract the data source. The Application Controller talks to the Repository, not directly to an API or Database.

## Folder Structure

```
client/
├── core/                   # Core logic
│   ├── app_controller.py   # Main Controller (Orchestrator)
│   └── workers.py          # Background threads
├── data/                   # Data access layer
│   └── repositories/       # Repositories (Data Abstraction)
├── models/                 # Data Class definitions (DTOs)
├── ui/                     # User Interface
│   ├── components/         # Independent UI Modules (MFE)
│   ├── dialogs/            # Modal dialogs
│   └── styles/             # Global styling (QSS, Themes)
└── main.py                 # Application Entry Point
```

## Installation & Setup

1.  **Prerequisites**: Ensure you have Python 3.10+ installed.
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```
3.  **Activate the Virtual Environment**:
    - Windows: `venv\Scripts\activate`
    - macOS/Linux: `source venv/bin/activate`
4.  **Install Dependencies**:
    ```bash
    pip install PySide6
    ```

## Running the Application

To start the application, run the `main.py` file from the `client` directory:

```bash
python main.py
```

## Backend Integration

Currently, the application runs in a **mocked mode**. The interaction with the "backend" is simulated in `client/data/repositories/supermarket_repo.py`.

### How the Backend Should Interact

The frontend expects an API that accepts natural language queries and returns structured data. The interaction contract is defined by the data classes in `client/models/types.py`.

To connect a real backend:

1.  **API Endpoint**: The backend should expose an endpoint (e.g., `POST /api/search`) that accepts a JSON payload with the user's prompt.

    ```json
    {
      "user_id": "uuid-...",
      "prompt": "I need milk and bread"
    }
    ```

2.  **Response Format**: The backend must return a JSON response that indicates either a **success** (found products) or a **request for clarification** (ambiguity).

    **Scenario A: Success (Map to `StoreResult`)**

    ```json
    {
      "type": "result",
      "data": {
        "store_name": "Supermarket Name",
        "address": "123 Street Name",
        "total_price": 50.0,
        "items": [
          { "id": "1", "name": "Milk", "quantity": 1, "price": 10.0 },
          { "id": "2", "name": "Bread", "quantity": 2, "price": 20.0 }
        ]
      }
    }
    ```

    **Scenario B: Ambiguity (Map to `ClarificationRequest`)**

    ```json
    {
      "type": "clarification",
      "data": {
        "question": "Which type of bread do you prefer?",
        "options": ["Whole Wheat", "White", "Sourdough"]
      }
    }
    ```

3.  **Client Implementation**:
    Update `SupermarketRepository.send_prompt_to_ai` in `client/data/repositories/supermarket_repo.py` to replace the mock logic with a real HTTP request (using libraries like `requests` or `httpx`).

    ```python
    # Example Implementation Concept
    def send_prompt_to_ai(self, user_text: str):
        response = requests.post("http://localhost:8000/api/search", json={"prompt": user_text})
        data = response.json()

        if data["type"] == "result":
            return StoreResult(**data["data"])
        elif data["type"] == "clarification":
            return ClarificationRequest(**data["data"])
    ```
