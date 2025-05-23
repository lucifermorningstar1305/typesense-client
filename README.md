# Typesense Client

A simple Streamlit-based client to browse and manage your Typesense search database.


# Features

- Connect to a remote or local Typesense server.
- List collections in the cluster.
- View and interact with documents in JSON format.
- Search within the collections with pagination.
- Delete or update documents directly from the UI.

# Prerequisites
- Python 3.8 or higher
- [Typesense](https://typesense.org/) server
- [UV Package Manager](https://docs.astral.sh/uv/) (for dependency and management)
- Docker & Docker Compose (optional, for containerized deployment)

# Installation

1. Clone the repository
    ```{bash}
    git clone https://github.com/lucifermorningstar1305/typesense-client.git
    ```

2. Install packages 
    ```{bash}
    uv sync --frozen
    ```

# Configuration
You can either enter your Typesense connection in the web form at runtime or set them via environment variables. To use a `.env` file copy and update the example.
```{bash}
cp .env.example .env
```
# Running Locally
```{bash}
uv run streamlit run app.py --server.port 8081
```
Open your browser to `http://localhost:8081` and fill in your Typesense details (if you haven't set the `.env` file)

# Docker Deployment
Build and run with Docker compose

```{bash}
docker compose up --build -d
```
Then just open your browser to `http://localhost:8081` and fill in your Typesense details (if you haven't set the `.env` file)


# Usage

1. Enter your Typesense server credentials in the form.
2. Select a collection from the dropdown.
3. Browse, search, delete, or update documents as needed.

# Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature_YOUR_FEATURE`).
3. Commit your changes (`git commit -m "Add YOUR FEATURE"`).
4. Push to the branch (`git push origin feature_YOUR_FEATURE`).
5. Open a Pull Request.

# License
This project is licensed under the MIT License. See [LICENSE](https://github.com/lucifermorningstar1305/typesense-client/blob/main/LICENSE) for details.

