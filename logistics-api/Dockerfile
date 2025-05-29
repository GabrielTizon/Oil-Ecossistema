FROM php:8.0-cli

RUN apt-get update \
 && apt-get install -y librabbitmq-dev git unzip \
 && pecl install amqp \
 && docker-php-ext-enable amqp \
 && docker-php-ext-install sockets \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia o composer.json e instala o Composer + dependências PHP
COPY composer.json .
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
 && composer install --no-dev --optimize-autoloader

COPY index.php .

EXPOSE 8000
CMD ["php", "-S", "0.0.0.0:8000", "index.php"]
