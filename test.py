import requests
import json
import timeit
import re
import pandas as pd

# List of models to test
MODELS = [
    "llama3.1:8b-instruct-q4_0",
    "llama3.1:70b-instruct-q4_0",
    # "aya:35b-23-q4_K_M",
    # "mistral-small:22b-instruct-2409-q4_0",
    # "mixtral:8x7b-instruct-v0.1-q4_0"
]

# Context length
# num_ctx = 4000
num_ctx = 200

# Results dictionary
results = []

for MODEL in MODELS:
    # Start timer
    start = timeit.default_timer()

    # Prompt to generate text
    prompt = "С какой периодичностью происходит ледниковый период"

    # Make API request
    result = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': MODEL,
            "options": {
                "seed": 123,
                "num_predict": 500,
                "temperature": 0,
                "num_ctx": num_ctx
            },
            "keep_alive": 0,
            "prompt": prompt,
            "stream": False
        }
    ).content

    # Parse result
    a = json.loads(result)

    # Calculate duration in seconds
    nanoseconds = a['eval_duration']
    seconds = nanoseconds / 1_000_000_000

    # Stop time
    end = timeit.default_timer()

    # Detect quantization
    quantization = "q4_0"  # default quantization
    match = re.search(r'^(.*)-(q\d_.*|fp16)$', MODEL)
    if match:
        quantization = match[2]
        MODEL = match[1]

    results_dict = {
        'model': MODEL, 'quantization': quantization, 'context_length': num_ctx,
        'total_tokens': a['eval_count'], 'duration_s': seconds,
        'tokens_per_sec': a['eval_count'] / seconds, 'time_to_retrieve_s': end - start
    }
    # Print intermediate information
    print(results_dict)
    results.append(results_dict)

# df = pandas.DataFrame.from_dict(results, orient='index')
# print(df.to_markdown(index=False, tablefmt='fancy_grid'))

# Print results table
df = pd.DataFrame(results)  # .from_dict(results, orient='index')
print("\n------\n")
print(df.to_markdown(index=False))
