# Web ChatGPT backend
> This demo is for applying ChatGPT API in practice

If you are not in an open net (where restriction of access network assets doesn't exist),
you should set up or find a working proxy address!

## How to Use
1. write a config.yml in the same format with `example.config.yml`
2. run migration work
    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```
3. run server
    ```python
    python manage.py runserver
    ```