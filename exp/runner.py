import os

def run(provider_list, prefix):
    
    google_config = [i for i in os.listdir('sample_config/google') if i.endswith('.yaml')]
    ollama_config = [i for i in os.listdir('sample_config/ollama') if i.endswith('.yaml')]
    openai_config = [i for i in os.listdir('sample_config/openai') if i.endswith('.yaml')]
    vllm_config = [i for i in os.listdir('sample_config/vllm') if i.endswith('.yaml')]

    configs = {
        "ollama": ollama_config,
        "openai": openai_config,
        "google": google_config,
        "vllm": vllm_config
    }

    for provider in provider_list:
        for idx, config in enumerate(configs.get(provider, [])):
            root = f"sample_config/{provider}/"
            name = config.split('.')[0]
            print(f"Running benchmark for {provider} config: {name}, idx/{idx}/{len(configs[provider])}")
            try:
                os.system(f"python -m main run-benchmark -c {root}{config} -r {name}{prefix}")
            except:
                print(f"Failed to run benchmark for {name} with {provider} config {config}")
            continue
    
if __name__ == "__main__":
    prefix = "marine"
    #provider_list = ["ollama", "openai", "google", "vllm"]
    provider_list = [ "openai", "google"]
    
    run(provider_list=provider_list, prefix=prefix)