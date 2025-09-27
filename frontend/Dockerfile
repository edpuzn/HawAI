# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Package dosyalarını kopyala
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

# Dependencies'leri kur (dev dependencies dahil)
RUN npm ci

# Kaynak kodları kopyala
COPY . .

# Vite executable'ına permission ver
RUN chmod +x node_modules/.bin/vite

# Build işlemi
RUN npm run build

# Production stage
FROM nginx:alpine

# Build edilmiş dosyaları kopyala
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx konfigürasyonu
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Port'u expose et
EXPOSE 80

# Nginx'i çalıştır
CMD ["nginx", "-g", "daemon off;"]