# CCI Deployment Rehberi

## 🚀 SWR Image'ları ile CCI Deployment

### 1. Backend Deployment

**Image**: `swr.ap-southeast-3.myhuaweicloud.com/hawai/hawai-backend:cci`

**Environment Variables:**
```
MONGO_URL=mongodb://rwuser:Mu2190541%3F@124.243.175.197:8635,188.239.49.153:8635/test?authSource=admin
MONGO_DB=hawai
CORS_ORIGINS=http://frontend:80
JWT_SECRET=hawai-production-secret-key-2024
JWT_ALG=HS256
JWT_EXPIRE_MINUTES=10080
OAI_BASE_URL=http://ollama:11434/v1
OAI_MODEL=llava:7b
APP_NAME=HawAI API
```

**Port**: 8000
**CPU**: 1 Core
**Memory**: 1GB

### 2. Frontend Deployment

**Image**: `swr.ap-southeast-3.myhuaweicloud.com/hawai/hawai-frontend:cci`

**Environment Variables:**
```
VITE_API_BASE=http://backend:8000
```

**Port**: 80
**CPU**: 0.5 Core
**Memory**: 512MB

### 3. Ollama Deployment (Opsiyonel)

**Image**: `ollama/ollama:latest`

**Port**: 11434
**CPU**: 2 Core
**Memory**: 4GB

## 📋 Deployment Sırası

1. **Namespace**: `hawai` oluşturun
2. **ConfigMap**: Environment variables için
3. **Secret**: MongoDB connection string için
4. **Backend**: İlk olarak backend'i deploy edin
5. **Frontend**: Backend hazır olduktan sonra frontend'i deploy edin
6. **Ollama**: Model download için (opsiyonel)

## 🔧 CCI Console'da Yapılacaklar

### 1. Namespace Oluşturma
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: hawai
```

### 2. ConfigMap Oluşturma
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hawai-config
  namespace: hawai
data:
  MONGO_DB: hawai
  CORS_ORIGINS: "*"
  OAI_BASE_URL: http://ollama:11434/v1
  OAI_MODEL: llava:7b
  VITE_API_BASE: http://backend:8000
```

### 3. Secret Oluşturma
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: hawai-secrets
  namespace: hawai
type: Opaque
data:
  JWT_SECRET: Y2hhbmdlLW1l
  MONGO_URL: bW9uZ29kYjovL3J3dXNlcjpNdTIxOTA1NDElM0ZAMTI0LjI0My4xNzUuMTk3Ojg2MzUsMTg4LjIzOS40OS4xNTM6ODYzNS90ZXN0P2F1dGhTb3VyY2U9YWRtaW4=
```

### 4. Backend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: hawai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: swr.ap-southeast-3.myhuaweicloud.com/hawai/hawai-backend:cci
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: hawai-config
            - secretRef:
                name: hawai-secrets
          readinessProbe:
            httpGet:
              path: /docs
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /docs
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: hawai
spec:
  selector:
    app: backend
  ports:
    - name: http
      port: 8000
      targetPort: 8000
  type: ClusterIP
```

### 5. Frontend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: hawai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: swr.ap-southeast-3.myhuaweicloud.com/hawai/hawai-frontend:cci
          env:
            - name: VITE_API_BASE
              value: "http://backend:8000"
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 10
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: hawai
spec:
  selector:
    app: frontend
  ports:
    - name: http
      port: 80
      targetPort: 80
  type: ClusterIP
```

## 🌐 Ingress (Opsiyonel)

Frontend'i dış dünyaya açmak için:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hawai-ingress
  namespace: hawai
spec:
  rules:
  - host: hawai.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

## ✅ Deployment Kontrolü

Deploy sonrası kontrol edin:
- Backend: `http://<backend-ip>:8000/docs`
- Frontend: `http://<frontend-ip>:80/`

## 🔍 Troubleshooting

### Log Kontrolü
```bash
kubectl logs -f deployment/backend -n hawai
kubectl logs -f deployment/frontend -n hawai
```

### Pod Durumu
```bash
kubectl get pods -n hawai
kubectl describe pod <pod-name> -n hawai
```

### Service Kontrolü
```bash
kubectl get services -n hawai
```
