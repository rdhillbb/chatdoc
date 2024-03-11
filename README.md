**Geppetto Doc Chat V01**
11/4/2022 added  config/llmparams.yaml Can not swith between OpenAI and DeepInfra. 
Need to set GOVBOTTIC_LLM in bash/zshrc file
export GOVBOTIC_LLM=DeepInfra:mistralai/Mixtral-8x7B-Instruct-v0.1
Valid Values
OpenAI
OpenAI:gpt-4-0125-preview
OpenAI:gpt-4-turbo-preview

DeepInfra
DeepInfra:mistralai/Mixtral-8x7B-Instruct-v0.1

In the Documents directory you will find an installation and API document.
Sample Test code can be found
-Source_director/sampleapps
-Source_director/ingest/sampleapps
