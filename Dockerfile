FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

RUN apk add --no-cache rclone

COPY . .

RUN uv sync

CMD ["uv", "run", "main.py"]