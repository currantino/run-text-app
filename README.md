## Run text app
Приложение, которое генерирует видео бегущей строки с заданным текстом.
Сгенерированное видео сохраняется в Minio, чтобы для повторных запросов не нужно было генерировать новое.
Каждый запрос на сохранение видео сохраняется в Postgres, все запросы можно увидеть на странице `/requests`

![Run Text App demo](demo/demo.gif)

## Запуск
Перед запуском небходимо установить пароли для Postgres и Minio в соответствующих .env файлах. 
```bash
  docker compose up
```

