FROM python
WORKDIR /app
COPY ./requirements.txt .
RUN apt-get update \
  && apt-get -y install tesseract-ocr
RUN pip install -r ./requirements.txt
COPY . .
EXPOSE 8000
