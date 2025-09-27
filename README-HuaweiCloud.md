# HawAI - Huawei Cloud Deployment Guide

Bu rehber HawAI uygulamasını Huawei Cloud SWR (Software Repository for Container) ve CCE (Cloud Container Engine) kullanarak deploy etmek için hazırlanmıştır.

## 🏗️ Gereksinimler

- Docker Desktop
- kubectl
- Huawei Cloud hesabı
- CCE cluster (en az 2 node)

## 📋 Adım Adım Deployment

### 1. SWR Registry'ye Login

```bash
# Huawei Cloud SWR'a login olun
docker login swr.ap-southeast-1.myhuaweicloud.com
# Username: [Huawei Cloud kullanıcı adınız]
# Password: [Huawei Cloud şifreniz]
```

### 2. Docker Images Build & Push

```bash
# Images'ları build et ve SWR'a push et
./build-images.sh swr.ap-southeast-1.myhuaweicloud.com hawai

# Manuel push (eğer script çalışmazsa)
docker push swr.ap-southeast-1.myhuaweicloud.com/hawai/hawai-frontend:latest
docker push swr.ap-southeast-1.myhuaweicloud.com/hawai/hawai-backend:latest
```

### 3. CCE Cluster'a Deploy

```bash
# CCE cluster kubeconfig'ini indirin ve ayarlayın
export KUBECONFIG=~/path/to/your/kubeconfig

# Deployment'ı başlatın
cd k8s
./deploy-to-cce.sh

# Manuel deployment (eğer script çalışmazsa)
kubectl apply -f hawai-deployment.yaml
```

### 4. Domain ve Ingress Ayarları

`k8s/hawai-deployment.yaml` dosyasında:
- `hawai.yourdomain.com` yerine kendi domain'inizi yazın
- Ingress controller'ın CCE'de aktif olduğundan emin olun

## 🔧 Konfigürasyon

### Environment Variables

Backend için gerekli environment variables `hawai-deployment.yaml` içinde tanımlanmıştır:

- `MONGO_URL`: MongoDB bağlantı URL'si
- `CORS_ORIGINS`: Frontend URL'si
- `JWT_SECRET`: JWT secret key
- `OAI_BASE_URL`: Ollama API URL'si

### Secrets

Hassas bilgiler Kubernetes secrets olarak saklanır:
- MongoDB şifresi
- JWT secret key

## 📊 Monitoring ve Debug

### Pod Logları

```bash
# Backend logları
kubectl logs -f deployment/hawai-backend -n hawai

# Frontend logları  
kubectl logs -f deployment/hawai-frontend -n hawai
```

### Servis Durumu

```bash
# Tüm servisleri listele
kubectl get all -n hawai

# Ingress durumu
kubectl describe ingress hawai-ingress -n hawai
```

### Scaling

```bash
# Backend'i 3 replica'ya scale et
kubectl scale deployment hawai-backend --replicas=3 -n hawai

# Frontend'i 3 replica'ya scale et
kubectl scale deployment hawai-frontend --replicas=3 -n hawai
```

## 🚨 Troubleshooting

### Yaygın Sorunlar

1. **Image Pull Error**: SWR registry'ye login olduğunuzdan emin olun
2. **Pod CrashLoopBackOff**: Logları kontrol edin, environment variables doğru mu?
3. **Ingress 404**: Domain ayarlarını ve path'leri kontrol edin
4. **CORS Error**: Backend CORS_ORIGINS ayarını kontrol edin

### Debug Komutları

```bash
# Pod detayları
kubectl describe pod <pod-name> -n hawai

# ConfigMap kontrolü
kubectl get configmap hawai-config -n hawai -o yaml

# Secret kontrolü
kubectl get secret hawai-secrets -n hawai -o yaml
```

## 🔄 Update Process

### Yeni Image Deploy Etme

```bash
# 1. Yeni image build et
./build-images.sh

# 2. SWR'a push et
docker push swr.ap-southeast-1.myhuaweicloud.com/hawai/hawai-frontend:latest
docker push swr.ap-southeast-1.myhuaweicloud.com/hawai/hawai-backend:latest

# 3. Deployment'ı restart et
kubectl rollout restart deployment/hawai-backend -n hawai
kubectl rollout restart deployment/hawai-frontend -n hawai
```

## 📈 Production Optimizasyonları

### Resource Limits

Production'da resource limits'leri artırın:
- Backend: 1GB RAM, 1 CPU
- Frontend: 512MB RAM, 0.5 CPU

### Health Checks

Liveness ve readiness probe'ları production load'una göre ayarlayın.

### SSL/TLS

Production'da SSL sertifikası ekleyin:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - hawai.yourdomain.com
    secretName: hawai-tls
```

## 📞 Destek

Sorunlar için:
1. Logları kontrol edin
2. Kubernetes events'leri inceleyin: `kubectl get events -n hawai`
3. Huawei Cloud CCE dokümantasyonunu kontrol edin
