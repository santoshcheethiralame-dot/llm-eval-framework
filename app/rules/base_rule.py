from abc import ABC, abstractmethod
from app.schemas.evaluation import EvaluationRequest, RuleResult

class BaseRule(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def rule_id(self) -> str:
        pass

    @property
    @abstractmethod
    def rule_name(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, request: EvaluationRequest) -> RuleResult:
        pass

    def _create_result(
        self,
        passed: bool,
        score: float,
        explanation: str
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            passed=passed,
            score=score,
            explanation=explanation
        )