# Universal QA Assistant
### Benchmarking, Reliability, Offline AI, and Future Development Roadmap

**Project focus:** Generative AI · Large Language Models · RAG Evaluation · Local Inference · Model Benchmarking

**Current status:** Baseline evaluation completed; reliability improvements and offline migration planned.

---

## 1. Project Overview

The Universal QA Assistant is an AI-powered question-answering project designed to generate responses to user queries and evaluate the reliability, latency, and cost of LLM-based inference.

The current implementation uses Python, Streamlit, LangChain, Groq-hosted LLMs, Hugging Face embeddings, FAISS vector search, and LangSmith for tracing and experiment evaluation.

The current RAG implementation serves as an experimental baseline. Its purpose is to identify limitations in retrieval, answer generation, evidence grounding, and abstention before developing a more reliable and resource-efficient system.

The long-term objective is to develop a modular QA platform supporting:

- Local LLM inference using Ollama.
- Structured responses and validation using Pydantic.
- Automated evaluation of correctness, faithfulness, and hallucination-related failures.
- Intelligent model selection based on query complexity and resource constraints.
- Reproducible latency, token-usage, and resource benchmarks.
- An offline-capable deployment that can operate without a cloud LLM API.

**Important distinction:** The offline architecture, advanced routing, and several reliability improvements are planned enhancements. They should not be considered completed until implemented and tested.

---

## 2. Current Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Application and evaluation logic |
| Frontend | Streamlit | Chat interface and document interaction |
| LLM inference | Groq API | Cloud-hosted language-model responses |
| LLM orchestration | LangChain | Model and retrieval integration |
| Embeddings | Hugging Face Sentence Transformers | Text representation for semantic search |
| Vector search | FAISS | Similarity-based retrieval |
| Document input | PDF text extraction | Source-document ingestion |
| Experiment tracking | LangSmith | Tracing, latency inspection, and evaluation |
| Evaluation dataset | LangSmith dataset | Repeatable question-and-answer tests |

FastAPI, Pydantic response contracts, Ollama inference, and automated offline benchmarking are proposed extensions unless separately implemented in the project.

---

## 3. Initial Benchmark Results

The first recorded experiment was:

**Experiment:** `wttc-rag-baseline-v1-795f9fe7`

**Dataset:** WTTC Introduction to AI PDF evaluation set

**Number of evaluated questions:** 16

### 3.1 Performance measurements

| Metric | Recorded value |
|---|---:|
| Questions evaluated | 16 |
| Reported p50 latency | 6.02 seconds |
| Total tokens | 21,783 |
| Input tokens | 17,086 |
| Output tokens | 4,697 |
| Displayed total cost | $0.0054 |
| Displayed input cost | $0.0025 |
| Displayed output cost | $0.0029 |
| Reference-match evaluator average | 0.00 |
| Correct-abstention evaluator average | 0.50 |

The cost figures are rounded values displayed by LangSmith. They represent the recorded experiment, not a guaranteed cost for future requests.

### 3.2 Token distribution

Input tokens accounted for approximately **78.43%** of total token usage.

Output tokens accounted for approximately **21.57%**.

This suggests that prompt content, document context, and retrieved passages deserve investigation as potential sources of token overhead. However, these percentages alone do not establish that input tokens are unnecessarily high.

### 3.3 Approximate cost per question

Using the displayed total cost:

`$0.0054 / 16 = $0.0003375 per question`

This is an approximate benchmark average based on the reported total. Actual cost will vary with the model, prompt length, retrieved context, answer length, and provider pricing.

### 3.4 How to interpret these results

The reported p50 of 6.02 seconds is the median latency, not the average and not the maximum. A p95 latency measurement is needed to understand slower requests.

The reference-match score of 0.00 does not prove that every generated answer is incorrect. The current evaluator relies on lexical matching and can reject semantically correct paraphrases.

The correct-abstention score of 0.50 suggests inconsistent performance on the abstention cases evaluated. Its interpretation depends on how many examples were scored by that evaluator.

These results establish an initial experimental baseline. They do not establish a verified overall accuracy, hallucination rate, or improvement percentage.

---

## 4. Observed Limitations

### 4.1 Unsupported answers and hallucinations

One evaluated question asked when the WTTC Staff Shortages report was published. The expected behavior was to acknowledge that the PDF did not provide the publication month.

