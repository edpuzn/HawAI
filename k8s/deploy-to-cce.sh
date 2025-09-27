#!/bin/bash

# Huawei Cloud CCE deployment scripti
# Kullanım: ./deploy-to-cce.sh [KUBECONFIG_PATH]

set -e

KUBECONFIG_PATH=${1:-"~/.kube/config"}
NAMESPACE="hawai"

echo "🚀 HawAI CCE Deployment Script"
echo "============================="
echo "Kubeconfig: $KUBECONFIG_PATH"
echo "Namespace: $NAMESPACE"
echo ""

# kubectl kontrolü
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl bulunamadı. Lütfen kubectl'i yükleyin."
    exit 1
fi

# Kubeconfig kontrolü
if [ ! -f "$KUBECONFIG_PATH" ]; then
    echo "❌ Kubeconfig dosyası bulunamadı: $KUBECONFIG_PATH"
    echo "Huawei Cloud CCE'den kubeconfig dosyasını indirin."
    exit 1
fi

export KUBECONFIG="$KUBECONFIG_PATH"

# Cluster bağlantısı test et
echo "🔍 CCE cluster bağlantısı test ediliyor..."
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ CCE cluster'a bağlanılamıyor. Kubeconfig'i kontrol edin."
    exit 1
fi

echo "✅ CCE cluster bağlantısı başarılı!"
echo ""

# Namespace oluştur
echo "📦 Namespace oluşturuluyor..."
kubectl apply -f hawai-deployment.yaml

# Deployment durumunu kontrol et
echo "⏳ Deployment'lar başlatılıyor..."
kubectl rollout status deployment/hawai-backend -n $NAMESPACE --timeout=300s
kubectl rollout status deployment/hawai-frontend -n $NAMESPACE --timeout=300s

echo ""
echo "✅ Deployment tamamlandı!"
echo ""

# Servis durumları
echo "📊 Servis durumları:"
kubectl get services -n $NAMESPACE
echo ""

echo "📊 Pod durumları:"
kubectl get pods -n $NAMESPACE
echo ""

echo "📊 Ingress durumu:"
kubectl get ingress -n $NAMESPACE
echo ""

echo "🌐 Erişim bilgileri:"
echo "Frontend: http://hawai.yourdomain.com"
echo "Backend API: http://hawai.yourdomain.com/api"
echo ""
echo "🔧 Debug komutları:"
echo "kubectl logs -f deployment/hawai-backend -n $NAMESPACE"
echo "kubectl logs -f deployment/hawai-frontend -n $NAMESPACE"
echo "kubectl describe ingress hawai-ingress -n $NAMESPACE"
