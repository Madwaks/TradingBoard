FROM python:3.7.4-slim-stretch

RUN apt-get update && apt-get install -y gettext build-essential git wget
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add - \
 && echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" >> /etc/apt/sources.list.d/pgdg.list \
 && apt-get update && apt-get install -y postgresql-client-11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -U pip setuptools \
 && pip install --no-cache-dir -r requirements.txt

COPY src/. /app/.
COPY scripts/run_trade_fox.sh /app/.

RUN chmod +x /app/run_trade_fox.sh

EXPOSE 80

ENTRYPOINT ["/app/run_trade_fox.sh"]
CMD ["runserver"]
