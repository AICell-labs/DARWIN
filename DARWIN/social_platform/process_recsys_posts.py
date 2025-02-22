#
#
from typing import List

import torch
from transformers import AutoModel, AutoTokenizer


# Function: Process each batch
@torch.no_grad()
def process_batch(model: AutoModel, tokenizer: AutoTokenizer,
                  batch_texts: List[str]):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = tokenizer(batch_texts,
                       return_tensors="pt",
                       padding=True,
                       truncation=True)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    outputs = model(**inputs)
    return outputs.pooler_output


def generate_post_vector(model: AutoModel, tokenizer: AutoTokenizer, texts,
                         batch_size):
    # Loop through all messages
    # If the list of messages is too large, process them in batches.
    all_outputs = []
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_outputs = process_batch(model, tokenizer, batch_texts)
        all_outputs.append(batch_outputs)
    all_outputs_tensor = torch.cat(all_outputs, dim=0)  # num_posts x dimension
    return all_outputs_tensor.cpu()


if __name__ == "__main__":
    # Input list of strings (assuming there are tens of thousands of messages)
    # Here, the same message is repeated 10000 times as an example
    texts = ["I'm using TwHIN-BERT! #TwHIN-BERT #NLP"] * 10000
    # Define batch size
    batch_size = 100
    all_outputs_tensor = generate_post_vector(texts, batch_size)
    print(all_outputs_tensor.shape)
