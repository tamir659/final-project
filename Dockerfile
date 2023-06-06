FROM python:3.10-slim 

WORKDIR /restaurant-app 

RUN pip install Flask flask_wtf wtforms wtforms.validators flask_sqlalchemy datetime email_validator psycopg2-binary 

COPY . . 

CMD python server.py  

 