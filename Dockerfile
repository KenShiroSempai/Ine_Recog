FROM python
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -٢ ./requirements.txt
COPY . .
EXPOSE 4999
