#!/bin/bash

# Huawei Cloud SWR ve CCE için image build scripti
# Kullanım: ./build-images.sh [SWR_REGISTRY_URL] [NAMESPACE]

set -e

# Varsayılan değerler
SWR_REGISTRY=${1:-"swr.ap-southeast-3.myhuaweicloud.com"}
NAMESPACE=${2:-"hawai"}
PROJECT_NAME="hawai"

echo "🚀 HawAI Docker Images Build & Push Script"
echo "=========================================="
echo "SWR Registry: $SWR_REGISTRY"
echo "Namespace: $NAMESPACE"
echo ""

# Docker login kontrolü
echo "📋 Docker login durumu kontrol ediliyor..."
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon çalışmıyor. Lütfen Docker'ı başlatın."
    exit 1
fi

# Frontend build
echo "🔨 Frontend image build ediliyor..."
cd frontend
docker build -t ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-frontend:latest .
docker tag ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-frontend:latest ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-frontend:$(date +%Y%m%d-%H%M%S)
cd ..

# Backend build  
echo "🔨 Backend image build ediliyor..."
cd HawAI-backend
docker build -t ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-backend:latest .
docker tag ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-backend:latest ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-backend:$(date +%Y%m%d-%H%M%S)
cd ..

echo "✅ Build tamamlandı!"
echo ""
echo "📤 SWR'a push etmek için:"
echo "docker login $SWR_REGISTRY"
echo "docker push ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-frontend:latest"
echo "docker push ${SWR_REGISTRY}/${NAMESPACE}/${PROJECT_NAME}-backend:latest"
echo ""
echo "🔍 Image'ları kontrol etmek için:"
echo "docker images | grep $PROJECT_NAME"
