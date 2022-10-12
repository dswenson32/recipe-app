FROM python:3.7-slim-buster
WORKDIR /usr/src/app
RUN pip install pipenv
RUN pipenv install
RUN pip install -r requirements.txt
COPY . /usr/src/app
ENV FLASK_APP app.py
CMD [ "pipenv", "run", "gunicorn", "-w", "1", "-b", "127.0.0.1:5001", "app:app" ]

# docker run -p 5001:5001 -v ~/docker/docker_data/recipe_app_data:/recipes_data  recipe-app