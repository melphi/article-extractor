FROM python:3.6-slim

COPY app/ /opt/app
COPY extract_server.py /opt
COPY requirements.txt /opt

WORKDIR /opt
RUN apt-get update
RUN pip install -r requirements.txt

# In case of errors dowlonad https://github.com/aboSamoor/pycld2 and then
# install with python3 setup.py install
COPY lib/libstdc++.so.6 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
COPY lib/pycld2 /usr/local/lib/python3.6/site-packages/pycld2

RUN groupadd theuser
RUN useradd -g theuser theuser
RUN chown theuser.theuser -R /opt
USER theuser

ENTRYPOINT []
CMD ["python3", "extract_server.py"]

EXPOSE 8000
