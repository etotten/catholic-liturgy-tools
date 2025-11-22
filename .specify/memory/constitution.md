<!--
Sync Impact Report:
Version change: none → 1.0.0 (initial constitution creation)
Modified principles: N/A (initial version)
Added sections: All sections (initial constitution)
Removed sections: None
Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (pending verification)
  - ✅ .specify/templates/spec-template.md (pending verification)
  - ✅ .specify/templates/tasks-template.md (pending verification)
Follow-up TODOs: None
-->

# Project Constitution

**Project Name:** Catholic Liturgy Tools  
**Version:** 1.0.0  
**Ratification Date:** 2025-11-22  
**Last Amended:** 2025-11-22

---

## Purpose

This constitution establishes the foundational principles, guidelines, and requirements for the Catholic Liturgy Tools project. All development, contributions, and decisions must adhere to these principles.

---

## Principles

### Principle 1: Liturgical Authenticity

**Name:** Liturgical Authenticity

**Rules:**
- ALL liturgical content MUST derive from authoritative Catholic sources
- No content may be included from unofficial, speculative, or non-authoritative sources
- When in doubt about source authenticity, content MUST be reviewed and verified before inclusion
- Sources MUST be clearly documented and traceable

**Rationale:**
The integrity of Catholic liturgical content is paramount. Using only authoritative sources ensures doctrinal correctness and prevents the propagation of errors or unauthorized materials.

**Acceptable Sources (non-exhaustive):**
- Official Vatican publications
- USCCB (United States Conference of Catholic Bishops) approved texts
- Liturgy of the Hours (official editions)
- Roman Missal (official editions)
- Catechism of the Catholic Church
- Papal documents and encyclicals
- Documents from Ecumenical Councils

**Source Documentation Requirements:**
Each liturgical text or content MUST include:
- Source identification
- Edition/version information
- Copyright status (if applicable)
- Date of content

### Principle 2: Simplicity and Minimalism

**Name:** Simplicity and Minimalism

**Rules:**
- Implementations MUST be kept simple and minimal
- Complexity MAY grow organically only as demonstrated need arises
- Straightforward solutions are REQUIRED over clever abstractions
- Development MUST stick to stated requirements; scope creep is forbidden
- Features MUST be built as thin slices that can be incrementally enhanced
- Large, monolithic implementations are NOT PERMITTED

**Rationale:**
Simple code is maintainable code. By keeping implementations minimal and building incrementally, we reduce bugs, improve clarity, and make the codebase accessible to contributors. Premature complexity increases maintenance burden without corresponding benefit.

### Principle 3: Correctness Over Performance

**Name:** Correctness Over Performance

**Rules:**
- Correctness and clarity MUST be prioritized over optimization
- Performance optimizations MAY only be added when a demonstrated need exists
- Code MUST be easy to understand and maintain
- Premature optimization is NOT PERMITTED

**Rationale:**
Correct code that performs adequately is better than fast code that contains subtle bugs. Clarity enables verification and maintenance. Performance can be addressed when profiling demonstrates actual bottlenecks.

### Principle 4: Testing Discipline

**Name:** Testing Discipline

**Rules:**
- Unit test coverage MUST be at least 90%
- Coverage MUST be checked and enforced with each development phase
- End-to-end (E2E) tests MUST exist for ALL CLI options
- Tests MUST be maintained alongside feature development
- No feature is considered complete without adequate test coverage
- Test quality matters as much as test quantity

**Rationale:**
High test coverage provides confidence in changes and prevents regressions. E2E tests ensure that user-facing functionality works as expected. Testing discipline is non-negotiable for maintaining project quality.

**Testing Tools:**
- pytest for test execution
- pytest-cov for coverage measurement
- Coverage reports MUST be generated for verification

### Principle 5: CLI-First Development

**Name:** CLI-First Development

**Rules:**
- A CLI MUST be maintained and kept current with all features
- All CLI options MUST have corresponding E2E tests
- CLI MUST provide helpful error messages and documentation
- CLI serves as both a user interface and manual verification tool

**Rationale:**
The CLI serves dual purposes: it provides direct value to users and enables developers to manually verify functionality during development. A well-maintained CLI also serves as living documentation of project capabilities.

### Principle 6: Semantic Versioning

**Name:** Semantic Versioning

