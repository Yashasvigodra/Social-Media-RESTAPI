#base image
FROM python:3.9.7

#working directory
WORKDIR /user/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app" , "--host" , "0.0.0.0" , "--port" , "8000"]

