FROM python
WORKDIR /app
COPY ./requirements.txt .
RUN apt-get update \
  && apt-get -y install tesseract-ocr
RUN apt-get install tesseract-ocr-spa -y
RUN pip install -r ./requirements.txt
COPY . .
EXPOSE 8000
