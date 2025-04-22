# filename: run_vllm_from_base.py

from vllm import LLM, SamplingParams
from vllm.utils import get_chat_template

# --- Initialize vLLM model from local folder ---
llm = LLM(model="/path/to/your/BASE")   # <- point to your BASE model

# --- Access the model's chat template ---
chat_template = get_chat_template(llm.llm_engine.tokenizer)

# --- Define your chat messages ---
messages = [
    {"role": "user", "content": "Hello, who are you?"}
]

# --- Apply chat template to create prompt ---
prompt = chat_template.apply_chat_template(messages, tokenize=False)

# --- Set sampling parameters ---
sampling_params = SamplingParams(
    stop=["<|eos|>"],    # or whatever your BASE model uses
    temperature=0.7,
    top_p=0.9,
    max_tokens=512
)

# --- Generate ---
outputs = llm.generate([prompt], sampling_params=sampling_params)

# --- Print output ---
for output in outputs:
    print("Generated Text:")
    print(output.outputs[0].text)
