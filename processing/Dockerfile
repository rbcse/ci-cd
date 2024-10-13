FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install scikit-learn flask joblib
CMD ["python", "processing.py"]
