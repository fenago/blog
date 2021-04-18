FROM python
WORKDIR /me-bot
ADD . /me-bot
RUN pip install --upgrade pip
RUN pip install flask tensorflow tensorflow-hub numpy sentencepiece
CMD ["python", "index.py"]