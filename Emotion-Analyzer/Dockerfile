FROM python
WORKDIR /emotion-analyzer
ADD . /emotion-analyzer
RUN pip install --upgrade pip
RUN pip install flask tensorflow numpy pandas matplotlib librosa scikit-learn
CMD ["python", "index.py"]