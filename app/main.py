from fastapi import FastAPI, HTTPException
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.core.evaluator import Evaluator

app = FastAPI(
    title="LLM Evaluation Framework",
    description="API for evaluating LLM outputs based on customizable rules.",
    version="0.1.0"
)

evaluator = Evaluator()

@app.get("/")
def root():
    return {
        "message": "LLM Evaluation Framework",
        "status": "running",
        "version": "0.1.0"
    }

@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest):
    try:
        result = evaluator.evaluate(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "evaluator": "initialized",
        "rules_loaded": len(evaluator.rules)
    }
