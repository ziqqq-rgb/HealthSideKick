# 1. Use a lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements file first (this makes future builds faster)
COPY requirements.txt .

# 4. Install all your Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your backend code into the container
COPY . .

# 6. Expose the port FastAPI uses
EXPOSE 8000

# 7. The command to start your server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]