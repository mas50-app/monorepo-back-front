FROM tiangolo/uvicorn-gunicorn:python3.9-alpine3.14

WORKDIR /app

COPY requirements.txt ./

RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

RUN apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font && fc-cache -f && fc-list | sort

RUN pip install -r requirements.txt

COPY . .

COPY ./temporales_desarrollo/imagenes /app/temporales_desarrollo/imagenes

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

