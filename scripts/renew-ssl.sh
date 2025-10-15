#!/bin/bash
docker compose -f ../docker/prod/docker-compose.yml run --rm certbot renew
docker compose -f ../docker/prod/docker-compose.yml exec nginx nginx -s reload