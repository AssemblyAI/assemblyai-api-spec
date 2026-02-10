# Check nginx configuration
docker compose exec streaming-asr-lb nginx -t

# Restart specific service
docker compose restart streaming-api
docker compose restart streaming-asr-english
docker compose restart streaming-asr-multilang
