# Integrate Google Gen AI with MCP Servers

## MCP Definition

MCP (Model Context Protocol) : Frameworks to integrate LLM (Large Language Model) with another service (API, Databases and Function). MCP can help LLM to execute tools in MCP to connect with external data. Without MCP we need extra code to connect to external. data With MCP we can configure our tools with LLM more easily. MCP can standarize LLM workflow to connect to external data.
In this project I have integrate Google Gen AI API with weather API from https://api.weather.gov/ and order API  from https://services.odata.org/v2/northwind/northwind.svc 


## Prerequisite

- Python
- uv
- Google GenAI 


## How to Setup this MCP Project

1. setup environmental variables

create python environment
```
uv venv
```

activate environment

```
.venv\Scripts\activate
```

2. install MCP CLI to Python

```
uv add "mcp[cli]"
```

3. Check your API response in MCP Inspector

```
uv run mcp dev server/weather.py
```

Please go to http://localhost:your_port/?MCP_PROXY_AUTH_TOKEN=your_token

go to Tools section and you can check your API response


4. Add your tools to Claude

If you have claude you can add your tools to integrate with claude

```
uv run mcp install server/weather.py
```

You can ask your Claude with integrate with your tools


5. Add requirements library

```
uv add langchain_google_genai

uv add mcp_use

uv add onnxruntime==1.16.3

uv pip install fastembed --no-deps
```

6. Run your LLM with CMD

```
uv run server/client.py
```





