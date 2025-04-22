# filename: run_vllm_inference.py

from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

# --- Load tokenizer (for chat template and eos token) ---
tokenizer = AutoTokenizer.from_pretrained('mistral/<model-name>')

# --- Prepare chat messages ---
messages = [
    {"role": "user", "content": "Hello, who are you?"}
]

# --- Apply chat template to create the full prompt ---
prompt = tokenizer.apply_chat_template(messages, tokenize=False)

# --- Initialize vLLM model ---
llm = LLM(model="mistral/<model-name>")

# --- Set sampling parameters (including stop tokens) ---
sampling_params = SamplingParams(
    stop=[tokenizer.eos_token],  # stop sequences are TEXT, not token IDs
    temperature=0.7,             # optional, can be adjusted
    top_p=0.9,                   # optional
    max_tokens=512               # optional
)

# --- Run generation ---
outputs = llm.generate([prompt], sampling_params=sampling_params)

# --- Print output ---
for output in outputs:
    print("Generated Text:")
    print(output.outputs[0].text)
