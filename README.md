# Internet consumption

Example of simple django project with API

## Installation

Install all dependency:
- django == 3.2.7
- djangorestframework == 3.12.4

```shell
$ pip install -r requirements.txt
```

## Run

```shell
$ python manage.py runserver 0.0.0.0:8000
```

### For Web

Open your browser and enter [http://0.0.0.0:8000/]()

### For API

```shell
$ curl "http://127.0.0.1:8000/api/"
```

All endpoint:
- `/api/`
- `/api/users/`
- `/api/consumption/`
- `/api/month-consumption/`

`/api/month-consumption/ `should contain body data or GET request parameters

Example:
```shell
# With GET request parameters
$ curl "http://127.0.0.1:8000/api/month-consumption/?name=John&date=2020-09-24"
```
```shell
# With body data
$ curl --header "Content-Type: application/json" \
       --request GET \
       --data '{"name": "Bob", "date": "2020-09-23"}' \
       http://127.0.0.1:8000/api/month-consumption/
```

## Testing

Install dev dependency

```shell
$ pip install -r requirements-dev.txt
```
And run

```shell
$ pytest
```

## License

This project is licensed under the terms of the MIT license.
