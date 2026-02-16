
FROM python:3.12.7

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

USER root

RUN apt-get update && apt-get install -y \
    && apt-get clean
USER user

COPY --chown=user . /app

# Render sets PORT; default 8000 for local runs
ENV PORT=8000
EXPOSE $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
