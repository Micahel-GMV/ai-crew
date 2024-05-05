from langchain_openai import ChatOpenAI

from ..utils.env_man import config

class LlmDto:
    def __init__(self, name, base_url, openai_api_key, is_local, size, volume, quantization, architecture, datasets, model_type, model_purpose):
        if not all([name, base_url, openai_api_key]):
            raise ValueError("Parameters needed for the ChatOpenAi object instantiation are mandatory: name, base_url, openai_api_key")

        self.llm = ChatOpenAI(
            model=name,
            base_url=base_url,
            openai_api_key=openai_api_key,
            api_key=openai_api_key  # Assuming api_key is the same as openai_api_key
        )
        self.name = name
        self.is_local = is_local
        self.size = size
        self.volume = volume
        self.quantization = quantization
        self.architecture = architecture
        self.datasets = datasets
        self.type = model_type
        self.model_purpose = model_purpose

    def __repr__(self):
        return f"<Model {self.name}, Local: {self.is_local}, Type: {self.type}, Purpose: {self.model_purpose}, Size: {self.size}>"

    def get_llm(self):
        return self.llm

class LlmMan:
    def __init__(self):
        self.llms = []
        self.init_models()

    def add_model(self, name, base_url, openai_api_key, is_local, size, volume, quantization, architecture, datasets, model_type, model_purpose):
        model = LlmDto(name, base_url, openai_api_key, is_local, size, volume, quantization, architecture, datasets, model_type, model_purpose)
        self.llms.append(model)

    def list_models(self):
        for model in self.llms:
            print(model)
    def init_models(self):
        base_url_web = config.get("web_llm", "base_url")
        api_key_web = config.get("web_llm", "api_key")

        base_url_loc = config.get("local_llm", "base_url")
        api_key_loc = config.get("local_llm", "api_key")

        models_info = [ # TODO: move this hell to the database or any simpler table
            # name                       base_url        api_key        is_local  size      volume  quant  architecture    datasets                model type                  model purpose
            ("gpt-3.5-turbo",            base_url_web,   api_key_web,   False,    "Size TBD", 1,    False, "transformer",  ["Wide-range Datasets"], "Web-based NLP",           "Highly versatile, large-scale NLP model capable of understanding and generating human-like text."),
            ("all-minilm",               base_url_loc,   api_key_loc,   True,     "45 MB",    1,    False, "transformer",  ["Text Corpus"],         "General NLP",             "Compact model for general natural language processing tasks."),
            ("codebooga",                base_url_loc,   api_key_loc,   True,     "19 GB",    2,    True,  "neural net",   ["Developer Code"],      "Coding Assistance",       "Advanced model for automated code generation and analysis."),
            ("codegemma",                base_url_loc,   api_key_loc,   True,     "5.0 GB",   1,    False, "transformer",  ["Project Code"],        "Code Analysis",           "Optimized for static code analysis and quality improvements."),
            ("codeqwen",                 base_url_loc,   api_key_loc,   True,     "4.2 GB",   1,    False, "transformer",  ["Public Repos"],        "Code Generation",         "Focuses on generating boilerplate code from specifications."),
            ("dolphincoder",             base_url_loc,   api_key_loc,   True,     "4.2 GB",   1,    False, "transformer",  ["Programming Forums"],  "Coding",                  "Designed to interpret and answer programming queries."),
            ("falcon",                   base_url_loc,   api_key_loc,   True,     "4.2 GB",   1,    False, "transformer",  ["Scientific Computing"],"Research",                "Used in high-performance computing tasks for research."),
            ("gemma",                    base_url_loc,   api_key_loc,   True,     "5.0 GB",   1,    False, "transformer",  ["Data Sets"],           "Data Analysis",           "Specializes in data mining and pattern recognition."),
            ("llama3",                   base_url_loc,   api_key_loc,   True,     "4.7 GB",   1,    False, "llama",        ["Large Texts"],         "NLP",                     "Enhanced capabilities for understanding and generating natural language."),
            ("magicoder",                base_url_loc,   api_key_loc,   True,     "3.8 GB",   1,    False, "transformer",  ["Source Code"],         "Coding",                  "Focuses on automating routine coding tasks."),
            ("mistral",                  base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["General Text"],        "General NLP",             "General-purpose NLP model for a variety of text processing tasks."),
            ("mistral-openorca",         base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Open Data"],           "Open Tasks",              "Capable of handling diverse datasets for open-ended tasks."),
            ("mistrallite",              base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Lite Tasks"],          "Lightweight NLP",         "Lighter version of Mistral for less resource-intensive tasks."),
            ("mixtral",                  base_url_loc,   api_key_loc,   True,     "26 GB",    2,    True,  "transformer",  ["Mixed Data"],          "High Performance",        "High-capacity model designed for complex data processing tasks."),
            ("moondream",                base_url_loc,   api_key_loc,   True,     "1.7 GB",   1,    False, "transformer",  ["Dream Analysis"],      "Dream Modeling",          "Specialized in modeling and interpreting dream content."),
            ("mxbai-embed-large",        base_url_loc,   api_key_loc,   True,     "669 MB",   1,    False, "transformer",  ["Embeddings"],          "Embedding",               "Focused on creating and using large-scale text embeddings."),
            ("neural-chat",              base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Chat Data"],           "Chatbot",                 "Designed to simulate conversational dynamics for chatbots."),
            ("nexusraven",               base_url_loc,   api_key_loc,   True,     "7.4 GB",   2,    True,  "transformer",  ["Complex NLP Tasks"],   "Advanced NLP",            "Advanced NLP model for complex language understanding and generation."),
            ("nomic-embed-text",         base_url_loc,   api_key_loc,   True,     "274 MB",   1,    False, "transformer",  ["Text Embedding"],      "Embedding",               "Efficient at producing text embeddings for various applications."),
            ("notux",                    base_url_loc,   api_key_loc,   True,     "26 GB",    2,    True,  "transformer",  ["High-Capacity Tasks"], "Advanced Computation",    "Designed for computational tasks requiring extensive resources."),
            ("open-orca-platypus2",      base_url_loc,   api_key_loc,   True,     "7.4 GB",   2,    True,  "orca",         ["Diverse Datasets"],    "Data Processing",         "Handles complex data processing tasks across various domains."),
            ("openchat",                 base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Chat Applications"],   "Chat Interfaces",         "Optimized for building interactive chat interfaces."),
            ("phi3",                     base_url_loc,   api_key_loc,   True,     "2.3 GB",   1,    False, "transformer",  ["Educational Content"], "Education",               "Designed to support and enhance educational applications."),
            ("phind-codellama",          base_url_loc,   api_key_loc,   True,     "19 GB",    2,    True,  "llama",        ["Coding Challenges"],   "Problem Solving",         "Excels in solving complex coding problems and challenges."),
            ("solar",                    base_url_loc,   api_key_loc,   True,     "6.1 GB",   1,    False, "transformer",  ["Solar Data"],          "Energy Forecasting",      "Used for predictive modeling in solar energy systems."),
            ("stable-code",              base_url_loc,   api_key_loc,   True,     "1.6 GB",   1,    False, "transformer",  ["Stable Systems"],      "System Stability",        "Ensures stability in automated systems."),
            ("starcoder2",               base_url_loc,   api_key_loc,   True,     "9.1 GB",   1,    True,  "transformer",  ["Next-gen Coding"],     "Cutting-edge Coding",     "Advanced model for next-generation code development."),
            ("starling-lm",              base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Language Data"],       "Language Modeling",       "Specializes in language modeling for various applications."),
            ("tinydolphin",              base_url_loc,   api_key_loc,   True,     "636 MB",   1,    False, "transformer",  ["Quick Tasks"],         "Quick Analysis",          "Rapid analysis and response for on-the-go tasks."),
            ("tinyllama",                base_url_loc,   api_key_loc,   True,     "637 MB",   1,    False, "transformer",  ["Small Tasks"],         "Efficiency",              "Efficient processing for small-scale tasks."),
            ("wizard-math",              base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Math Problems"],       "Mathematical Analysis",   "Specializes in solving complex mathematical problems."),
            ("wizard-vicuna-uncensored", base_url_loc,   api_key_loc,   True,     "3.8 GB",   1,    False, "transformer",  ["Uncensored Content"],  "Content Moderation",      "Handles and moderates uncensored content effectively."),
            ("wizardcoder",              base_url_loc,   api_key_loc,   True,     "35 GB",    2,    True,  "transformer",  ["Elite Coding"],        "Elite Coding Tasks",      "Top-tier model for elite coding tasks and algorithms."),
            ("wizardlm2",                base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Broad NLP"],           "General NLP",             "Versatile NLP capabilities for broad applications."),
            ("xwinlm",                   base_url_loc,   api_key_loc,   True,     "3.8 GB",   1,    False, "transformer",  ["Cross-window Learning"],"Cross-learning",         "Facilitates learning across multiple data windows."),
            ("yi",                       base_url_loc,   api_key_loc,   True,     "3.5 GB",   1,    False, "transformer",  ["General AI"],          "General Purpose AI",      "General-purpose AI for a wide range of tasks."),
            ("zephyr",                   base_url_loc,   api_key_loc,   True,     "4.1 GB",   1,    False, "transformer",  ["Light Applications"],  "Real-time Processing",    "Optimized for real-time processing in lightweight applications.")
        ]

        for info in models_info:
            self.add_model(*info)

    def get_model_byname(self, model_name):
        for model in self.llms:
            if model.name == model_name:
                return model
        return None  # or raise an exception if you prefer


