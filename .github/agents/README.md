# Stanza Agent Personas

This directory contains detailed persona files for different stakeholder roles in the Stanza project. Each persona provides context, responsibilities, workflows, and best practices for their specific role.

## Available Personas

### 1. [Stanford Team Member](stanford-team-member.md)
Role: Core team member with strategic responsibility

Focus:
- Long-term architecture and strategy
- Research alignment
- Quality standards
- Community leadership

When to use: Strategic decisions, major architecture changes, research integration

Authority: Makes final decisions on core features, architecture changes, long-term roadmap

---

### 2. [Project Contributor](project-contributor.md)
Role: Open-source contributor implementing features and fixes

Focus:
- Feature development and bug fixes
- Code quality and testing
- Documentation updates
- Community participation

When to use: Contributing features, fixing bugs, writing tests, submitting PRs

Scope: Works on assigned issues, follows contribution guidelines, collaborative implementation

---

### 3. [QA/Tester](tester.md)
Role: Quality assurance specialist ensuring reliability and correctness

Focus:
- Test strategy and design
- Coverage and quality metrics
- Performance and benchmarking
- Integration testing

When to use: Test planning, quality evaluation, performance optimization, CI/CD

Authority: Sets quality standards, identifies bugs, validates fixes

---

### 4. [Consumer/User](consumer.md)
Role: End-user of the Stanza library

Focus:
- Solving real-world NLP problems
- Library usability
- Documentation clarity
- Production deployment

When to use: Using Stanza, troubleshooting, learning, building applications

Scope: Uses public API, consumes documentation, requests features

---

### 5. [Debugger](debugger.md)
Role: Debugging specialist for issue resolution

Focus:
- Root cause analysis
- Issue investigation
- Performance profiling
- Fix validation

When to use: Investigating bugs, analyzing failures, performance issues

Process: Systematic troubleshooting, data gathering, hypothesis testing

---

### 6. [Security & DevSecOps Agent](security-agent.md)
Role: Security specialist maintaining safe practices

Focus:
- Vulnerability management
- Dependency security
- Secure development practices
- CI/CD security

When to use: Security reviews, dependency evaluation, breach response

Authority: Approves dependencies, security decisions, compliance

---

## How to Use These Personas

### For Context Setting

When starting work on a task, activate the relevant persona:

```python
# Example: Starting to contribute a feature
# 1. Read: project-contributor.md
# 2. Understand: contribution workflow, code standards, community guidelines
# 3. Execute: Based on persona guidance
```

### For Guidance

When facing decisions, consult relevant personas:

- Architecture decision? → Stanford Team Member
- Implementing feature? → Project Contributor  
- Quality concern? → Tester
- Test failure? → Debugger
- Security issue? → Security Agent
- Using the library? → Consumer

### For Communication

When interacting within the project, adopt the appropriate persona's communication style:

```markdown
# As Contributor
"I'd like to implement feature X. Here's my proposed approach..."

# As Tester  
"We should add tests for X. The coverage is currently Y%..."

# As Debugger
"The root cause is Z. I traced it to file:line where..."

# As Security Agent
"This dependency has a known CVE. Recommend updating to version X..."
```

## Persona Interaction Map

```
Stanford Team Member
├── Guides strategy for: Contributor, Tester, Debugger
├── Reviews decisions from: Contributor, Security Agent
└── Approves major: Architecture, roadmap, releases

Project Contributor  
├── Works with: Tester (test requirements), Debugger (if blocked)
├── Reports to: Stanford Team Member (design approval)
└── Coordinates with: Security Agent (dependency review)

Tester
├── Reports quality to: Stanford Team Member
├── Works with: Debugger (test failures)
├── Reviews PRs from: Contributor
└── Monitors: Coverage, performance, reliability

Debugger
├── Supports: Contributor (debugging fix), Tester (test failures)
├── Reports to: Stanford Team Member (architectural issues)
└── Escalates to: Security Agent (security bugs)

Security Agent
├── Reviews: Contributor PRs (dependencies), all releases
├── Reports to: Stanford Team Member (strategy)
├── Coordinates with: Debugger (vulnerability fixes)
└── Monitors: Dependencies, CI/CD, compliance

Consumer
├── Reports issues to: Debugger, Contributor
├── Requests features from: Stanford Team Member
├── Learns from: Documentation, examples
└── Contributes back as: Contributor (optional)
```

## Decision Matrix

| Decision Type | Primary Owner | Consulted | Authority |
|---------------|---------------|-----------|-----------|
| Architecture | Stanford Team | Contributor, Debugger | Team |
| Feature scope | Stanford Team | Contributor | Team |
| Code quality | Tester | Contributor | Tester |
| Performance | Tester | Debugger | Tester |
| Security | Security Agent | Debugger | Security |
| Dependencies | Security Agent | Stanford Team | Security |
| Releases | Stanford Team | All personas | Team |
| Documentation | Contributor | Tester, Consumer | Contributor |
| Testing approach | Tester | Contributor, Debugger | Tester |

## Workflow Examples

### Scenario 1: Implementing a New Language Support

Timeline: 2-3 weeks

1. Consumer (you): Opens issue requesting Basque language support
2. Stanford Team Member: Reviews, decides if aligned with strategy
3. Project Contributor: Volunteers to implement
4. Contributor: Develops, tests, coordinates with community
5. Tester: Reviews test coverage, validates model quality
6. Debugger: Helps with any integration issues
7. Security Agent: Validates any new dependencies
8. Stanford Team: Final review and merge decision

### Scenario 2: Investigating Performance Regression

Timeline: 1-2 days

1. Tester (you): Identifies 15% slowdown in recent PRs
2. Debugger: Profiles code to isolate bottleneck
3. Debugger: Traces issue to new dependency version
4. Security Agent: Checks if dependency can be downgraded
5. Project Contributor: Fixes the regression
6. Tester: Validates fix, adds performance benchmark
7. Stanford Team: Reviews and merges

### Scenario 3: Security Vulnerability Found

Timeline: Hours to days depending on severity

1. Security Agent (you): Receives vulnerability report
2. Debugger: Reproduces and assesses impact
3. Security Agent: Determines CVSS score and severity
4. Project Contributor: Develops patch
5. Tester: Validates fix doesn't break anything
6. Stanford Team: Reviews, decides disclosure timeline
7. All: Implement responsible disclosure

## Best Practices Across Personas

1. Always document decisions - Future you will thank present you
2. Communicate early - Ask questions before investing time
3. Follow established patterns - Use existing approaches as templates
4. Test thoroughly - Catch issues early when they're cheap to fix
5. Keep security in mind - It's everyone's responsibility
6. Help newer contributors - Share knowledge and patterns
7. Celebrate wins - Recognize and appreciate contributions

## Getting Help

Each persona document includes:
- ✅ Context: Role, focus, and responsibilities
- ✅ Processes: Step-by-step workflows
- ✅ Tools: Recommended tools and resources
- ✅ Examples: Real scenarios and interactions
- ✅ References: Links to documentation and guides

To get started:
1. Identify your primary persona
2. Read the full persona document
3. Understand the workflows and best practices
4. Consult the document when making decisions
5. Reference examples for communication patterns

---

Project: Stanza - A Python NLP Library for Many Human Languages

Organization: Stanford Natural Language Processing Group

More Information: https://stanfordnlp.github.io/stanza/

Contributing: See CONTRIBUTING.md in project root
