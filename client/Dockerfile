FROM node:20-slim AS build

WORKDIR /app

# Install native build tools (needed for packages like rollup, esbuild, etc.)
RUN apt-get update && apt-get install -y \
  python3 \
  make \
  g++ \
  bash \
  && rm -rf /var/lib/apt/lists/*

# Copy config files first to leverage Docker layer caching
COPY package.json package-lock.json .npmrc ./

# Optional: clear everything before install
RUN rm -rf node_modules package-lock.json

# Avoid buggy optional installs
ENV npm_config_optional=false

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
