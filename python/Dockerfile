FROM python:3.6-alpine

COPY app/ /opt/app
COPY extract_server.py /opt

WORKDIR /opt
RUN pip install -r requirements.txt
ADD lib/pycld2.zip /opt/

ENTRYPOINT []
CMD ["python3", "extract_server.py"]

EXPOSE 8000
