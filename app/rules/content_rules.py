from app.rules.base_rule import BaseRule
from app.schemas.evaluation import EvaluationRequest, RuleResult
import re


# Rule to check if the output contains required keywords specified in the prompt
class RequiredKeywordsRule(BaseRule):
    @property
    def rule_id(self) -> str:
        return "required_keywords"

    @property
    def rule_name(self) -> str:
        return "required keyword detection"

    def evaluate(self, request: EvaluationRequest) -> RuleResult:
        if not request.prompt:
            return self._create_result(
                passed=True,
                score=1.0,
                explanation="No prompt provided to check keywords"
            )

        required_keywords = self._extract_required_keywords(request.prompt)

        if not required_keywords:
            return self._create_result(
                passed=True,
                score=1.0,
                explanation="No required keywords detected in prompt"
            )

        output_lower = request.output.lower()
        missing_keywords = []
        found_keywords = []

        for keyword in required_keywords:
            if keyword.lower() in output_lower:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)

        score = len(found_keywords) / len(required_keywords) if required_keywords else 1.0

        if missing_keywords:
            return self._create_result(
                passed=False,
                score=score,
                explanation=f"Missing required keywords: {', '.join(missing_keywords)}"
            )

        return self._create_result(
            passed=True,
            score=1.0,
            explanation=f"All {len(required_keywords)} required keywords present: {', '.join(found_keywords)}"
        )

    def _extract_required_keywords(self, prompt: str) -> list[str]:
        keywords = []

        pattern1 = re.findall(
            r"must (?:include|mention|contain|use)(?: the (?:word|term|phrase))? ['\"]([^'\"]+)['\"]",
            prompt,
            re.IGNORECASE,
        )
        keywords.extend(pattern1)

        pattern2 = re.findall(
            r"make sure to (?:mention|include|use) ['\"]([^'\"]+)['\"]",
            prompt,
            re.IGNORECASE,
        )
        keywords.extend(pattern2)

        pattern3_match = re.search(
            r"include (?:the )?following (?:terms?|words?|phrases?)?:?\s*([^\n]+)",
            prompt,
            re.IGNORECASE,
        )
        if pattern3_match:
            terms_str = pattern3_match.group(1)
            terms = [t.strip().strip("\"',") for t in terms_str.split(",")]
            keywords.extend(terms)

        return list(set(keywords))



# Rule to check if the output contains forbidden phrases
class ForbiddenPhrasesRule(BaseRule):
    FORBIDDEN_PHRASES = [
        "as an ai",
        "as a language model",
        "i'm an ai",
        "i am an ai",
        "i don't have access to",
        "i cannot browse",
        "i don't have the ability to",
        "my training data",
        "my knowledge cutoff",
        "i'm not able to",
        "i cannot provide real-time",
    ]

    @property
    def rule_id(self) -> str:
        return "forbidden_phrases"

    @property
    def rule_name(self) -> str:
        return "forbidden phrase detection"

    def evaluate(self, request: EvaluationRequest) -> RuleResult:
        output_lower = request.output.lower()

        found_phrases = []
        for phrase in self.FORBIDDEN_PHRASES:
            if phrase in output_lower:
                found_phrases.append(phrase)

        if found_phrases:
            score = max(0.0, 1.0 - (len(found_phrases) * 0.3))
            
            if len(found_phrases) <= 5:
                phrases_list = "', '".join(found_phrases)
                explanation = f"contains {len(found_phrases)} forbidden phrase(s): '{phrases_list}'"
            else:
                first_five = "', '".join(found_phrases[:5])
                remaining = len(found_phrases) - 5
                explanation = f"contains {len(found_phrases)} forbidden phrase(s): '{first_five}' and {remaining} more"
            
            return self._create_result(
                passed=False,
                score=score,
                explanation=explanation,
            )

        return self._create_result(
            passed=True,
            score=1.0,
            explanation="No forbidden phrases detected",
        )