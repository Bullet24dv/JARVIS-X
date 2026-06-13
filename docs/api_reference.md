# API Reference

## POST /api/v1/chat/completion
Request: { "messages": [...], "temperature": 0.7 }
Response: { "response": "...", "provider": "deepseek" }

## POST /api/v1/voice/tts
Request: { "text": "...", "emotion": "neutral" }
Response: { "audio": "base64..." }

## GET /api/v1/vision/screenshot
Response: { "screenshot": "base64..." }

## POST /api/v1/computer/open
Request: { "name": "chrome" }
Response: { "status": "opened" }