# temp-kubectl-tool

## Quickstart

1. generated an encoded kubeconfig file:
```
cat ./kubeconfig | base64 | tr -d '\n' > kubeconfig.base64
```
Where ./kubeconfig should be replaced by any kubeconfig file, either downloaded kubeconfig file or ~/.kube/config

2. Start otto8 using Docker with the following commands:
```
docker run -d -p 8080:8080 -e "OPENAI_API_KEY=sk-" -e KUBECONFIG_FILE="$(cat kubeconfig.base64)"  ghcr.io/otto8-ai/otto8:latest
```
This will set the env variable for the right kubeconfig context.

3. Use the URL of this repo to register a kubectl tool.

4. Add the tool to agent and chat!

