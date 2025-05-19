FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt pyproject.toml /app/

ENV PATH="/app/.venv/bin:$PATH"

RUN pip install -r requirements.txt

COPY ./ /app/

RUN pip install -e .

EXPOSE 3000

CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]
