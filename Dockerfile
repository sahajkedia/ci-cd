FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_BASE_URL_PATH=/
ENV STREAMLIT_BROWSER_SERVER_ADDRESS=localhost
ENV STREAMLIT_BROWSER_SERVER_PORT=80
ENV STREAMLIT_SERVER_ENABLE_CORS=true
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_THEME_BASE="light"
ENV STREAMLIT_CLIENT_TOOLBAR_MODE=minimal


# Run Streamlit in production mode
CMD ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.baseUrlPath=/", \
    "--server.enableCORS=true", \
    "--server.enableXsrfProtection=true", \
    "--server.maxUploadSize=50", \
    "--server.enableWebsocketCompression=true", \
    "--browser.serverAddress=localhost", \
    "--browser.serverPort=80", \
    "--browser.gatherUsageStats=false", \
    "--client.showErrorDetails=false", \
    "--client.toolbarMode=minimal", \
    "--logger.level=info"]