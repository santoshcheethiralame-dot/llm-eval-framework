from app.schemas.evaluation import EvaluationRequest, RuleResult
from app.rules.base_rule import BaseRule
import json
import re


# Rule to check if the output is empty or contains only whitespaces
class EmptyOutputRule(BaseRule):

    @property
    def rule_id(self) -> str:
        return "empty_output"

    @property
    def rule_name(self) -> str:
        return "empty output detection"

    def evaluate(self, request: EvaluationRequest) -> RuleResult:
        output = request.output.strip()

        if len(output) == 0:
            return self._create_result(
                passed=False,
                score=0.0,
                explanation="output is empty or contians only whitespaces"
            )

        return self._create_result(
            passed=True,
            score=1.0,
            explanation=f"output contains {len(output)} characters"
        )


# Rule to check if the output is valid JSON when expected
class JSONFormatRule(BaseRule):

    @property
    def rule_id(self) -> str:
        return "json_format"

    @property
    def rule_name(self) -> str:
        return "JSON format validation"

    def evaluate(self, request: EvaluationRequest) -> RuleResult:
        expects_json = self._expects_json(request)

        if not expects_json:
            return self._create_result(
                passed=True,
                score=1.0,
                explanation="no JSON format expected for this task"
            )

        output = request.output.strip()

        try:
            parsed = json.loads(output)
            return self._create_result(
                passed=True,
                score=1.0,
                explanation=f"Valid JSON with {len(str(parsed))} characters"
            )
        except json.JSONDecodeError as e:
            return self._create_result(
                passed=False,
                score=0.0,
                explanation=f"Invalid JSON format: {str(e)}"
            )

    def _expects_json(self, request: EvaluationRequest) -> bool:
        if request.task_type and "json" in request.task_type.lower():
            return True

        if request.prompt:
            prompt_lower = request.prompt.lower()
            json_keywords = {"json", "return {", "output {", "format {"}

            for keyword in json_keywords:
                if keyword in prompt_lower:
                    return True

        return False


# Rule to check if the output meets length constraints specified in the prompt
class LengthConstraintRule(BaseRule):

    @property
    def rule_id(self) -> str:
        return "length_constraint"

    @property
    def rule_name(self) -> str:
        return "Length constraint validation"

    def evaluate(self, request: EvaluationRequest) -> RuleResult:
        if not request.prompt:
            return self._create_result(
                passed=True,
                score=1.0,
                explanation="No prompt provided to check constraints"
            )

        constraint = self._extract_length_constraint(request.prompt)

        if not constraint:
            return self._create_result(
                passed=True,
                score=1.0,
                explanation="No length constraint detected in prompt"
            )

        limit_type, limit_value = constraint
        actual_value = self._measure_output(request.output, limit_type)

        if actual_value <= limit_value:
            return self._create_result(
                passed=True,
                score=1.0,
                explanation=f"Output meets the {limit_type} constraint of {limit_value}. Actual: {actual_value}"
            )

        excess_pct = ((actual_value - limit_value) / limit_value) * 100
        score = max(0.0, 1.0 - (excess_pct / 100))

        return self._create_result(
            passed=False,
            score=score,
            explanation=f"output has {actual_value} {limit_type}, exceeds limit of {limit_value} by {excess_pct:.1f}%"
        )

    def _extract_length_constraint(self, prompt: str):
        prompt_lower = prompt.lower()

        word_match = re.search(r'(\d+)\s*words?', prompt_lower)
        if word_match:
            return "words", int(word_match.group(1))

        char_match = re.search(r'(\d+)\s*characters?', prompt_lower)
        if char_match:
            return "characters", int(char_match.group(1))

        sent_match = re.search(r'(\d+)\s*sentences?', prompt_lower)
        if sent_match:
            return "sentences", int(sent_match.group(1))

        return None

    def _measure_output(self, output: str, measure_type: str) -> int:
        if measure_type == "words":
            return len(output.split())

        if measure_type == "characters":
            return len(output)

        if measure_type == "sentences":
            sentences = re.split(r"[.!?]+", output)
            return len([s for s in sentences if s.strip()])

        return 0