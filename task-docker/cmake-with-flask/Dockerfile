FROM python:3.11-slim

WORKDIR /

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask

COPY . /

RUN mv /print_hello.sh /bin/print_hello && chmod +x /bin/print_hello

RUN mkdir build && cd build && cmake .. && make

RUN useradd -m devops2024user

USER devops2024user

EXPOSE 8898

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "8898"]