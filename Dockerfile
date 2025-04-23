FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install build tools and a safe numpy version first
RUN pip install --upgrade pip setuptools wheel \
    && pip install numpy==1.24.4

# Pin spaCy to a compatible version
RUN pip install spacy==3.7.4 \
    && python -m spacy download en

# Then install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
