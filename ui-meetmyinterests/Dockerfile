# syntax=docker/dockerfile:1

# Install dependencies only when needed
FROM --platform=linux/amd64 node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

# Rebuild the source code only when needed
FROM --platform=linux/amd64 node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image, copy all the files and run next
FROM --platform=linux/amd64 node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 bloggroup
RUN adduser --system --uid 1001 bloguser

COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
# COPY --from=builder --chown=bloguser:bloggroup /app/.next/standalone ./
COPY --from=builder --chown=bloguser:bloggroup /app/.next/static ./.next/static
RUN mkdir -p /app/.next/cache/images && chown bloguser:bloggroup /app/.next/cache/images
VOLUME /app/.next/cache/images

USER bloguser

ARG REPO
ARG BRANCH
ARG COMMIT
ARG MESSAGE

ENV GIT_REPO=$REPO
ENV GIT_BRANCH=$BRANCH
ENV GIT_COMMIT=$COMMIT
ENV GIT_MESSAGE=$MESSAGE

EXPOSE 3000
CMD ["node_modules/.bin/next", "start"]