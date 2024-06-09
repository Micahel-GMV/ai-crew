from langchain_openai import ChatOpenAI

from ..utils.env_man import config

class LlmDto:
    def __init__(self, name : str, base_url : str, openai_api_key : str, is_local : bool, size : float, volume : float, quantization : any, architecture : str, datasets : str, model_type : str, model_purpose : str):
        if not all([name, base_url, openai_api_key]):
            raise ValueError("Required parameters are missing for LLM initialization: name, base_url, openai_api_key")
        self.llm = ChatOpenAI(model=name, base_url=base_url, openai_api_key=openai_api_key, api_key=openai_api_key)
        self.name = name
        self.is_local = is_local
        self.size = size
        self.volume = volume
        self.quantization = quantization
        self.architecture = architecture
        self.datasets = datasets[:]
        self.model_type = model_type
        self.model_purpose = model_purpose

    def get_model_type(self) -> str:
        """Return the model type of the LLM."""
        return self.model_type

    def get_llm(self) -> ChatOpenAI:
        return self.llm

    def get_name(self) -> str:
        return self.name

    def copy(self):
        return LlmDto(self.name, self.llm.openai_api_base, self.llm.openai_api_key, self.is_local, self.size, self.volume, self.quantization, self.architecture, self.datasets, self.model_type, self.model_purpose)

    def __repr__(self):
        return (f"<Model {self.name}, Local: {self.is_local}, Type: {self.model_type}, "
                f"Purpose: {self.model_purpose}, Size: {self.size}>")


