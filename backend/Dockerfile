FROM python:3.13-slim

WORKDIR /srv/backend

# System deps for psycopg2-binary (less needed) and build essentials if needed later
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy app and tests
COPY app /srv/backend/app
COPY tests /srv/backend/tests

# Set environment variables
ENV PYTHONPATH=/srv/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