**Rules:**
The project MUST follow [Semantic Versioning 2.0.0](https://semver.org/)

**Format:** MAJOR.MINOR.PATCH

**MAJOR version** (X.0.0) - MUST increment when:
- Making incompatible API changes
- Removing or renaming public functions, classes, or methods
- Changing function signatures in non-backward-compatible ways
- Removing or renaming CLI commands or arguments
- Changing default behavior that breaks existing usage

**MINOR version** (0.X.0) - MUST increment when:
- Adding new functionality in a backward-compatible manner
- Adding new public functions, classes, or methods
- Adding new CLI commands or optional arguments
- Adding new features without breaking existing functionality
- Deprecating functionality (but not removing it)

**PATCH version** (0.0.X) - MUST increment when:
- Fixing bugs without changing the public API
- Updating documentation
- Making internal code improvements
- Applying security patches that don't affect functionality
- Improving test coverage

**Pre-1.0 Development:**
- During 0.x.x versions, the API is not considered stable
- Breaking changes MAY occur in MINOR releases during this phase
- Version 1.0.0 will be released when the API is considered stable

**Rationale:**
Semantic versioning provides clear expectations to users about the impact of updates. It enables informed decision-making about when to upgrade and what testing may be required.

### Principle 7: Python 3.11 Standard

**Name:** Python 3.11 Standard

**Rules:**
- Primary language MUST be Python 3.11
- All Python code MUST be compatible with Python 3.11+
- Alternative languages MAY be used only when significantly more convenient for specific tasks
- Such exceptions MUST be documented and justified

**Rationale:**
Standardizing on Python 3.11 ensures consistency, leverages modern Python features, and simplifies dependency management. The language choice aligns with the project's requirements for clarity and maintainability.

### Principle 8: Scope Constraints for Early Development

**Name:** Scope Constraints for Early Development

**Rules:**
During early development (pre-1.0), the following constraints apply:
- English-only (no multilingual support required)
- No accessibility features required at this stage
- No performance optimizations unless demonstrated need exists
- Focus MUST be on core functionality first

These constraints MAY be lifted in future constitution amendments as the project matures.

**Rationale:**
Limiting scope during early development allows focus on core functionality and prevents premature complexity. As the project matures and demonstrates value, these constraints can be relaxed through constitutional amendment.

---

## Governance

### Amendment Process

At this early stage, the amendment process is intentionally simple and informal:

**Amendment Procedure:**
1. Amendments MAY be proposed by project maintainers
2. Amendments MUST be documented in git history
3. Constitution version number MUST increment with changes according to semantic versioning rules
4. Once amended, the current constitution MUST be followed strictly

**Constitution Versioning:**
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

### Constitution Authority

- The constitution in the main branch is authoritative
- All code, decisions, and contributions MUST conform to the current constitution
- When constitution conflicts with other documentation, constitution takes precedence

### Future Governance Evolution

As the project matures, a more formal amendment process MAY be established, such as:
- Required review periods for proposed changes
- Stakeholder approval mechanisms
- Major vs. minor amendment classifications

---

## Technical Standards

### Project Structure

**Required Files:**
- `pyproject.toml` - Package configuration and dependencies
- `README.md` - Project overview and usage instructions
- `CHANGELOG.md` - Version history and changes
- `.specify/memory/constitution.md` - This document
- `LICENSE` - Project license

**Required Directory Structure:**
```
catholic-liturgy-tools/
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/
│   └── scripts/
├── src/
│   └── catholic_liturgy_tools/
│       ├── __init__.py
│       ├── cli.py
│       └── [feature modules]
├── tests/
│   ├── conftest.py
│   ├── test_*.py
│   └── e2e/
│       └── test_cli_*.py
├── docs/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
└── LICENSE
```

### Code Quality Standards

**Required:**
- Code MUST be formatted consistently (Black recommended)
- Linting rules MUST be followed (Ruff or similar)
- Code MUST be readable and well-documented
- Docstrings MUST exist for all public functions and classes

**Encouraged:**
- Type hints (encouraged but not required at this stage)
- Comments for complex logic

---

## Quality Gates

### Pre-Commit Requirements

The following MUST pass before any commit:
- All tests MUST pass
- Test coverage MUST meet 90% minimum
- Code MUST pass linting checks
- No unresolved merge conflicts

### Pre-Release Requirements

The following MUST be completed before any release:
- All features MUST be documented in README
- CHANGELOG MUST be updated with all changes
- Version numbers MUST be updated consistently across all files
- All E2E tests MUST pass
- CLI help text MUST be current and accurate

---

## Development Workflow

### Iterative Development

**Required Approach:**
- Focus on thin slices of functionality
- Build features incrementally
- Each iteration MUST be complete and testable
- Building everything at once is NOT PERMITTED

### Feature Development Checklist

For each new feature, the following MUST be completed:
- [ ] Implement core functionality
- [ ] Add unit tests (90%+ coverage)
- [ ] Add CLI commands/options if applicable
- [ ] Add E2E tests for CLI
- [ ] Update documentation
- [ ] Verify all tests pass
- [ ] Update CHANGELOG.md

---

## Compliance

### Constitution Adherence

- All development MUST comply with this constitution
- Non-compliant code MAY be rejected or reverted
- Exceptions REQUIRE explicit documentation and justification

### Review Process

- Code reviews MUST verify constitutional compliance
- Testing requirements are non-negotiable
- Source authenticity MUST be verified for liturgical content

---

## Documentation Standards

### Code Documentation

**Required:**
- Docstrings for all public functions and classes
- Comments for complex logic
- README with clear usage examples

**As Project Grows:**
- API documentation
- Architecture documentation

### User Documentation

**Required:**
- Clear installation instructions
- Usage examples for all features
- CLI help text for all commands
- Troubleshooting guidance

---

## Release Process

**Required Steps:**
1. Determine version bump based on changes since last release
2. Update version in all relevant files (`pyproject.toml`, `__init__.py`, etc.)
3. Update `CHANGELOG.md` with changes
4. Create git tag (e.g., `v0.1.0`)
5. Push tag: `git push origin v0.1.0`
6. Verify release artifacts

---

## Version History

### Version 1.0.0 (2025-11-22)
- Initial constitution established
- Eight core principles defined
- Technical standards specified
- Versioning rules documented
- Development workflow outlined
- Governance structure established
