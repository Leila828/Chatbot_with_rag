FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt  \
    && rm -rf /root/.cache/pip \


COPY . .

COPY setup.py ./

ENV HUGGING_FACE_HUB_TOKEN=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

CMD ["python", "chatbot.py"]

RUN python setup.py