# Real-Time Notification Microservice (deepak-dk)

A Django-based real-time notification system using REST APIs, Celery workers, Redis queues, and WebSocket delivery channels.

## Features
- Send notifications via REST API
- Real-time WebSocket streaming
- Celery asynchronous processing
- Upstash Redis free-tier integration
- Render free-tier hosting
- GitHub Pages frontend UI

## API Example
POST /api/notify/
{
  "user_id": 1,
  "message": "Hello World"
}

## WebSocket
wss://your-domain/ws/notifications/<user_id>/

## Deployment
- Backend on Render (free)
- Redis on Upstash (free)
- Demo UI on GitHub Pages (free)

## Author
**Deepak A — Backend Engineer**