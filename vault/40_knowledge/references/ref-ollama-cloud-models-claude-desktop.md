---
title: "Ollama's Cloud models can now be used inside Claude Desktop - sean.winslow28@gmail.com"
source: "https://mail.google.com/mail/u/0/#inbox/FMfcgzQgLjRpvLhPlLMHhpngWWzrjPDt"
author:
published:
created: 2026-05-05
description: "Google's approach to email"
tags:
  - "source/web-clip"
  - "ollama"
  - "claude-desktop"
type: "reference"
status: processed
domain: [claude-mastery]
ai-context: "Ollama 0.23 release announcement — Cloud models can now serve Claude Desktop's third-party inference, making Ollama Cloud usable inside Claude Cowork and Claude Code via `ollama launch claude-desktop`."
---
Ollama 0.23 now supports Claude Desktop’s built-in third party inference.

This allows all models from Ollama's Cloud to be available for use within Claude Cowork and Claude Code from Claude Desktop.

[![](https://ci3.googleusercontent.com/meips/ADKq_NanBZB1sB2Ldlxk0xt4huOJs9ri9jSRMB_lAUwV5lgjRC2dpWzQy8Efs9OgkAovKazVpQneIw8FmNIpMTmb73X8VmEnSePG1HfNGrm8aCzHjIjloXaJWe5ugHh--f3bGLQWbJlaoUW-Lg=s0-d-e1-ft#https://images.vialoops.com/cmoqdesi13bfy0ixlh6s04ofh/cmorjkf63002j0itnvsx15xed.png)](https://c.vialoops.com/CL0/https:%2F%2Fdocs.ollama.com%2Fintegrations%2Fclaude-desktop/1/0100019df5f0c273-fdabdade-d594-45f3-b20d-23f14e76f090-000000/MFcWrBBnhOrm64fd_3BDR11MzOZWw2yWtB7H1vTBya8=452)

### Get started

[Download Ollama 0.23](https://c.vialoops.com/CL0/https:%2F%2Follama.com%2Fdownload/1/0100019df5f0c273-fdabdade-d594-45f3-b20d-23f14e76f090-000000/7PBTEzRqYq3Zjs6uJ-1FSDsREl9_kAH2NEGwrt8vDs4=452), then run:

```
ollama launch claude-desktop
```

You will be prompted to create an [Ollama API key](https://c.vialoops.com/CL0/https:%2F%2Follama.com%2Fsettings%2Fkeys/1/0100019df5f0c273-fdabdade-d594-45f3-b20d-23f14e76f090-000000/l_B9UyZAoNQgRh13GI9LdhwvsV-SpoHzMMysV6WwOvg=452). After setup, Claude Desktop will automatically discover all available Ollama Cloud models.

### Choosing a model

Ollama's cloud models will appear automatically in the model selector

[![](https://ci3.googleusercontent.com/meips/ADKq_NaCypgdNkdeVdjbanC4HQl1SlT0NNuwIYC0Oyyvbnq2ObDaTcgfDQGS_0vpAh-qvasNUvgu9qAWB-imZsOiShEsUg0SXO_32IlzfKMtRTJz5RLCVb8X56Aat7vLpRvPHX8kC1Jb8jAURg=s0-d-e1-ft#https://images.vialoops.com/cmoqdesi13bfy0ixlh6s04ofh/cmorjasew001l0iz87heu28hh.png)](https://c.vialoops.com/CL0/https:%2F%2Fdocs.ollama.com%2Fintegrations%2Fclaude-desktop/2/0100019df5f0c273-fdabdade-d594-45f3-b20d-23f14e76f090-000000/QMjlyz6n7AYrS8IbhOZoS3HLUNQr4ljaSss91p2sqoE=452)

- kimi-k2.6

- qwen3.5

- minimax-m2.7

- glm-5.1

For those who don't yet have a paid subscription with Ollama's cloud, choose a model that supports reliable tool calling and agentic behavior:

- nemotron-3-super

- gemma4:31b

### Restoring to Claude models

To restore the default Claude profile, use --restore:

```
ollama launch claude-desktop --restore
```

If you have any feedback, please directly reply to this email or join [Ollama's Discord channel](https://c.vialoops.com/CL0/https:%2F%2Fdiscord.gg%2Follama/1/0100019df5f0c273-fdabdade-d594-45f3-b20d-23f14e76f090-000000/dEd67RZ_UzW_n0Yf_b8vyNHsZYKNxUtJu_RaV2ZDJ34=452).

Ollama

You are receiving this email because you opted-in to receive updates from Ollama  
Ollama, 744 High Street, Palo Alto, CA 94301  
[Unsubscribe](https://c.vialoops.com/CL0/https:%2F%2Fapp.loops.so%2Funsubscribe%2Fcmos05d9n7y2j018fdboh5qb2%2Ff7024ab9e276f154d32421600937d88e6d082cddc9faaa5c4964f99cb89fb0ff861c41c260874fc5d34971f4e5f55dc450c0af82f1409a6515528a58/1/0100019df5f0c273-fdabdade-d594-45f3-b20d-23f14e76f090-000000/YaPlW7TUSLM67TxQ-C7hPc9pWq3k8b4pAUQdjTIc1MI=452)

---
*Clipped from [google.com](https://mail.google.com/mail/u/0/#inbox/FMfcgzQgLjRpvLhPlLMHhpngWWzrjPDt) on 2026-05-05T06:02:02-04:00*
