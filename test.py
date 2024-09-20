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
result = requests.post(
    'http://gpu02:11434/api/generate',
    json={
        'model': MODEL,
        "options": {
            "seed": 123,
            "num_predict": 500,
            "temperature": 0,
            "num_ctx": num_ctx
        },
        "keep_alive": "10m", "prompt": prompt,
        "stream": False
    }
).content
a = json.loads(result)
nanoseconds = a['eval_duration']  # 5 billion nanoseconds
seconds = nanoseconds / 1_000_000_000
end = timeit.default_timer()

print(a['response'])
print()
print(f"Модель: {MODEL}")
print(f"Размер контекста: {num_ctx}")
print(f"Всего токенов: {a['eval_count']}")
print(f"Длительность: {seconds}")
print(f"Токенов в секунду: {a['eval_count'] / seconds}")
print(f"Время до получения ответа: {end - start}")
