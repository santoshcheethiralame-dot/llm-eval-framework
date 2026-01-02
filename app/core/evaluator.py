from app.schemas.evaluation import EvaluationRequest, EvaluationResponse, RuleResult
from app.rules.format_rules import EmptyOutputRule, JSONFormatRule, LengthConstraintRule
from app.rules.content_rules import RequiredKeywordsRule, ForbiddenPhrasesRule
from datetime import datetime
import uuid
from typing import Dict, List

class Evaluator:

    def __init__(self):
        self.rules = [
            EmptyOutputRule(),
            JSONFormatRule(),
            LengthConstraintRule(),
            RequiredKeywordsRule(),
            ForbiddenPhrasesRule()
        ]

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
        results = []

        for rule in self.rules:
            try:
                result = rule.evaluate(request)
                results.append(result)
            except Exception as e:
                results.append(
                    RuleResult(
                        rule_id=rule.rule_id,
                        rule_name=rule.rule_name,
                        passed=False,
                        score=0.0,
                        explanation=f"Rule execution failed: {str(e)}"
                    )
                )

        return results

    def _aggregate_scores(self, rule_results: List[RuleResult]) -> Dict[str, float]:
        format_rules = ["empty_output", "json_format", "length_constraint"]
        content_rules = ["required_keywords", "forbidden_phrases"]

        format_scores = [r.score for r in rule_results if r.rule_id in format_rules]
        content_scores = [r.score for r in rule_results if r.rule_id in content_rules]

        scores = {}

        if format_scores:
            scores["format_score"] = sum(format_scores) / len(format_scores)

        if content_scores:
            scores["content_score"] = sum(content_scores) / len(content_scores)

        return scores

    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        if not scores:
            return 0.0
        return sum(scores.values()) / len(scores)

    def _identify_failures(self, rule_results: List[RuleResult]) -> List[str]:
        failures = []

        for result in rule_results:
            if not result.passed:
                failures.append(result.rule_id)

        return failures

    def _generate_explanations(
        self,
        rule_results: List[RuleResult],
        failure_labels: List[str]
    ) -> Dict[str, str]:
        explanations = {}

        for result in rule_results:
            if not result.passed:
                explanations[result.rule_id] = result.explanation

        return explanations
