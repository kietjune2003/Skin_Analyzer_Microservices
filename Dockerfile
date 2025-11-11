
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxrender1 libxext6 ffmpeg \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV MICRO_HOST=0.0.0.0
ENV MICRO_PORT=5000
ENV MICRO_DEBUG=false
ENV PYTHONUNBUFFERED=1


EXPOSE 5000


CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5000", "--timeout", "300"]
