# 🧩 LLM NER(Named Entity Recognition) Benchmarks

<!--- BADGES: START --->

[![Python 3.11.9](https://img.shields.io/badge/python-3.11.9-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![GitHub - License](https://img.shields.io/github/license/Bae-ChangHyun/llm-structured-output-benchmarks?logo=github&style=flat&color=green)][### 🧭 Roadmap

1. **Framework Integration:**
   | Framework | Named Entity Recognition |
   |-----------|:-----------------------:|
   | [Jsonformer](https://github.com/1rgs/jsonformer) | 💭 Planning |
   | [Guidance](https://github.com/guidance-ai/guidance) | 💭 Planning |
   | [DSPy](https://dspy-docs.vercel.app/docs/building-blocks/typed_predictors) | 💭 Planning |

2. **Enhancements:**
   - Multi-language support
   - Additional evaluation metrics
   - Real-time result streaming
   - Advanced visualization features

## 💡 Contribution guidelines

Contributions are welcome! Here are the steps to contribute:

1. **Open an issue** describing your proposed changes
2. **Fork the repository** and create a feature branch
3. **Implement your changes** following the existing code style
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request** with a clear description of changes

## 🙏 Feedback

If this work helped you in any way, please consider ⭐ this repository to give feedback so I can spend more time on this project.

For questions, issues, or suggestions, please open an issue on GitHub.[Github](https://img.shields.io/github/followers/Bae-ChangHyun?style=social)

[#github-license]: https://github.com/Bae-ChangHyun/llm-structured-output-benchmarks/blob/main/LICENSE

<!--- BADGES: END --->

Benchmark LLM on NER tasks with various frameworks and models:
`Instructor`, `Mirascope`, `Langchain`, `LlamaIndex`, `Marvin`, `LMFormatEnforcer`, `OpenAI`, `Google`, `Ollama`

## Attribution

This project is based on the excellent work of the original repository [llm-structured-output-benchmarks](https://github.com/stephenleo/llm-structured-output-benchmarks) created by `stephenleo`.
I would like to express gratitude to the original author for their contribution to the open source community.

## 🏆 Benchmark Results [2025-05-26]

| Framework                                                                                           |                Model                 | Reliability |  Latency p95 (s)   | Precision | Recall | F1 Score | Distance |
| --------------------------------------------------------------------------------------------------- | :----------------------------------: | :---------: | :----------------: | :-------: | :----: | :------: | :------: |
| [OpenAI Structured Output](https://github.com/openai/openai-python)                                 |        gpt-4o-mini-2024-07-18        |    1.000    |       3.459        |   0.834   | 0.748  |  0.789   |  0.211   |
| [LMFormatEnforcer](https://github.com/noamgat/lm-format-enforcer)                                   | unsloth/llama-3-8b-Instruct-bnb-4bit |    1.000    | 6.573<sup>\*</sup> |   0.701   | 0.262  |  0.382   |  0.618   |
| [Instructor](https://github.com/jxnl/instructor)                                                    |        gpt-4o-mini-2024-07-18        |    0.998    |       2.438        |   0.776   | 0.768  |  0.772   |  0.228   |
| [Mirascope](https://github.com/mirascope/mirascope)                                                 |        gpt-4o-mini-2024-07-18        |    0.989    |       3.879        |   0.768   | 0.738  |  0.752   |  0.248   |
| [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/output_parsing/openai_pydantic_program/) |        gpt-4o-mini-2024-07-18        |    0.979    |       5.771        |   0.792   | 0.310  |  0.446   |  0.554   |
| [Marvin](https://github.com/PrefectHQ/marvin)                                                       |        gpt-4o-mini-2024-07-18        |    0.979    |       3.270        |   0.822   | 0.776  |  0.798   |  0.202   |

<sup>\*</sup>GPU: `NVIDIA GeForce RTX 4080 Super`

## 🏃 Run the benchmark

1. **Install the requirements**  
   Run the following command to install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API keys**

   - Create a `.env` file in the root directory based on the provided `.env copy` template.
   - Fill in your API keys as follows:
     ```env
     OPENAI_API_KEY=your_openai_key
     GOOGLE_API_KEY=your_google_key
     ```

3. **Prepare your configuration file**

   - Write your own configuration file for the benchmark. Refer to the examples in the `sample_config` directory for guidance.
   - Configuration files are organized by provider: `sample_config/openai/`, `sample_config/google/`, `sample_config/ollama/`, `sample_config/vllm/`

4. **Run the benchmark**  
   Use the following command to execute the benchmark:

   ```bash
   python -m main run-benchmark
   ```

   **Available options:**

   - `--config`, `-c`: Specify configuration file path (default: `config.yaml`, Required)
   - `--results`, `-r`: Specify results directory (default: `results/{current_date}`, Optional)

   **Examples:**

   ```bash
   # Run
   python -m main run-benchmark --config sample_config/openai/openai_openai.yaml --results my_experiment

   # Get help
   python main.py run-benchmark --help
   ```

5. **Show the results**  
   Use the following command to generate and view the results:

   ```bash
   python main.py show-results
   ```

   **Available options:**

   - `--ground-truth`, `-g`: Specify ground truth PKL file path(Optional)
   - `--sort-by`, `-s`: Sort results by metric `distance`, `f1`, `recall`, `precision`, `reliability`, `latency` (default: distance, Optional)
   - `--files`, `-f`: Analyze specific PKL files (comma-separated, Optional)

   **Examples:**

   ```bash
   # Show all results sorted by F1 score
   python main.py show-results --sort-by f1

   # Show specific files
   python -m main show-results --files results/2025-05-26/OpenAIFramework_gpt-4o-mini.pkl

   # Show multiple experiment results
   python -m main show-results results/experiment1 results/experiment2

   # Use custom ground truth
   python -m main show-results --ground-truth data/custom_labels.pkl

   # Get help
   python main.py show-results --help
   ```

6. **Visualize results**  
   Launch an interactive Json diff visualization tool:

   ```bash
   python -m main visualize
   ```

   **Available options:**

   - `--port`, `-p`: Specify port number (default: 8501)

   **Example:**

   ```bash
   python -m main visualize --port 8080
   ```

7. **Get help on command-line arguments**  
   Add `--help` after any command to view detailed usage instructions.
   ```bash
   python main.py --help
   ```

## ⚙️ Configuring the benchmark

The benchmark is configured using a YAML file (default: `config.yaml`).
Here's how to set up your configuration:

1. **Basic configuration structure:**

   ```yaml
   FrameworkName:
     - task: "ner" # Task type (required)
       retries: 3 # Max retries when framework fails (required)
       init_kwargs: # Framework initialization parameters
         prompt: "Extract and resolve a list of entities from the following text: {text}" # (required)
         llm_model: "gpt-4o-mini-2024-07-18" # Model name (required)
         llm_model_alias: "gpt-4o-mini" # Model alias for display (optional)
         llm_provider: "openai" # Provider type (required)
         source_data_pickle_path: "data/resume_data.pkl" # Ground truth dataset (required)
         description_path: "data/schema.json" # Schema description (optional)
         base_url: "http://localhost:11434" # Custom API endpoint (optional)
         api_delay_seconds: 1 # API delay between requests (optional)
   ```

2. **Supported `llm_provider` values:**

   - `openai`: OpenAI models (requires OPENAI_API_KEY)
   - `google`: Google models like Gemini (requires GOOGLE_API_KEY)
   - `ollama`: Local models via Ollama (set `base_url` in config)
   - `vllm`: vLLM models (set `base_url` in config)
   - `transformers`: Hugging Face Transformers models

## 🔧 Framework Compatibility

Each framework supports specific model providers. The following table shows the compatibility matrix:

| Framework \ Provider      | OpenAI | Google | Ollama | vLLM | Transformers |
| ------------------------- | :----: | :----: | :----: | :--: | :----------: |
| OpenAIFramework           |   ✅   |   ✅   |   ✅   |  ✅  |              |
| GoogleFramework           |        |   ✅   |        |      |              |
| OllamaFramework           |        |        |   ✅   |      |              |
| InstructorFramework       |   ✅   |   ✅   |   ✅   |  ✅  |              |
| MirascopeFramework        |   ✅   |   ✅   |   ✅   |      |              |
| MarvinFramework           |   ✅   |        |   ✅   |      |              |
| LlamaIndexFramework       |   ✅   |   ✅   |   ✅   |  ✅  |              |
| LMFormatEnforcerFramework |        |        |        |      |      ✅      |
| LangchainToolFramework    |   ✅   |   ✅   |   ✅   |  ✅  |              |
| LangchainParserFramework  |   ✅   |   ✅   |   ✅   |  ✅  |              |

**Note:** Framework compatibility is automatically validated using `config/framework_compatibility.yaml`. Incompatible combinations will be filtered out during execution.

## 🧪 Benchmark methodology

### Evaluation Metrics

1. **Reliability**: Percentage of successful executions across all retries
2. **Latency**: 95th percentile response time in seconds
3. **Precision**: Micro-averaged precision score for named entity recognition
4. **Recall**: Micro-averaged recall score for named entity recognition
5. **F1 Score**: Micro-averaged F1 score combining precision and recall
6. **Distance**: Deep difference score using DeepDiff to measure structural similarity

### Experiment Process

1. Each input text is processed through the specified framework with the configured number of retries
2. Success rate, latency, and prediction accuracy are measured for each run
3. Results are aggregated and saved as pickle files with model-specific naming
4. Metrics are calculated by comparing predictions against ground truth labels
5. Results can be visualized and compared across different frameworks and models

## 📊 Adding new data

1. **Create a new dataset:**

   ```python
   import pandas as pd

   # Create DataFrame with required columns
   data = pd.DataFrame({
       'text': ['Resume text content...'],
       'labels': [['Expected', 'entity', 'labels']]
   })

   # Save as pickle file
   data.to_pickle('data/my_dataset.pkl')
   ```

2. **Update configuration:**

   ```yaml
   YourFramework:
     - task: "ner"
       retries: 3
       init_kwargs:
         source_data_pickle_path: "data/my_dataset.pkl"
         # ... other parameters
   ```

3. **Required columns:**
   - `text`: Input text to be processed
   - `labels`: Expected entity labels (list or set format)

## 🏗️ Adding a new framework

1. **Create framework file:**

   ```python
   # frameworks/my_framework.py
   from frameworks.base import BaseFramework, experiment

   class MyFramework(BaseFramework):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           # Initialize your framework-specific components

       def run(self, retries=0, expected_response=None, inputs={}):
           @experiment(retries=retries, expected_response=expected_response, task=self.task)
           def run_experiment(inputs):
               # Implement your framework logic here
               response = your_framework_call(inputs["text"])
               return response

           return run_experiment(inputs)
   ```

2. **Register framework:**

   ```python
   # frameworks/__init__.py
   from .my_framework import MyFramework

   def factory(framework_name, **kwargs):
       # Add your framework to the factory
       if framework_name == "MyFramework":
           return MyFramework(**kwargs)
       # ... existing framework mappings
   ```

3. **Update compatibility:**

   ```yaml
   # config/framework_compatibility.yaml
   MyFramework:
     hosts:
       - openai
       - google
       # ... supported providers
   ```

4. **Create configuration:**
   ```yaml
   # your_config.yaml
   MyFramework:
     - task: "ner"
       retries: 3
       init_kwargs:
         prompt: "Your prompt template with {text}"
         llm_model: "your-model"
         llm_provider: "your-provider"
         source_data_pickle_path: "data/resume_data.pkl"
   ```

## Framework Reference

1. [OpenAI Structured Output](https://platform.openai.com/docs/guides/structured-outputs)
2. [Google Gemini](https://ai.google.dev/gemini-api/docs/structured-output?lang=python)
3. [Ollama](https://ollama.com/blog/structured-outputs)
4. [Instructor](https://python.useinstructor.com)
5. [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/output_parsing/openai_pydantic_program/)
6. [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer)
7. [Marvin](https://github.com/PrefectHQ/marvin)
8. [Mirascope](https://github.com/mirascope/mirascope)
9. [Langchain Tools](https://python.langchain.com/docs/how_to/structured_output/#the-with_structured_output-method)
10. [Langchain Parser](https://python.langchain.com/docs/how_to/structured_output/#prompting-and-parsing-model-outputs-directly)

## 🧭 Roadmap

1. Framework related tasks:
   | Framework | Named Entity Recognition |
   |-----------------------------------------------------------------------------------------------------|:--------------------------:|
   | [Jsonformer](https://github.com/1rgs/jsonformer) | 💭 Planning |
   | [Guidance](https://github.com/guidance-ai/guidance) | 💭 Planning |
   | [DsPy](https://dspy-docs.vercel.app/docs/building-blocks/typed_predictors) | 💭 Planning |

## 💡 Contribution guidelines

Contributions are welcome! Here are the steps to contribute:

1. Please open an issue.

## 🙏 Feedback

If this work helped you in any way, please consider ⭐ this repository to give me feedback so I can spend more time on this project.
