FROM python:3.8-slim
RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /dsa
RUN pip install dsa-downloader
USER app_user
CMD ["dsa-downloader"]