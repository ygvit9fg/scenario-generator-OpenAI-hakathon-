from huggingface_hub import HfApi

api = HfApi()


models = api.list_models(filter="text-generation", sort="downloads", direction=-1, limit=20)

print("Доступные модели (топ-20 по популярности):")
for m in models:
    print(m.modelId)