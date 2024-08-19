from datasets import Dataset
from sentence_transformers.evaluation import (
    InformationRetrievalEvaluator,
    SequentialEvaluator,
)
from sentence_transformers.util import cos_sim

def construct_information_retireval_evaluator(dataset: Dataset):
    matryoshka_dimensions = [768, 512, 256, 128, 64]  # Important: large to small\
    train_dataset = dataset["train"]
    test_dataset = dataset["test"]
    # extract all unique chunk
    chunk = set()
    for item in test_dataset:
        chunk.update(item["positive"])
    for item in train_dataset:
        chunk.update(item["positive"])
    print(f"Number of unique chunks: {len(chunk)}")
    # cheat a chunk to dictionary index
    chunk_to_index = {}
    i = 0
    for item in chunk:
        chunk_to_index[item] = i
        i += 1
    # constreuct index to chunk
    index_to_chunk = {v: k for k, v in chunk_to_index.items()}
    # test queries for information retrieval evaluation
    queries = dict(zip(test_dataset["id"], test_dataset["anchor"]))
    # relevant_docs:  Query ID to relevant documents (qid => set([relevant_cids])
    relevant_docs = {}

    for i in range(len(test_dataset)):
        chunk = test_dataset[i]["positive"]
        id = test_dataset[i]["id"]
        relevant_docs[id] = [chunk_to_index[chunk]]

    matryoshka_evaluators = []
    # Iterate over the different dimensions
    for dim in matryoshka_dimensions:
        ir_evaluator = InformationRetrievalEvaluator(
            queries=queries,
            corpus=index_to_chunk,
            relevant_docs=relevant_docs,
            name=f"dim_{dim}",
            truncate_dim=dim,  # Truncate the embeddings to a certain dimension
            score_functions={"cosine": cos_sim},
            write_csv=True
        )
        matryoshka_evaluators.append(ir_evaluator)

    # Create a sequential evaluator
    evaluator = SequentialEvaluator(matryoshka_evaluators)
    return evaluator
    


