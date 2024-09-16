import requests
import json
import timeit

MODEL = "llama3.1:8b"
# MODEL = "llama3.1:8b-instruct-fp16"
# MODEL = "llama3.1:70b"
# MODEL = "aya:35b-23-q4_K_M"

# num_ctx = 200
num_ctx = 4000

start = timeit.default_timer()
prompt = "С какой периодичностью происходит ледниковый период"
result = requests.post('http://localhost:11434/api/generate', json={'model': MODEL, "options":{ "seed": 123,"num_predict":500,"temperature": 0,"num_ctx": 4000}, "keep_alive":"10m", "prompt":prompt, "stream": False}).content
a = json.loads(result)

print(a['response'])
print("Всего токенов: ", a['eval_count'])

nanoseconds = a['eval_duration']  # 5 billion nanoseconds

seconds = nanoseconds / 1_000_000_000

print("Длительность: ", seconds)  # Output: 5.0
print("T/s - ", a['eval_count'] / seconds)

end = timeit.default_timer()
print(f"Time to retrieve response: {end - start}")
