# Elice Community API Server
Elice **Backend Interview 용으로 개발된** 커뮤니티 API 서버입니다


## Requirements
- Python 3.11
- Docker & Docker Compose
- (Optional) Postgresql **version**
- (Optional) Redis **version**

## Conventions

### Active Branches
- `prod`: 사용하지 않습니다
- `dev` (default): 개발용 브랜치입니다, EC2에 배포됩니다 (예정)
- `feature/{description}`: 새로운 기능이 추가되는 경우에 사용
- `refactor/{description}`: 기능 변경 없이 코드 리팩토링만을 하는 경우에 사용
- `fix/{description}`: `dev` 브랜치로 반영하는 사소한 오류 수정 시에 사용
- `hotfix/{description}`: `prod` 브랜치로 반영하는 긴급한 오류 수정 시에 사용

### PR Merge Rules
  - default: *Squash and merge*
  - `dev` to `prod`: *Create a merge commit*


## Dev Guidelines

### Python Dependencies
가상환경을 활성화하고 필요한 패키지를 설치합니다.
```shell
poetry shell
poetry install
```
`pyproject.toml` 파일의 패키지 목록을 변경한 경우, 아래 명령을 통해 `poetry.lock` 파일을 최신화합니다.
```shell
poetry lock
```

### Server Startup
Docker Compose를 활용하여 MySQL, Redis 및 FastAPI 서버를 실행합니다.
```shell
docker compose up
```


## Test
Pytest를 이용하여 테스트를 진행합니다.
```shell
make test
```

## Deployment
`dev`, `prod` 브랜치에 새로운 push가 일어날 때마다 [GitHub Actions](.github/workflows)를 활용한 ECR 이미지 업로드 및 ArgoCD를 활용한 배포가 진행됩니다.

---
# API Documentation
## User
### User Signup
- **URL**: `/api/users/signup`
- **Method**: `POST`
- **Request**
  - **Body**
    - `email`: `string`
    - `password`: `string`
    - `fullname`: `string`
  - **Example**
    ```json
    {
      "email": "",
      "password": "1234",
      "fullname": "elice kang"
    }
    ```
- **Response**
    - **Body**
        - `id`: `int`
        - `email`: `string`
        - `fullname`: `string`
    - **Example**
        ```json
        {
        "id": 1,
        "email": "",
        "fullname": "elice kang"
        }
        ```
### User Login
- **URL**: `/api/users/login`
- **Method**: `POST`
- **Request**
  - **Body**
    - `email`: `string`
    - `password`: `string`
  - **Example**
    ```json
    {
      "email": "",
      "password": "1234"
    }
    ```
- **Response**
- **Body**
    - `access_token`: `string`
    - **Example**
        ```json
        {
          "access_token": ""
        }
        ```
### User Logout
- **URL**: `/api/users/logout`
- **Method**: `POST`

## Board
### Board List
- **URL**: `/api/v1/boards`
- **Method**: `GET`
- **Request**
  - **Query**
    - `page`: `int`
    - `limit`: `int`
  - **Example**
    ```json
    {
      "page": 1,
      "limit": 10
    }
    ```
- **Response**
- **Body**
    - `count`: `int`
    - `next`: `string`
    - `previous`: `string`
    - `results`: `array`
        - `id`: `int`
        - `title`: `string`
        - `content`: `string`
        - `author`: `object`
            - `id`: `int`
            - `email`: `string`
            - `nickname`: `string`
            - `created_at`: `string`
            - `updated_at`: `string`
            - `deleted_at`: `string`
            - `is_active`: `boolean`
        - `created_at`: `string`
        - `updated_at`: `string`
        - `deleted_at`: `string`
        - `is_active`: `boolean`
    - **Example**
        ```json
        {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
            "id": 1,
            "title": "title",
            "content": "content",
            "author": {
                "id": 1,
                "email": "",
                "nickname": "elice",
                "created_at": "2021-10-18T14:00:00",
                "updated_at": "2021-10-18T14:00:00",
                "deleted_at": null,
                "is_active": true
            },
            "created_at": "2021-10-18T14:00:00",
            "updated_at": "2021-10-18T14:00:00",
            "deleted_at": null,
            "is_active": true
            }
        ]
        }
        ```
### Board Create
- **URL**: `/api/v1/boards`
- **Method**: `POST`
- **Request**
  - **Body**
    - `title`: `string`
    - `content`: `string`
  - **Example**
    ```json
    {
      "title": "title",
      "content": "content"
    }
    ```