class LlmProvider:
    def __init__(self):
        self.llms : [LlmDto] = []
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
            # name                       base_url        api_key        is_local  size,GB  tokens,B quant  architecture    datasets                          model type                  model purpose
            ("gpt-3.5-turbo",            base_url_web,   api_key_web,   False,    0.0,      175,    False,  "transformer", ["Wide-range Datasets"],              "pretrained",           "Highly versatile, large-scale NLP model capable of understanding and generating human-like text."),
            ("gpt-3.5-turbo-instruct",   base_url_web,   api_key_web,   False,    0.0,      175,    False,  "transformer", ["Wide-range Datasets"],              "pretrained",           "Highly versatile, large-scale NLP model capable of understanding and generating human-like text."),
            ("text-embedding-ada-002",   base_url_web,   api_key_web,   False,    0.0,      175,    False,  "transformer", ["Wide-range Datasets"],              "pretrained",           "Highly versatile, large-scale NLP model capable of understanding and generating human-like text."),
            ("babbage-002",              base_url_web,   api_key_web,   False,    0.0,      175,    False,  "transformer", ["Wide-range Datasets"],              "pretrained",           "Highly versatile, large-scale NLP model capable of understanding and generating human-like text."),
            ("gpt-4",                    base_url_web,   api_key_web,   False,    0.0,      175,    False,  "transformer", ["Wide-range Datasets"],              "pretrained",           "Highly versatile, large-scale NLP model capable of understanding and generating human-like text."),
            ("text-embedding-3-large",   base_url_web,   api_key_web,   False,    0.0,      175,    False,  "transformer", ["Wide-range Datasets"],              "pretrained",           "Highly versatile, large-scale NLP model capable of understanding and generating human-like text."),

            ("openhermes:latest",        base_url_loc,   api_key_loc,   False,     4.1,      7.0,  4,     "transformer",  ["Chat Applications"],   "pretrained",         "Optimized for building interactive chat interfaces."),
            ("solar",                    base_url_loc,   api_key_loc,   False,     4.1,      7.0,  4,     "transformer",  ["Chat Applications"],   "pretrained",         "Optimized for building interactive chat interfaces."),

            # ("all-minilm",               base_url_loc,   api_key_loc,   True,     0.045,    0.023,  "F16" , "transformer", ["Text Corpus"],                      "embedded",             "Compact model for general natural language processing tasks."),
            ("codebooga",                base_url_loc,   api_key_loc,   True,     19.0,     34.0,   4,      "transformer", ["Developer Code"],                   "pretrained",       "Advanced model for automated code generation and analysis."),
            # More than 25 mins @0.3 during write_report test. Frozen @0.2
            ("codegemma",                base_url_loc,   api_key_loc,   True,     5.0,      9.0,    4,      "gemma",       ["Project Code"],                     "pretrained",           "Optimized for static code analysis and quality improvements."), # has 3 variants: instruct, cose, 2b - test deeply
            ("codeqwen",                 base_url_loc,   api_key_loc,   True,     4.2,      7.0,    4,      "qwen2",       ["Public Repos"],                     "pretrained",         "Focuses on generating boilerplate code from specifications."),
            ("codestral",                base_url_loc,   api_key_loc,   True,     4.1,      1,      False, "transformer",  ["General Text"],        "pretrained",             "General-purpose NLP model for a variety of text processing tasks."),
            # ("command-r",                 base_url_loc,   api_key_loc,   True,     4.2,      7.0,    4,      "qwen2",       ["Public Repos"],                     "pretrained",         "Focuses on generating boilerplate code from specifications."),
            # Timeouts: pass content @0.7
            # ("command-r-plus:104b-q2_K",                 base_url_loc,   api_key_loc,   True,     4.2,      7.0,    4,      "qwen2",       ["Public Repos"],                     "pretrained",         "Focuses on generating boilerplate code from specifications."),
            # Timeouts: pass content @0.0 just from the start
            ("dolphincoder",             base_url_loc,   api_key_loc,   True,     4.2,      7.0,    4,      "starcoder2",  ["Programming Forums"],               "pretrained",                  "Designed to interpret and answer programming queries."),
            ("falcon",                   base_url_loc,   api_key_loc,   True,     4.2,      7.0,    4,      "falcon",      ["Falcon RefinedWeb"],                "pretrained",                "Used in high-performance computing tasks for research."),
            ("gemma",                    base_url_loc,   api_key_loc,   True,     5.0,      9.0,    4,      "gemma",       ["Web documents, code, mathematics"], "pretrained",           "Specializes in data mining and pattern recognition."),
            ("llama3",                   base_url_loc,   api_key_loc,   True,     4.7,   8.0,    4, "llama",               ["Large Texts"],                      "pretrained",                   "Enhanced capabilities for understanding and generating natural language."),
            # Loves English classical literature too much. Is not usable for precise work.
            ("llama3:instruct",                   base_url_loc,   api_key_loc,   True,     4.7,   8.0,    4, "llama",               ["Large Texts"],                      "pretrained",                   "Enhanced capabilities for understanding and generating natural language."),
            ("magicoder",                base_url_loc,   api_key_loc,   True,     3.8,      1,      False, "transformer",  ["Source Code"],         "pretrained",                  "Focuses on automating routine coding tasks."),
            #
            ("mistral",                  base_url_loc,   api_key_loc,   True,     4.1,      1,      False, "transformer",  ["General Text"],        "pretrained",             "General-purpose NLP model for a variety of text processing tasks."),
            # Timeouts: normalize frozen @0.4
            ("mistral:instruct",           base_url_loc,   api_key_loc,   True,     4.1,      7.2,    False, "transformer",  ["General Text"],        "pretrained",             "General-purpose NLP model for a variety of text processing tasks."),
            ("mistral-openorca",         base_url_loc,   api_key_loc,   True,     4.1,      1,      False, "transformer",  ["Open Data"],           "pretrained",              "Capable of handling diverse datasets for open-ended tasks."),
            ("mistrallite",              base_url_loc,   api_key_loc,   True,     4.1,      1,      False, "transformer",  ["Lite Tasks"],          "pretrained",         "Lighter version of Mistral for less resource-intensive tasks."),
            ("mixtral",                  base_url_loc,   api_key_loc,   True,     26.0,     2,    True,  "transformer",  ["Mixed Data"],          "pretrained",        "High-capacity model designed for complex data processing tasks."),
            ("mixtral:instruct",                  base_url_loc,   api_key_loc,   True,     26.0,     2,    True,  "transformer",  ["Mixed Data"],          "pretrained",        "High-capacity model designed for complex data processing tasks."),
            # normalize @ 0.5
            ("moondream",                base_url_loc,   api_key_loc,   True,     1.7,      1,    False, "transformer",  ["Dream Analysis"],      "pretrained",          "Specialized in modeling and interpreting dream content."),
            ("mxbai-embed-large",        base_url_loc,   api_key_loc,   True,     0.669,    1,    False, "transformer",  ["Embeddings"],          "embedded",               "Focused on creating and using large-scale text embeddings."),
            ("neural-chat",              base_url_loc,   api_key_loc,   True,     4.1,      1,    False, "transformer",  ["Chat Data"],           "pretrained",                 "Designed to simulate conversational dynamics for chatbots."),
            ("nexusraven",               base_url_loc,   api_key_loc,   True,     7.4,      2,    True,  "transformer",  ["Complex NLP Tasks"],   "pretrained",            "Advanced NLP model for complex language understanding and generation."),
            ("nomic-embed-text",         base_url_loc,   api_key_loc,   True,     0.274,    1,    False, "transformer",  ["Text Embedding"],      "embedded",               "Efficient at producing text embeddings for various applications."),
            ("notux",                    base_url_loc,   api_key_loc,   True,     26,       47,    True,  "transformer",  ["High-Capacity Tasks"], "pretrained",    "Designed for computational tasks requiring extensive resources."),
            ("open-orca-platypus2",      base_url_loc,   api_key_loc,   True,     7.4,      2,    True,  "orca",         ["Diverse Datasets"],    "pretrained",         "Handles complex data processing tasks across various domains."),
            ("openchat",                 base_url_loc,   api_key_loc,   True,     4.1,      1,    False, "transformer",  ["Chat Applications"],   "pretrained",         "Optimized for building interactive chat interfaces."),
            ("openhermes:latest",        base_url_loc,   api_key_loc,   True,     4.1,      7.0,  4,     "transformer",  ["Chat Applications"],   "pretrained",         "Optimized for building interactive chat interfaces."),
            ("phi3",                     base_url_loc,   api_key_loc,   True,     2.3,      1,    False, "transformer",  ["Educational Content"], "pretrained",               "Designed to support and enhance educational applications."),
            ("phind-codellama",          base_url_loc,   api_key_loc,   True,     19.0,     2,    True,  "llama",        ["Coding Challenges"],   "pretrained",         "Excels in solving complex coding problems and challenges."),
            ("solar",                    base_url_loc,   api_key_loc,   True,     6.1,      1,    False, "transformer",  ["Solar Data"],          "pretrained",      "Used for predictive modeling in solar energy systems."),
            ("stable-code",              base_url_loc,   api_key_loc,   True,     1.6,      1,    False, "transformer",  ["Stable Systems"],      "pretrained",        "Ensures stability in automated systems."),
            ("starcoder2:15b",           base_url_loc,   api_key_loc,   True,     9.1,      16,    True,  "transformer",  ["Next-gen Coding"],     "pretrained",     "Advanced model for next-generation code development."),
            ("starcoder2:instruct",           base_url_loc,   api_key_loc,   True,     9.1,      16,    True,  "transformer",  ["Next-gen Coding"],     "pretrained",     "Advanced model for next-generation code development."),
            # Timeouts: pass content @0.0 just from the start
            ("starling-lm",              base_url_loc,   api_key_loc,   True,     4.1,      1,    False, "transformer",  ["Language Data"],       "pretrained",       "Specializes in language modeling for various applications."),
            ("tinydolphin",              base_url_loc,   api_key_loc,   True,     0.636,    1,    False, "transformer",  ["Quick Tasks"],         "pretrained",          "Rapid analysis and response for on-the-go tasks."),
            ("tinyllama",                base_url_loc,   api_key_loc,   True,     0.637,    1,    False, "transformer",  ["Small Tasks"],         "pretrained",              "Efficient processing for small-scale tasks."),
            ("wizard-math",              base_url_loc,   api_key_loc,   True,     4.1,      1,    False, "transformer",  ["Math Problems"],       "pretrained",   "Specializes in solving complex mathematical problems."),
            ("wizard-vicuna-uncensored", base_url_loc,   api_key_loc,   True,     3.8,      1,    False, "transformer",  ["Uncensored Content"],  "pretrained",      "Handles and moderates uncensored content effectively."),
            ("wizardcoder:latest",       base_url_loc,   api_key_loc,   True,     3.8,      7.0,  4,     "llama",        ["Elite Coding"],        "pretrained",      "Top-tier model for elite coding tasks and algorithms."),
            # Timeouts: normalize @0.0 just from the start
            ("wizardcoder:34b-python-q8_0",base_url_loc,   api_key_loc,   True, 35.0,     2,    True,  "transformer",   ["Elite Coding"],        "pretrained",      "Top-tier model for elite coding tasks and algorithms."),
            ("wizardlm2",                base_url_loc,   api_key_loc,   True,     4.1,      1,    False, "transformer",  ["Broad NLP"],           "pretrained",             "Versatile NLP capabilities for broad applications."),
            ("xwinlm",                   base_url_loc,   api_key_loc,   True,     3.8,      1,    False, "transformer",  ["Cross-window Learning"],"pretrained",         "Facilitates learning across multiple data windows."),
            ("yi",                       base_url_loc,   api_key_loc,   True,     3.5,      1,    False, "transformer",  ["General AI"],          "pretrained",      "General-purpose AI for a wide range of tasks."),
            ("zephyr",                   base_url_loc,   api_key_loc,   True,     4.1,      1,    False, "transformer",  ["Light Applications"],  "pretrained",    "Optimized for real-time processing in lightweight applications.")
        ]

        for info in models_info:
            self.add_model(*info)

    def get_model_byname(self, model_name) -> LlmDto:
        for model in self.llms:
            if model.name == model_name:
                return model.copy()
        raise ValueError(f"Model named {model_name} not found")

    def get_models_bymodeltype(self, model_type: str) -> [LlmDto]:
        return [model.copy() for model in self.llms if model_type.lower() == getattr(model, 'get_model_type')().lower()]

    def get_all_models(self) -> [LlmDto]:
        return [model.copy() for model in self.llms]


