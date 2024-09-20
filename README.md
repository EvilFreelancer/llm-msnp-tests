# LLM MSNP Tests

A small and collection of results, if checks speed of GGUF model on different combination of GPUs and CPUs.  

Inspired due to conversation in Telegram chat.  

## MSNP Leaderboards

https://huggingface.co/spaces/evilfreelancer/msnp-leaderboard

## How to test

First you need to install [ollama](https://ollama.com/download) to server where you will make tests.

Then you need to create Python Virtual Environment, then chroot to it:

```shell
mkdir msnp-tests
cd msnp-tests
python3 -m venv venv
source venv/bin/activate
```

Then download tests.py file:

```shell
wget https://raw.githubusercontent.com/EvilFreelancer/llm-msnp-tests/refs/heads/main/test.py
```

And run it:

```shell
python3 test.py 
```

In result will be something like this:

![examples](./assets/example.png)
