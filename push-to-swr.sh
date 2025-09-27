#!/bin/bash

# SWR Login (kendi bilgilerinizi girin)
echo "SWR'a login oluyor..."
docker login -u <username> -p <password> swr.ap-southeast-3.myhuaweicloud.com

# Namespace'i ayarlayın
NAMESPACE="<namespace>"
REGISTRY="swr.ap-southeast-3.myhuaweicloud.com"

echo "Backend build ediliyor ve push ediliyor..."
docker buildx build --platform linux/amd64 \
  -t ${REGISTRY}/${NAMESPACE}/hawai-backend:cci \
  --push \
  ./HawAI-backend

echo "Frontend build ediliyor ve push ediliyor..."
docker buildx build --platform linux/amd64 \
  -t ${REGISTRY}/${NAMESPACE}/hawai-frontend:cci \
  --push \
  ./frontend

echo "Platform doğrulaması yapılıyor..."
echo "Backend platform:"
docker buildx imagetools inspect ${REGISTRY}/${NAMESPACE}/hawai-backend:cci

echo "Frontend platform:"
docker buildx imagetools inspect ${REGISTRY}/${NAMESPACE}/hawai-frontend:cci

echo "✅ Tüm image'lar başarıyla SWR'a push edildi!"
