FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml README.md ./
COPY src ./src
COPY knowledge ./knowledge
RUN pip install --no-cache-dir --upgrade "setuptools>=83" pip &&     pip install --no-cache-dir . &&     useradd --create-home --uid 10001 sentinelops
USER 10001
EXPOSE 8000
CMD ["uvicorn", "sentinelops.api:app", "--host", "0.0.0.0", "--port", "8000"]
