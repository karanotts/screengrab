FROM python:3.7

RUN pip3 install pipenv

WORKDIR /screengrab

COPY Pipfile ./
COPY Pipfile.lock ./
COPY start.sh ./

RUN set -ex && pipenv install --deploy --system

COPY . .

RUN chmod +x ./start.sh
RUN ./start.sh

EXPOSE 5000
CMD [ "gunicorn", "-b0.0.0.0:5000", "wsgi:app" ]