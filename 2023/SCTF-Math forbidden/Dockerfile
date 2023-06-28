FROM python:3.7.17
COPY task /root
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y socat
RUN python -m pip install pycrypto -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 10000
CMD ["socat","tcp-l:10000,fork","exec:'python3 /root/task.py',reuseaddr"]