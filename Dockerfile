FROM python:3.10.14-alpine

WORKDIR /app
COPY requirements.txt .
RUN apk --no-cache add tzdata curl && \
      ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]