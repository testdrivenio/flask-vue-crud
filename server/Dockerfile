FROM python:3.7-alpine
RUN apk --update add --no-cache \
    lapack-dev \
    python3-dev gcc \
    freetype-dev \
    jpeg-dev zlib-dev libjpeg \
    gfortran musl-dev \
    ffmpeg
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:80", "app:app", "--timeout 20000"]
