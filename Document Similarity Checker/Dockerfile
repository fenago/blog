FROM python:3.6.5-alpine
WORKDIR /document-similarity-checker
ADD . /document-similarity-checker
RUN pip install --upgrade pip
RUN pip install flask scikit-learn nltk
CMD ["python", "ui.py"]