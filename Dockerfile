FROM python:3.7-slim-buster
WORKDIR /usr/src/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
CMD ["flask", "run"]

# docker run -p 5001:5001 -v ~/docker/docker_data/recipe_app_data:/recipes  recipe-app