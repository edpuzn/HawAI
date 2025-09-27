# HawAI CCI Deployment Rehberi

## 🚀 Adım Adım Deployment

### 1. SWR Login
```bash
# SWR'a login olun (kendi bilgilerinizi girin)
docker login -u <username> -p <password> swr.ap-southeast-3.myhuaweicloud.com
```

### 2. Docker Buildx Ayarları
```bash
# Buildx builder oluşturun (eğer yoksa)
docker buildx create --name multiarch --use

# Builder'ı başlatın
docker buildx inspect --bootstrap
```

### 3. Image'ları Build ve Push Et
```bash
# Script'i çalıştırın (namespace'i düzenleyin)
./push-to-swr.sh
```

**Manuel komutlar:**
```bash
# Backend
docker buildx build --platform linux/amd64 \
  -t swr.ap-southeast-3.myhuaweicloud.com/<namespace>/hawai-backend:cci \
  --push \
  ./HawAI-backend

# Frontend
docker buildx build --platform linux/amd64 \
  -t swr.ap-southeast-3.myhuaweicloud.com/<namespace>/hawai-frontend:cci \
  --push \
  ./frontend
```

### 4. Platform Doğrulaması
```bash
# Backend platform kontrolü
docker buildx imagetools inspect swr.ap-southeast-3.myhuaweicloud.com/<namespace>/hawai-backend:cci

# Frontend platform kontrolü
docker buildx imagetools inspect swr.ap-southeast-3.myhuaweicloud.com/<namespace>/hawai-frontend:cci
```

### 5. CCI'da Deploy Et
```bash
# YAML dosyalarındaki <namespace> kısmını kendi namespace'inizle değiştirin
# Sonra deploy edin:

kubectl apply -f k8s/hawai-backend-deployment.yaml
kubectl apply -f k8s/hawai-frontend-deployment.yaml
```

### 6. Deployment Durumunu Kontrol Et
```bash
# Pod'ları kontrol edin
kubectl get pods

# Service'leri kontrol edin
kubectl get services

# Log'ları kontrol edin
kubectl logs -f deployment/hawai-backend
kubectl logs -f deployment/hawai-frontend
```

### 7. Hata Takibi
```bash
# Pod durumunu detaylı kontrol
kubectl describe pod <pod-name>

# Event'leri kontrol et
kubectl get events --sort-by=.metadata.creationTimestamp

# Log'ları takip et
kubectl logs -f <pod-name>
```

## 🔧 Önemli Notlar

- **Platform**: Tüm build'ler `linux/amd64` için yapılıyor
- **Namespace**: YAML dosyalarındaki `<namespace>` kısmını kendi namespace'inizle değiştirin
- **Environment Variables**: Backend'de MongoDB ve diğer servisler için gerekli env'ler ayarlanmış
- **Health Checks**: Liveness ve readiness probe'ları ayarlanmış
- **Resources**: CPU ve memory limitleri ayarlanmış

## 🚨 Sorun Giderme

### Exec Format Error
- Image'ların `linux/amd64` platformunda build edildiğinden emin olun
- `docker buildx imagetools inspect` ile platformu doğrulayın

### Pod CrashLoopBackOff
- `kubectl logs <pod-name>` ile log'ları kontrol edin
- Environment variable'ları kontrol edin
- Resource limitlerini kontrol edin

### Image Pull Error
- SWR login'inin doğru olduğundan emin olun
- Image path'inin doğru olduğundan emin olun
- Namespace'in doğru olduğundan emin olun
