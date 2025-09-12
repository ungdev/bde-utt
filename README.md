```SQL
CREATE DATABASE bde CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bdeuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON bde.* TO 'bdeuser'@'localhost';
FLUSH PRIVILEGES;
```

docker run -p 8000:8000 --env-file .env --add-host=host.docker.internal:host-gateway bde-app:0.1