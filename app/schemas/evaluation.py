from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class EvaluationRequest(BaseModel):
    task_type: Optional[str] = Field(
        None,
        description="type of task: 'qa', 'reasoning', 'summarization', etc.",
        example="qa"
    )

    prompt: Optional[str] = Field(
        None,
        description="original prompt given to the LLM",
        example="What is the capital of France?"
    )

    output: str = Field(
        ...,
        description="LLM's generated output to evaluate",
        example="The capital of France is Paris."
    )

    reference: Optional[str] = Field(
        None,
        description="ground truth or reference answer for comparison",
        example="Paris"
    )

    meta: Optional[Dict[str, Any]] = Field(
        None,
        description="metadata like model name, temperature, etc.",
        example={"model": "gpt-4", "temperature": 0.7}
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "task_type": "qa",
                "prompt": "What is the capital of France?",
                "output": "The capital of France is Paris.",
                "reference": "Paris",
                "meta": {"model": "gpt-4", "temperature": 0.7}
            }
        }
    )


class RuleResult(BaseModel):
    rule_id: str = Field(description="unique identifier for the evaluation rule")
    rule_name: str = Field(description="human readable name of the evaluation rule")
    passed: bool = Field(description="whether the output passed this rule")
    score: float = Field(..., ge=0.0, le=1.0, description="score for this rule between 0 and 1")
    explanation: str = Field(description="why the output passed or failed this rule")


class EvaluationResponse(BaseModel):
    evaluation_id: str = Field(..., description="unique ID for this evaluation")
    timestamp: datetime = Field(..., description="when evaluation was performed")

    scores: Dict[str, float] = Field(
        ...,
        description="scores for each evaluation dimension",
        example={
            "format_score": 1.0,
            "instruction_score": 0.8,
            "hallucination_score": 0.3
        }
    )

    overall_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="weighted overall reliability score"
    )

    failure_labels: List[str] = Field(
        default_factory=list,
        description="list of detected failure modes",
        example=["hallucination", "format_violation"]
    )

    explanations: Dict[str, str] = Field(
        default_factory=dict,
        description="explanations for each failure",
        example={
            "hallucination": "output contains unsupported facts"
        }
    )

    rule_results: List[RuleResult] = Field(
        default_factory=list,
        description="detailed results from each rule"
    )

    input_data: EvaluationRequest = Field(
        ...,
        description="original input that was evaluated"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "evaluation_id": "eval_123abc",
                "timestamp": "2024-10-01T12:34:56Z",
                "scores": {
                    "format_score": 1.0,
                    "instruction_score": 0.8,
                    "hallucination_score": 0.3
                },
                "overall_score": 0.7,
                "failure_labels": ["hallucination", "format_violation"],
                "explanations": {
                    "hallucination": "output contains unsupported facts"
                },
                "rule_results": [
                    {
                        "rule_id": "rule_001",
                        "rule_name": "Format Check",
                        "passed": True,
                        "score": 1.0,
                        "explanation": "Output matches the required format."
                    },
                    {
                        "rule_id": "rule_002",
                        "rule_name": "Hallucination Check",
                        "passed": False,
                        "score": 0.0,
                        "explanation": "Output contains unsupported facts."
                    }
                ],
                "input_data": {
                    "output": "The capital of France is Paris."
                }
            }
        }
    )
