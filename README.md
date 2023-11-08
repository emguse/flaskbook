# flaskbook

Based on the content of [this book](https://www.shoeisha.co.jp/book/detail/9784798166469)

- You need to create an `.env` file.
```.env
FLASK_APP=apps.app:create_app("local")
FLASK_ENV=deveropment
FLASK_DEBUG=1
FLASK_RUN_HOST='0.0.0.0'
FLASK_RUN_PORT={PORT}
FLASK_SECRET_KEY = {SECRET_KEY}
FLASK_WTF_CSRF_SECRET_KEY = {SECRET_KEY}
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = {USERNAME}@gmail.com
MAIL_PASSWORD = {PASSWORD}
MAIL_DEFAULT_SENDER = Flaskbook {USERNAME}@gmail.com
```