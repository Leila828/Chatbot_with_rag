FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt  \
    && rm -rf /root/.cache/pip \


COPY . .

COPY setup.py ./

ENV HUGGING_FACE_HUB_TOKEN=

CMD ["python", "chatbot.py"]

RUN python setup.py