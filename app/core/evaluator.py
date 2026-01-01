from app.schemas.evaluation import EvaluationRequest, EvaluationResponse, RuleResult
from datetime import datetime
import uuid
from typing import Dict, List

class Evaluator:

    def __init__(self):
        self.rules = []

    def evaluate(self, request: EvaluationRequest) -> EvaluationResponse:
        eval_id = f"eval_{uuid.uuid4().hex[:12]}"

        rule_results = self._run_rules(request)

        scores = self._aggregate_scores(rule_results)

        overall_score = self._calculate_overall_score(scores)

        failure_labels = self._identify_failures(rule_results)

        explanations = self._generate_explanations(rule_results, failure_labels)

        response = EvaluationResponse(
            evaluation_id=eval_id,
            timestamp=datetime.utcnow(),
            scores=scores,
            overall_score=overall_score,
            failure_labels=failure_labels,
            explanations=explanations,
            rule_results=rule_results,
            input_data=request
        )

        return response

    def _run_rules(self, request: EvaluationRequest) -> List[RuleResult]:
        output = request.output
        is_empty = len(output.strip()) == 0

        dummy_rule = RuleResult(
            rule_id="check_empty_output",
            rule_name="empty output detection",
            passed=not is_empty,
            score=0.0 if is_empty else 1.0,
            explanation="output is empty" if is_empty else "output contains text"
        )

        return [dummy_rule]

    def _aggregate_scores(self, rule_results: List[RuleResult]) -> Dict[str, float]:
        format_score = rule_results[0].score if rule_results else 0.0

        return {
            "format_score": format_score
        }

    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        if not scores:
            return 0.0
        return sum(scores.values()) / len(scores)

    def _identify_failures(self, rule_results: List[RuleResult]) -> List[str]:
        failures = []

        for result in rule_results:
            if result.rule_id == "check_empty_output" and not result.passed:
                failures.append("empty_output")

        return failures

    def _generate_explanations(
        self,
        rule_results: List[RuleResult],
        failure_labels: List[str]
    ) -> Dict[str, str]:
        explanations = {}

        for label in failure_labels:
            if label == "empty_output":
                explanations[label] = "The output provided by the model was empty."

        return explanations
