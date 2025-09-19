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


