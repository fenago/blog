FROM python:3.7

WORKDIR /sentiment-analysis
ADD . /sentiment-analysis
RUN pip install --upgrade pip
RUN pip install flask pandas numpy scikit-learn
CMD ["python", "ui.py"]