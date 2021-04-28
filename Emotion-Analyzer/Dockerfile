FROM python
WORKDIR /emotion-analyzer
ADD . /emotion-analyzer
RUN apt-get update -y
RUN apt-get install -y libsndfile-dev
RUN pip install --upgrade pip
RUN pip install flask tensorflow numpy pandas matplotlib librosa scikit-learn
CMD ["python", "index.py"]
