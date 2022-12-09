# python_fastapi_docker

# Run without Docker
Navigate to folder python_fastapi_docker
Run Command:
1. py -m pip install --upgrade pip
2. py -m pip install --user virtualenv
3. py -m venv venv
4. .\venv\Scripts\activate
5. cd fastapi_service
6. pip install -r requirements.txt
7. uvicorn app.main:app --reload
8. Gooto: http://127.0.0.1:8000/docs

# Run with Docker (assuming you already have Docker running on desktop)
Navigate to folder python_fastapi_docker
Run Commands
1. docker-compose up -d
2. Goto: localhost:8001/docs

# All Endpoints:
![endpoints](https://user-images.githubusercontent.com/8905320/206754795-313b3514-8f18-4323-9c2d-e86216c17740.png)
