# Stage 1: build the static site with Node + pnpm.
FROM node:24-alpine AS build
WORKDIR /app
# corepack provides the exact pnpm version pinned in package.json ("packageManager").
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# Stage 2: serve only the built files (no Node, no sources) with nginx on port 80.
FROM nginx:1.30-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
