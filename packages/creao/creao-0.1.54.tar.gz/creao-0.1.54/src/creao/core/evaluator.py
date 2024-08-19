from datasets import Dataset
from sentence_transformers.evaluation import (
    InformationRetrievalEvaluator,
    SequentialEvaluator,
)
from sentence_transformers.util import cos_sim
from creao.core.Diagnosis import RetrieverDiagnoser

class IREvaluator:
    def __init__(self, dataset: Dataset):
        # extract all unique chunk
        self.train_dataset = dataset["train"]
        self.test_dataset = dataset["test"]
        chunks = set()
        for item in self.test_dataset:
            chunks.add(item["positive"])
        for item in self.train_dataset:
            chunks.add(item["positive"])
        self.chunks = chunks
        print(f"Number of unique chunks: {len(chunks)}")
        question_list = []
        for item in self.test_dataset:
            question_list.append({"question":item["anchor"], "positive":item["positive"]})
        retriever_diagnoser = RetrieverDiagnoser(self.chunks, question_list)
        self.retriever_diagnoser = retriever_diagnoser
    def extract_retrieval_errors(self, rank_threshold:int=2):
        # list of dict with question, and positive chunk (ground truth)
        filtered_res = self.retriever_diagnoser.detect_retriever_error(rank_threshold=rank_threshold)
        return filtered_res


    def construct_information_retireval_evaluator(self):
        matryoshka_dimensions = [768, 512, 256, 128, 64]  # Important: large to small\
        # cheat a chunk to dictionary index
        chunk_to_index = {}
        i = 0
        for item in self.chunks:
            chunk_to_index[item] = i
            i += 1
        # constreuct index to chunk
        index_to_chunk = {v: k for k, v in chunk_to_index.items()}
        # test queries for information retrieval evaluation
        queries = dict(zip(self.test_dataset["id"], self.test_dataset["anchor"]))
        # relevant_docs:  Query ID to relevant documents (qid => set([relevant_cids])
        relevant_docs = {}

        for i in range(len(self.test_dataset)):
            chunk = self.test_dataset[i]["positive"]
            id = self.test_dataset[i]["id"]
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
    


