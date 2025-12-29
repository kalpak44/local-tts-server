# Local TTS Server

Offline Text-to-Speech server compatible with OpenAI API.

Engines:
- Silero (EN, RU)
- Piper (EN, RU, BG)

Models:
- https://github.com/snakers4/silero-models
- https://huggingface.co/rhasspy/piper-voices/tree/main

## Run

```bash
cp config.env.example config.env
docker build -t local-tts .
docker run --rm -p 5003:5003 --name local-tts -v "$(pwd)/config.env":/app/config.env local-tts
```

## API

### List voices
```shell
curl http://localhost:5003/audio/voices
```



### Generate speech

Russian text → Russian voice
```shell
curl -X POST http://localhost:5003/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input":"Привет мир","voice":"aidar"}' \
  -o out.wav
```

English text → English voice
```shell
curl -X POST http://localhost:5003/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello world","voice":"alan-medium"}' \
  -o out.wav
```

Bulgarian text → Bulgarian voice

```shell
curl -X POST http://localhost:5003/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input":"Здравей свят","voice":"dimitar-medium"}' \
  -o out.wav
```