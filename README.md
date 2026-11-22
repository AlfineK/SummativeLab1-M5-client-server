
# Retail Inventory Management System

A full-stack retail inventory application built with a **Flask** REST API, a **CLI admin tool**, and a **React** frontend, integrated with **OpenFoodFacts** and a local mock array fallback.

---

## Project Structure

```text
retail_inventory_system/
├── README.md
├── server/
│   ├── requirements.txt
│   ├── product.py
│   ├── mock_db.py
│   ├── app.py
│   ├── cli.py
└── frontend/
    ├── package.json
    └── src/
        ├── App.css
        └── App.jsx
```

## File Overview

server/product.py — Product model and to_dict() JSON serializer.

server/mock_db.py — Mock OpenFoodFacts array, search helper, and starter inventory data.

server/app.py — Flask server on <http://127.0.0.1:5555> with CRUD routes and OpenFoodFacts lookup.

server/cli.py — Terminal menu for managing inventory and searching external products.

frontend/src/App.jsx — React dashboard for viewing, adding, editing, deleting, and looking up items.

frontend/src/App.css — Stylesheet for the React dashboard.

## Prerequisites

Python 3.10+ and pip

Node.js 18+ and npm

## Getting Started

1. Start the Flask Server

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate   
pip install -r requirements.txt
python app.py
```

The API runs at <http://127.0.0.1:5555> Keep this terminal running

2.Run the CLI Tool

Open a second terminal:

```bash
cd server
source .venv/bin/activate   
python cli.py
```

3.Run the React Frontend

Open a third terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL shown in the terminal (usually <http://localhost:5173>) in your browser
