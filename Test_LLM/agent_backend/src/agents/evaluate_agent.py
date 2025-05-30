from typing import Callable, List, Optional
from dataclasses import dataclass
from dataclasses import asdict
import numpy as np
import mlflow
from mlflow.types.llm import ChatMessage, ChatParams, ChatChoice

import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure required NLTK packages are downloaded
nltk.download("punkt")

@dataclass
class TestCase:
    question: str
    expected_sql: str
    expected_answer_substr: str
    expected_answer_text: str

@dataclass
class EvaluationResult:
    question: str
    agent_answer: str
    expected_answer: str
    contains_expected: bool
    bleu_score: float
    semantic_similarity: float

def bleu_score(ref: str, hyp: str) -> float:
    ref_tokens = nltk.word_tokenize(ref.lower())
    hyp_tokens = nltk.word_tokenize(hyp.lower())
    return sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=SmoothingFunction().method1)

def semantic_similarity(ref: str, hyp: str) -> float:
    vectorizer = TfidfVectorizer().fit([ref, hyp])
    vectors = vectorizer.transform([ref, hyp])
    sim = cosine_similarity(vectors[0], vectors[1])[0][0]
    return sim

def evaluate_agent_on_test_case(
    agent_fn: Callable,
    test_case: TestCase,
    messages: Optional[List[ChatMessage]] = None,
    params=None,
    verbose: bool = False
) -> EvaluationResult:
    input_messages = messages or [ChatMessage(role="user", content=test_case.question)]
    result = agent_fn(messages=input_messages, params=params, verbose=verbose)
    agent_answer = result["choices"][0]["message"]["content"]

    contains_expected = test_case.expected_answer_substr.lower() in agent_answer.lower()
    bleu = bleu_score(test_case.expected_answer_text, agent_answer)
    semantic = semantic_similarity(test_case.expected_answer_text, agent_answer)

    if verbose:
        print("Agent Answer:", agent_answer)
        print("Expected Substring:", test_case.expected_answer_substr)
        print("Expected Answer:", test_case.expected_answer_text)
        print("BLEU Score:", bleu)
        print("Semantic Similarity:", semantic)

    evaluation = EvaluationResult(
        question=test_case.question,
        agent_answer=agent_answer,
        expected_answer=test_case.expected_answer_text,
        contains_expected=contains_expected,
        bleu_score=bleu,
        semantic_similarity=semantic,
    )

    with mlflow.start_run(nested=True):  # optional: `run_name="evaluation"`
        mlflow.log_metrics({
            "bleu_score": bleu,
            "semantic_similarity": semantic,
        })
        mlflow.log_dict(asdict(evaluation), "agent_output.json")

    return evaluation

    
