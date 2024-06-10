# Dockerfile
FROM amazon/aws-sam-cli-build-image-python3.8
RUN pip install --upgrade pip && pip install -r requirements.txt
