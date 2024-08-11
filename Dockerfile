FROM python:3.12
WORKDIR /app
COPY src/ /app/src/
COPY data/ /app/data/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "/app/src/main.py", "/app/data/students.json", "/app/data/rooms.json", "--format", "json", "--output_name", "output"]