Instead, the model answered November 2022 and cited a PDF page.

This demonstrates a critical failure mode: a fluent answer can contain an unsupported claim and an unreliable citation.

**Planned improvements:**

- Require answers to be grounded in retrieved evidence.
- Validate source metadata and page references.
- Add explicit abstention behavior.
- Evaluate factual claims against verified reference answers.
- Test questions whose answers are deliberately absent from the document.

### 4.2 Retrieval and generation failures are not separated sufficiently

A wrong answer can originate from several stages:

1. The relevant passage was not retrieved.
2. The correct passage was retrieved but ignored.
3. The prompt permitted unsupported inference.
4. The generated answer contained an incorrect citation.
5. The evaluation method incorrectly scored a valid paraphrase.

The next iteration must inspect retrieval results and generated answers separately.

### 4.3 Small evaluation dataset

The current benchmark contains 16 questions. This is sufficient for an initial diagnostic experiment, but not for broad claims about general-purpose QA performance.

The next evaluation set should include direct factual questions, exact lookups, multi-part questions, ambiguous questions, general-chat questions, and unanswerable questions.

### 4.4 Limited evaluation metrics

The current reference-match and abstention checks do not provide a comprehensive measurement of correctness, grounding, retrieval quality, or security.

The project needs additional metrics and manual verification.

### 4.5 Cloud dependency

The current Groq-based inference path depends on an external service and network connectivity.

This limits fully offline operation and means that inference depends on provider availability, account configuration, and applicable rate limits.

### 4.6 Resource and deployment constraints

Local models require sufficient RAM, storage, and compute resources. A model that runs acceptably on one machine may be slow or unusable on another.

Offline deployment must account for model downloads, dependency installation, model loading, and the availability of the required assets without internet access.

---

## 5. Advantages and Disadvantages of the Current System

### Advantages

- Rapid development using existing Python and LangChain components.
- Cloud-hosted inference avoids the need to run a large LLM locally.
- FAISS supports semantic document retrieval.
- LangSmith provides experiment tracing and visibility into model execution.
- The existing application offers a foundation for systematic evaluation.
- Modular components can be reused in future offline and API-based implementations.

### Disadvantages

- Cloud inference requires connectivity and may incur API charges.
- Retrieval can return irrelevant or incomplete passages.
- The model may invent information absent from the source document.
- Current evaluator scores do not establish reliable overall accuracy.
- Prompt and retrieved-context tokens contribute to total inference usage.
- Fully offline operation is not yet established.
- The current benchmark does not demonstrate a measured improvement over an alternative model or architecture.

---

## 6. Proposed Evaluation Framework

The next major development task is an evaluation harness: a repeatable testing system that executes the same questions against different configurations and compares the resulting metrics.

### 6.1 Evaluation dataset

Start with 50–100 manually verified questions drawn from representative documents.

Each record should include:

- Question.
- Expected answer.
- Relevant document and page.
- Relevant chunk identifiers, where available.
- Question category.
- Expected behavior: answer, clarify, general chat, or abstain.

The dataset should include examples where the correct response is that the document does not provide enough information.

### 6.2 Retrieval metrics

| Metric | Purpose |
|---|---|
| Recall@K | Measures whether relevant evidence appears in the top K retrieved results |
| Precision@K | Measures the relevance of retrieved results |
| MRR | Measures how highly the first relevant result is ranked |
| nDCG@K | Evaluates ranking quality when relevance varies across passages |

These metrics require verified relevance labels for the test questions.

### 6.3 Answer-quality metrics

| Metric | Purpose |
|---|---|
| Answer correctness | Measures agreement with a verified reference answer or rubric |
| Faithfulness | Measures whether factual claims are supported by retrieved context |
| Citation accuracy | Checks whether cited source pages support the associated claims |
| Completeness | Measures whether all required parts of an answer are covered |
| Abstention accuracy | Measures whether unanswerable questions are appropriately declined |
| Unnecessary abstention rate | Measures how often the system declines questions it could answer |

BLEU and ROUGE may be included as supplementary text-overlap metrics. They should not be treated as sufficient measures of factual correctness.

Automated LLM judging should be validated against manually reviewed examples rather than treated as unquestionable ground truth.

### 6.4 Latency and resource metrics

Track:

