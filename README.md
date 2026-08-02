# How to Use This Repo

## 1. Checkout

Clone and checkout the repository.

## 2. Start Docker Environment

Run:

```bash
docker compose up
```

## 3. Pull an Ollama Model

Open the Ollama container and pull a model:

```bash
ollama pull qwen2.5:7b-instruct
```

`qwen2.5:7b-instruct` is just my choice. You can pick any model you prefer, but I would suggest keeping it in the **7B+ parameter range**.

## 4. Download Checkpoints

Download the checkpoints and place them inside:

```
comfy/models/checkpoints
```

Recommended starting checkpoints:

- `DreamShaper_8_pruned.safetensors`
- `Realistic_Vision_V5.1.safetensors`

## 5. Select Checkpoint Based on Version

Use the following checkpoints depending on the version:

| Version | Checkpoint |
|---|---|
| V1 | `DreamShaper_8_pruned` |
| V2 | `DreamShaper_8_pruned` |
| V3 | `Realistic_Vision_V5.1` |

> Note: V3 is still a work in progress. This guide is written with V2 in mind, so V2 is recommended.

## 6. Configure Docker Compose

Open:

```
docker-compose.yml
```

Change the `SAMPLER_NODES` value:

```
SAMPLER_NODES="5,8"
```

Also change the workflow name to:

```
WORKFLOW_NAME=V2.0
```

## 7. Configure OpenWebUI with comfy-mcp

Open **OpenWebUI** and configure it to use `comfy-mcp` by adding an integration.

Official documentation:

https://docs.openwebui.com/features/extensibility/

The workflow should look like:

```
User
 └── Setting
     └── Admin Setting
         └── Integrations
             └── External Tool Servers
                 └── "+" button
```

## 8. Add External Tool Server

Provide the URL:

```
http://mcpo:8001
```

For reference, check the `configure_mcp` screenshot in the repository:

```
doc/configure_mcp
```

## 9. Configure Model System Prompt

Navigate to:

```
User
 → Setting
 → Admin Setting
 → Models
 → Select the model you picked in Step 3
```

Set the system prompt using:

```
doc/system_prompt.txt
```

## 10. Enable Tool for the Model

Navigate again:

```
User
 → Setting
 → Admin Setting
 → Models
 → Select the model you picked in Step 3
```

Then:

1. Select the tool added in Step 8.
2. Select the tool name you configured.

Take a look at for reference

```
doc/configure_model.png
```

## 11. Have Fun!

Everything should now be configured and ready to use. 🚀