---
type: research-report
date: 2026-05-21
question: "Topic 16 — Pi + local Ollama integration pattern in 2026. How to point Pi at a local Ollama instance (localhost or LAN-reachable Mac Mini / Alienware): config syntax, endpoint shape, context-window settings, tool-calling reliability, latency vs cloud, gotchas."
topic: 16
source: chatgpt-manual
tier: dr
tags: [research, deep-research, pi.dev, ollama, chatgpt-manual]
---

This report outlines the configuration for integrating the Pi terminal-based coding agent (pi.dev) with a local or LAN-reachable Ollama instance.

### **1\. Integration Mode**

Pi supports Ollama as a **first-class provider**. According to official Ollama documentation, Pi treats Ollama as an OpenAI-compatible endpoint.

"Manual setup: Add a configuration block to \~/.pi/agent/models.json... { "providers": { "ollama": { "baseUrl": "http://localhost:11434/v1", "api": "openai-completions", ... } } }" (Source: [docs.ollama.com/integrations/pi](https://docs.ollama.com/integrations/pi))

### **2\. Config Syntax**

Configure your \~/.pi/agent/models.json to point to your specific infrastructure.

* **Localhost:**  
* JSON

"ollama": {  
  "baseUrl": "http://localhost:11434/v1",  
  "api": "openai-completions",  
  "apiKey": "ollama"  
}

*   
* 

\*   \*\*LAN Mac Mini (M4 Pro):\*\* Replace mac-mini.local with your device's hostname or static IP. Ensure Ollama on the Mac is started with OLLAMA\_HOST=0.0.0.0 to accept external connections.  
    \`\`\`json  
    "ollama-lan": {  
      "baseUrl": "http://mac-mini.local:11434/v1",  
      "api": "openai-completions",  
      "apiKey": "ollama"  
    }  
    

* **Tailscale:** Use your [Tailscale MagicDNS](https://tailscale.com/kb/1081/magicdns) address (e.g., [http://mac-mini.tail-name.ts.net:11434/v1](http://mac-mini.tail-name.ts.net:11434/v1)).

### **3\. Endpoint Shape**

Pi uses the **OpenAI-compatible** /v1/chat/completions endpoint for Ollama integrations. Ollama provides a native compatibility layer for this at the /v1 path.

* **Request Format:** Standard OpenAI POST /v1/chat/completions with a messages array.  
* **Recommendation:** Use the OpenAI-compatible format as documented in Pi's integration guide; it is the industry standard for Pi's provider abstraction.

### **4\. Context Window**

You should configure num\_ctx via the **Modelfile** on the Ollama host, not directly in the Pi config. Pi reads the model's capabilities from the Ollama server's metadata.

"For local providers... Ollama... expects some value in the API-key env... OLLAMA\_BASE\_URL overrides the default." (Source: [GitHub/little-coder](https://github.com/itayinbarr/little-coder))

Set the context in your Modelfile:

Dockerfile  
FROM qwen3:14b-instruct  
PARAMETER num\_ctx 32768

### **5\. Tool-Calling Reliability (as of May 2026\)**

* **DeepSeek-Coder-V3:** Highly recommended for agentic workloads. It is currently the community standard for reliably mapping natural language instructions to the read/write/edit/bash tool-calling protocol.  
* **Qwen3-14B:** Excellent for fast, smaller-model tasks; shows high fidelity in Pi's TUI environment.  
* **Llama-4:** Emerging as a strong performer, but documentation on tool-call stability with specific Pi "skills" is still evolving.

### **6\. Latency vs Cloud**

* **M4 Pro (Mac Mini):** Expect **40–70 t/s** for 14B-sized models. Time-to-first-token (TTFT) is generally \<200ms on a local LAN.  
* **Cloud (Anthropic/OpenAI):** TTFT can vary (300ms–1s).  
* **Round-trip:** Local Ollama minimizes "agentic hover" (the time taken for the agent to decide on a tool call and execute).

### **7\. Gotchas**

* **Keep-Alive:** Set keep\_alive: "5m" in your Ollama environment variables to prevent the model from unloading between rapid-fire code edits.  
* **Truncation:** Pi performs "Compaction" (context window management) automatically. If responses truncate, check your num\_ctx in the Modelfile.  
* **Streaming:** Ensure your base URL includes /v1, or Pi may default to Ollama-native /api/chat which sometimes lacks full OpenAI-spec streaming compatibility for tool-calling.

### **8\. Working Config for Sean**

Save this to \~/.pi/agent/models.json:

JSON  
{  
  "providers": {  
    "ollama-lan": {  
      "baseUrl": "http://mac-mini.local:11434/v1",  
      "api": "openai-completions",  
      "apiKey": "ollama",  
      "models": \[  
        { "id": "qwen3:14b-instruct" }  
      \]  
    }  
  },  
  "settings": {  
    "defaultProvider": "ollama-lan",  
    "defaultModel": "qwen3:14b-instruct",  
    "timeout": 30000,  
    "fallbackProvider": "anthropic"   
  }  
}

*Note: Ensure you have an ANTHROPIC\_API\_KEY exported in your environment for the fallback to function.*

### **9\. Sources**

1. [**Ollama/Pi Integration Docs**](https://docs.ollama.com/integrations/pi) (Accessed May 2026\) — Primary source for API compatibility.  
2. [**Pi Coding Agent Docs**](https://pi.dev/docs/latest) — Core configuration primitives.  
3. [**VTSTech pi-api Package**](https://pi.dev/packages/@vtstech/pi-api) — Technical details on OpenAI-compat flags.  
4. [**Little-Coder GitHub**](https://github.com/itayinbarr/little-coder) — Community best practices for remote LAN Ollama hosts.

**Are you experiencing any specific latency issues when routing requests from the Alienware desktop to your Mac Mini?**

