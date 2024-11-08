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

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Set environment variables for production
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_RUN_ON_SAVE=false
ENV STREAMLIT_THEME_BASE="light"
ENV STREAMLIT_DEVELOPMENT_MODE=false
ENV STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false
ENV STREAMLIT_SERVER_ENABLE_CORS=true
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true

# Run Streamlit in production mode
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.baseUrlPath=/", \
    "--server.enableCORS=true", \
    "--server.enableXsrfProtection=true", \
    "--server.maxUploadSize=50", \
    "--browser.serverAddress=0.0.0.0", \
    "--browser.gatherUsageStats=false", \
    "--global.developmentMode=false", \
    "--global.showWarningOnDirectExecution=true", \
    "--runner.postScriptGC=true", \
    "--client.showErrorDetails=false", \
    "--client.toolbarMode=minimal", \
    "--logger.level=error"]