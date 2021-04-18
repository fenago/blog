FROM python
WORKDIR /me-bot
ADD . /me-bot
RUN pip install tensorflow flask tensorflow-hub numpy sentencepiece
CMD ["python", "index.py", "--host=0.0.0.0", "--port=80:", "--without-threads"]
