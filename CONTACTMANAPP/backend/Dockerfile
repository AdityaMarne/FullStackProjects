#Use an official Python runtime as base
FROM python:3.10

#Set working directory
WORKDIR /app

#Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Expose the Flask port
EXPOSE 5000

#Run the app
CMD ["python", "app.py"]
