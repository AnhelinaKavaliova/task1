FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src /app
COPY data /app/data
CMD ["python", "main.py", "/app/data/students.json", "/app/data/rooms.json", "--format", "json", "--output_name", "Result"]
