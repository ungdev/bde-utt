FROM larueli/php-base-image:7.1

USER 0

ENV APACHE_DOCUMENT_ROOT="/var/www/html/web"

COPY . /var/www/html/
RUN composer install --no-interaction --no-dev --no-ansi && composer dump-autoload --no-dev --classmap-authoritative && \
    chmod g+rwx -R /var/www/html

USER 675654
