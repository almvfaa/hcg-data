# Etapa de construcción
FROM node:18-alpine AS builder

# Establecer directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar código fuente y construir
COPY . .

# Argumento para la URL del API, que será pasado por Render
ARG NEXT_PUBLIC_API_URL
# Establecer la variable de entorno para que el comando de build la use
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build

# Etapa de producción
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar solo lo necesario desde la etapa de construcción
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Exponer puerto 3000
EXPOSE 3000

# Comando para iniciar la aplicación
CMD ["npm", "start"]
