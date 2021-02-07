FROM python:3.6.5-alpine

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev

WORKDIR /course-recommender-app
ADD . /course-recommender-app
RUN pip install --upgrade pip
RUN pip install flask pandas numpy
CMD ["python", "index.py"]