- End-to-end p50 latency.
- End-to-end p95 latency.
- Retrieval latency.
- Generation latency.
- Validation and routing latency.
- Model-loading time.
- Peak RAM usage.
- Total input and output tokens for cloud inference.
- API cost per experiment and per question.

LangSmith can help trace supported model calls and their timings. Explicit application-level timers are still needed to measure complete request latency and local resource usage.

---

## 7. Proposed Structured Response Architecture

Pydantic should be used to define and validate consistent API response structures.

A future response may contain:

- `action`: ANSWER, CLARIFY, GENERAL_CHAT, or ABSTAIN.
- `answer`: the generated response, where appropriate.
- `clarification_question`: a question for the user when necessary.
- `sources`: validated document references.
- `model_used`: the model selected for inference.
- `metrics`: stage-level latency measurements.

Pydantic validation ensures that fields and types satisfy the declared schema. It does not establish factual correctness or prove that citations support the answer. Those checks require additional validation logic.

FastAPI is a planned interface for exposing this functionality through REST endpoints, while Streamlit can remain the user-facing interface.

---

## 8. Clarification and Question Routing

The assistant should not always generate an answer immediately.

The proposed routing behavior is:

### ANSWER
Use this when the question is sufficiently clear and relevant evidence is available.

### CLARIFY
Ask a targeted question when an important piece of user intent is missing.

For example, if the user asks which option is best, the assistant may ask whether the priority is cost, eligibility, or career prospects.

### GENERAL_CHAT
Handle questions that do not require document retrieval.

### ABSTAIN
Decline to provide a document-grounded answer when evidence is insufficient.

Evaluation should measure correct routing, unnecessary clarification, correct abstention, and final answer quality after clarification.

---

## 9. Offline Inference with Ollama

A major planned enhancement is local LLM inference through Ollama.

The objective is to provide a QA assistant that can operate without sending prompts to a cloud LLM API.

### Proposed architecture

The model interface should allow the application to use different providers while keeping the rest of the QA pipeline consistent.

Potential configurations include:

- A small local model for lower-latency, simpler questions.
- A larger local model for questions requiring more detailed reasoning.
- An optional cloud provider for deployments that permit external inference.

Model selection must be based on measured answer quality, latency, memory usage, and hardware constraints.

### Offline requirements

For genuine offline operation, the following must be available locally:

- Ollama and the selected LLM weights.
- Required Python packages and dependencies.
- Embedding model weights.
- Vector index and source documents.
- Any local reranker or supporting model assets.
- Application configuration and validation logic.

A successful offline test must be performed with internet connectivity disabled after all required assets have been provisioned.

Local inference removes per-request cloud LLM API charges but does not eliminate hardware, energy, maintenance, or storage costs.

---

## 10. Future Model Comparison and Routing

The project will eventually compare multiple local models using the same evaluation dataset.

For each model, the report should include:

- Answer correctness.
- Faithfulness.
- Correct abstention.
- p50 and p95 latency.
- Peak memory usage.
- Model-loading time.
- Tokens processed, where comparable.
- Cloud API cost, where applicable.

A model router may then select a model based on query category, expected complexity, and a latency budget.

The router should not assume that a smaller model is always faster or that a larger model is always more accurate. These are hypotheses to test on the target hardware and workload.

The first implementation should use a small, configurable model registry. More sophisticated routing can be added after enough evaluation data is available.

---

## 11. Advanced Retrieval — Future Work

Hybrid retrieval and reranking are intentionally deferred until the current semantic-retrieval baseline has been evaluated properly.

Potential future experiments include:

1. Combine dense semantic retrieval with BM25 keyword retrieval.
2. Merge ranked results using Reciprocal Rank Fusion.
3. Apply a cross-encoder reranker to select the strongest candidate passages.
4. Compare chunk size, overlap, metadata, and context-window settings.
5. Evaluate parent-child retrieval for questions requiring broader context.

Each change should be tested against the same dataset and measured using retrieval and answer-quality metrics.

The goal is not to add complexity for its own sake, but to demonstrate that a specific change improves a measurable weakness.

---

## 12. Fine-Tuning with LoRA or QLoRA

Fine-tuning is a later-stage option, not an immediate requirement.

RAG and fine-tuning solve different problems:

- RAG provides external evidence for answers.
- LoRA adapts a model using trainable low-rank parameter updates.
- QLoRA reduces fine-tuning memory requirements by using a quantized base model alongside trainable adapters.

