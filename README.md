# LLM Evaluation & Reliability Framework

A reproducible, explainable evaluation system for Large Language Model outputs.

## 🎯 Project Goal

Build an engineering-first framework that evaluates LLM reliability by:

- Running deterministic rule-based checks
- Identifying specific failure modes
- Providing explainable scores and reports
- Comparing behavior across models and prompts

## 🏗️ Current Status

**Day 2 Complete** ✅

- 5 working evaluation rules (format + content)
- Modular BaseRule abstract class
- Dimension-based scoring (format_score, content_score)
- Comprehensive test coverage with edge cases
- Bug fixes and improvements

**Rules Implemented:**

1. ✅ Empty Output Detection
2. ✅ JSON Format Validation
3. ✅ Length Constraint Checking
4. ✅ Required Keywords Detection
5. ✅ Forbidden Phrases Detection

## 📋 Roadmap

- [x] Day 1: Project setup + basic API
- [x] Day 2: Core rule engine (format, length, keywords)
- [ ] Day 3: Instruction adherence rules
- [ ] Day 4: Prompt injection detection
- [ ] Day 5: Hallucination heuristics
- [ ] Week 2-3: Storage, testing, documentation
- [ ] Week 4+: LLM-as-judge, comparative evaluation

## 🛠️ Tech Stack

- **Backend**: FastAPI + Pydantic
- **Testing**: pytest (coming soon)
- **Storage**: JSON/SQLite (coming soon)

## 📚 Learning Goals

This is a capstone project focused on:

- Schema-first API design
- Deterministic evaluation logic
- Failure-mode taxonomy in AI systems
- Building reliable AI infrastructure

## 📖 Documentation

- [Project Statement](docs/PROJECT_STATEMENT.md) - Full project specification
- API Docs: http://127.0.0.1:8000/docs (when server is running)

## 🤝 Contributing

This is a learning project, but feedback welcome via issues!

## 📝 License

MIT License - see LICENSE file
