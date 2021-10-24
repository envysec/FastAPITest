# Pull official base iamge
FROM python:3.9.6-slim-buster

# Set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

# Install system dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Add app
COPY . .

# Add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
