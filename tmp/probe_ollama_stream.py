import json
import time
import urllib.request


payload = json.dumps(
    {
        "model": "qwen3:4b-instruct",
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly: MODEL STREAM OK",
            }
        ],
        "stream": True,
        "think": False,
        "options": {"num_predict": 32},
    }
).encode("utf-8")
request = urllib.request.Request(
    "http://127.0.0.1:11434/api/chat",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

started = time.perf_counter()
first_visible = None
visible_chunks = []
with urllib.request.urlopen(request, timeout=120) as response:
    for raw_line in response:
        event = json.loads(raw_line)
        text = event.get("message", {}).get("content", "")
        if text:
            if first_visible is None:
                first_visible = time.perf_counter() - started
            visible_chunks.append(text)
        if event.get("done"):
            break

elapsed = time.perf_counter() - started
print(
    json.dumps(
        {
            "first_visible_seconds": round(first_visible or elapsed, 3),
            "total_seconds": round(elapsed, 3),
            "chunk_count": len(visible_chunks),
            "response": "".join(visible_chunks),
        }
    )
)
