from transformers import pipeline

moderation_pipeline = pipeline('text-classification', model='unitary/toxic-bert')


def is_toxic(text: str) -> bool:
    result = moderation_pipeline(text)
    for res in result:
        if res['label'] == 'toxic' and res['score'] > 0.5:
            return True
    return False
