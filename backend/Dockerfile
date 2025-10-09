FROM python:3.13-slim

WORKDIR /srv/backend

# System deps for psycopg2-binary (less needed) and build essentials if needed later
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy only the app and requirements to keep image lighter
COPY app /srv/backend/app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]


