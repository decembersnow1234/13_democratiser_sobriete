import ollama


def open_file(text_path: str) -> str:
    with open(text_path, "r") as f:
        txt = f.read()
    
    return txt

def ollama_available(model_name: str) -> bool:
    models = ollama.list().get("models", [])
    return any(model["model"] == model_name for model in models)
