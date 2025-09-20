### Dify (lokal) + Plugin’ler

- .env hazır: `dify/docker/.env` (ENABLE_PLUGINS=true)
- Çalıştırma (proje kökü):

```bash
docker compose -f docker-compose.override.yml up -d
# durum
docker compose -f docker-compose.override.yml ps
```

- Servisler:
  - dify-web: http://localhost:3000
  - dify-api: http://localhost:5001
  - dify-plugin-daemon: 5097 (opsiyonel debug)
  - dify-worker, dify-db, dify-redis

- Not: Bu kurulum sadece lokal geliştirme içindir; bulut/üretim ayarı eklemeyin.

## Docker Compose Integration

Tek komutla Dify + Backend + Ollama’yı ayağa kaldırmak için kökteki `docker-compose.override.yml` dosyasını kullanın.

### Servis adresleri
- Dify Web UI: http://localhost:3000
- Dify API: http://localhost:5001
- HawAI Backend: http://localhost:8000
- Ollama API: http://localhost:11434

### İlk kurulum
1. `docker compose up -d`
2. Tarayıcıdan `http://localhost:3000/install` adresine gidin ve Dify kurulumunu tamamlayın.
3. Dify’de App oluşturup App API Key’i alın, `HawAI-backend/.env` dosyasında `DIFY_APP_KEY` alanına koyun.

### Test
```bash
curl -s http://localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"message":"Sigarayı bırakmak istiyorum"}' | jq

docker compose ps
```