Fine-tuning may be considered if the evaluation demonstrates recurring issues with response behavior, specialized terminology, or formatting that cannot be adequately addressed through prompting and model selection.

It should not be assumed to improve document retrieval automatically.

Any fine-tuned model must be evaluated against the same baseline to verify that it improves the intended behavior without unacceptable regressions.

---

## 13. Security and Reliability

Security testing should be part of the evaluation harness.

Important test categories include:

- Direct prompt injection.
- Indirect prompt injection embedded in test documents.
- Attempts to reveal system instructions.
- Unauthorized document access.
- Malformed or excessively long requests.
- Fabricated or unsupported citations.
- Unanswerable questions.
- Validation failures in structured responses.

Retrieved documents must be treated as untrusted data rather than instructions that override the application's rules.

Use a separate test vector store for deliberately poisoned documents. Never introduce adversarial content into the production index merely to test a failure.

Security tests should evaluate actual behavior and access controls. Passing a few prompt-injection examples does not prove that the system is secure.

---

## 14. Development Roadmap

### Phase 1 — Establish a trustworthy baseline
- Verify the current dataset and reference answers.
- Review the 16 existing experiment traces.
- Manually label correctness and grounding failures.
- Add a larger, balanced evaluation dataset.
- Record retrieval results and end-to-end latency.

### Phase 2 — Improve grounding and validation
- Revise the RAG prompt.
- Validate citation metadata.
- Add structured response schemas.
- Implement answer, clarify, general-chat, and abstain actions.
- Add repeatable automated evaluations.

### Phase 3 — Build local inference
- Integrate Ollama through a common model interface.
- Select an initial lightweight model.
- Verify offline operation after provisioning dependencies and model assets.
- Measure local latency and resource consumption.

### Phase 4 — Compare configurations
- Run identical test questions through cloud and local models.
- Compare correctness, faithfulness, abstention, and latency.
- Evaluate routing strategies.
- Document measured trade-offs.

### Phase 5 — Advanced retrieval
- Experiment with hybrid retrieval and reranking.
- Measure improvements against the established baseline.
- Keep changes only when results justify their additional complexity.

### Phase 6 — Optional fine-tuning and deployment
- Investigate LoRA or QLoRA if evaluation identifies a specific need.
- Package the application and required local assets.
- Test installation and execution on a clean, compatible machine.
- Document hardware requirements and known limitations.

---

## 15. How Performance Improvements Will Be Reported

No percentage improvement should be claimed until a comparable experiment has been completed.

Latency reduction will be calculated as:

`Latency reduction (%) = ((Baseline latency - New latency) / Baseline latency) × 100`

For a fair comparison, use the same questions and report p50 and p95 latency separately.

Token reduction will be calculated as:

`Token reduction (%) = ((Baseline tokens - New tokens) / Baseline tokens) × 100`

Compare token counts only when the measurements are defined consistently.

For answer quality, report the absolute percentage-point change in correctness or faithfulness, along with the number of test cases and evaluation method.

For example, moving from 60% correctness to 75% correctness is an improvement of 15 percentage points, equivalent to a 25% relative increase. These are illustrative calculations, not results achieved by this project.

---

## 16. Current Status Summary

### Measured
- Initial 16-question LangSmith evaluation.
- Reported p50 latency of 6.02 seconds.
- Total token usage of 21,783.
- Displayed experiment cost of $0.0054.
- Initial reference-match and correct-abstention evaluator scores.

### Identified limitations
- Unsupported answers and potentially unreliable citations.
- Evaluation metrics that do not establish overall correctness.
- Limited dataset coverage.
- No verified cloud-versus-local performance comparison.

### Planned
- Improved grounding and abstention.
- Pydantic-based structured responses.
- A reproducible evaluation harness.
- Offline inference with Ollama.
- Comparative model benchmarking.
- Intelligent routing.
- Advanced retrieval and optional fine-tuning.

## Conclusion

The project is evolving from a basic document-question-answering prototype toward a measurable, reliable, and offline-capable AI assistant.

Its strongest engineering contribution will be a reproducible evaluation framework that demonstrates how retrieval, model choice, structured validation, and routing affect answer quality and performance.

The next priority is to establish trustworthy correctness and grounding measurements before introducing additional architectural complexity. That baseline will guide future development and ensure that claimed improvements are supported by experimental evidence.