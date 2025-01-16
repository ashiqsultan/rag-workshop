FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

EXPOSE 8888

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888", "--proxy-headers"] 