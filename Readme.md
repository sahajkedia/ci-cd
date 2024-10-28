# To run the file

```
source venv/bin/activate
```

# Run all linting checks

```
flake8 .
black . --check
isort . --check
```

# To actually format the code (not just check):

black .
isort .

# Run the streamlit app

```
streamlit run app.py
```


## **Build and run with Docker Compose**

```
docker-compose** up --build
```

## **Or build and run separately**

```
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
```
