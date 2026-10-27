# extrair-audio: áudio de vídeo sem perda

Script bash (`extrair-audio`), só ffmpeg/ffprobe, sem venv.

```bash
extrair-audio "pasta ou video.mp4"        # -> audio/ ao lado do vídeo
extrair-audio -o "destino/" "pasta/"      # -> destino escolhido
```

- **Copia a faixa (`-c:a copy`), não reencoda:** o arquivo é bit a bit o mesmo áudio do container. Reencodar pra WAV/FLAC não recupera nada, a perda já aconteceu na gravação.
- Container escolhido pelo codec (aac→m4a, opus→opus, pcm→wav...). Codec exótico cai pra FLAC.
- Aceita arquivo ou pasta (varre mp4/mov/mkv/webm/m4v/avi). Rodar 2x na mesma pasta não reprocessa o `audio/` gerado.
- O padrão é a subpasta `audio/` ao lado do vídeo; `-o` sobrescreve.

## Pra que serve

Passo 1 da limpeza de áudio: extrair, subir no [Adobe Podcast Enhance](https://podcast.adobe.com/en/enhance) (automatizado no repo [Adobe-Podcast-for-Claude-Code](https://github.com/SafeMantella/Adobe-Podcast-for-Claude-Code)) e remuxar no vídeo com `-map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k`. Transcrever o vídeo já com o áudio limpo dá transcrição bem melhor.

## Gotchas do Adobe Podcast (testado em 16/09/2026)

- **`.m4a` é rejeitado** ("File extension or content not currently supported") mesmo sendo AAC válido: o Adobe valida a extensão do container. Converter pra mp3 antes de subir: `ffmpeg -i x.m4a -c:a libmp3lame -b:a 192k x.mp3`. WAV funciona mas passa fácil do limite de upload do browser.
- Clicar em "Download" por automação trava num arquivo temporário sem extensão em `~/Downloads/` (`.com.google.Chrome.XXXXXX`). O arquivo já está completo e válido (`file` identifica como MP3): copiar e renomear, sem repetir o download. Cada clique gera um novo temp; limpar os extras.
- **Remux de áudio limpo em outro vídeo:** conferir que é a mesma tomada. `ffmpeg -i X -map 0:v -c copy -f md5 -` nos dois: hash igual = mesmo stream, sync garantido. Comparar MD5 de frame decodificado com `-ss` não serve (o seek cai em frames diferentes).
