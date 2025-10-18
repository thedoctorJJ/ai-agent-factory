# Prompt Library

This directory contains a comprehensive collection of reusable prompts and prompt templates for AI agents in the AI Agent Factory platform.

## 📁 Structure

```
prompt-library/
├── system-prompts/        # System-level prompts for agent behavior
│   ├── general/          # General-purpose system prompts
│   ├── specialized/      # Domain-specific system prompts
│   └── personality/      # Personality and tone prompts
├── user-prompts/         # User-facing prompts and templates
│   ├── onboarding/       # User onboarding prompts
│   ├── task-guidance/    # Task-specific guidance prompts
│   └── error-handling/   # Error and help prompts
├── conversation-starters/ # Initial conversation prompts
│   ├── greetings/        # Welcome and greeting prompts
│   ├── introductions/    # Agent introduction prompts
│   └── context-setting/  # Context establishment prompts
├── task-specific/        # Prompts for specific tasks and workflows
│   ├── data-processing/  # Data analysis and processing prompts
│   ├── api-integration/  # API and service integration prompts
│   ├── code-generation/  # Code generation and review prompts
│   └── decision-making/  # Decision support prompts
├── templates/            # Prompt templates with variables
│   ├── email/           # Email generation templates
│   ├── reports/         # Report generation templates
│   └── documentation/   # Documentation templates
└── examples/            # Example prompt implementations
    ├── chatbot/         # Chatbot conversation examples
    ├── assistant/       # AI assistant examples
    └── automation/      # Automation workflow examples
```

## 🎯 Purpose

The Prompt Library provides:

- **Standardized Prompts**: Consistent prompt patterns across agents
- **Best Practices**: Proven prompt engineering techniques
- **Reusability**: Templates that can be customized for different use cases
- **Quality Assurance**: Tested and validated prompt patterns
- **Documentation**: Clear guidance on prompt usage and customization

## 🚀 Quick Start

### 1. Choose a Prompt Category

```bash
# Browse available prompts
ls system-prompts/
ls user-prompts/
ls task-specific/
```

### 2. Select and Customize

```python
# Example: Using a system prompt
from prompt_library import SystemPrompts

system_prompt = SystemPrompts.get("data-analyst")
customized_prompt = system_prompt.format(
    domain="financial analysis",
    output_format="JSON"
)
```

### 3. Integrate with Your Agent

```python
# Example: FastAPI agent with prompt integration
from fastapi import FastAPI
from prompt_library import PromptManager

app = FastAPI()
prompt_manager = PromptManager()

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    prompt = prompt_manager.get_prompt(
        category="data-processing",
        task="analysis",
        context=request.context
    )
    # Use prompt with your AI model
    result = await ai_model.generate(prompt, request.data)
    return result
```

## 📋 Available Prompt Categories

### System Prompts

#### General Purpose
- **`general-assistant`**: General-purpose AI assistant behavior
- **`helpful-expert`**: Expert-level helpfulness and accuracy
- **`creative-collaborator`**: Creative and collaborative approach

#### Specialized Domains
- **`data-analyst`**: Data analysis and interpretation
- **`software-engineer`**: Code development and review
- **`business-consultant`**: Business analysis and strategy
- **`technical-writer`**: Technical documentation and communication

#### Personality Types
- **`professional`**: Formal, business-appropriate tone
- **`friendly`**: Warm, approachable communication style
- **`concise`**: Brief, to-the-point responses
- **`detailed`**: Comprehensive, thorough explanations

### User Prompts

#### Onboarding
- **`welcome`**: Initial user welcome and introduction
- **`capabilities`**: Agent capability overview
- **`getting-started`**: First-time user guidance

#### Task Guidance
- **`task-clarification`**: Help users clarify their requests
- **`step-by-step`**: Break down complex tasks
- **`progress-updates`**: Provide status updates during long tasks

#### Error Handling
- **`error-explanation`**: Explain errors in user-friendly terms
- **`troubleshooting`**: Guide users through problem resolution
- **`fallback`**: Handle unexpected or unclear requests

### Task-Specific Prompts

#### Data Processing
- **`data-analysis`**: Analyze datasets and provide insights
- **`data-cleaning`**: Clean and prepare data for analysis
- **`data-visualization`**: Create charts and visualizations
- **`statistical-analysis`**: Perform statistical tests and analysis

#### API Integration
- **`api-documentation`**: Generate API documentation
- **`endpoint-testing`**: Test API endpoints and validate responses
- **`integration-setup`**: Guide API integration setup
- **`error-handling`**: Handle API errors and edge cases

#### Code Generation
- **`code-review`**: Review code for quality and best practices
- **`bug-fixing`**: Identify and fix code issues
- **`refactoring`**: Improve code structure and performance
- **`documentation`**: Generate code documentation

## 🔧 Prompt Templates

### Template Variables

Templates support dynamic variables for customization:

```python
# Example template with variables
template = """
You are a {role} specializing in {domain}.
Your task is to {task} with {constraints}.
Provide output in {format} format.
"""

# Usage
prompt = template.format(
    role="data analyst",
    domain="financial markets",
    task="analyze market trends",
    constraints="focus on risk assessment",
    format="structured report"
)
```

### Common Variables

- **`{role}`**: Agent role or persona
- **`{domain}`**: Subject matter domain
- **`{task}`**: Specific task or objective
- **`{context}`**: Additional context or background
- **`{format}`**: Desired output format
- **`{tone}`**: Communication tone or style
- **`{constraints}`**: Limitations or requirements

## 📊 Prompt Quality Metrics

### Evaluation Criteria

- **Clarity**: Clear and unambiguous instructions
- **Completeness**: Covers all necessary aspects
- **Consistency**: Consistent behavior across similar tasks
- **Effectiveness**: Produces desired outcomes
- **Efficiency**: Minimal token usage for maximum impact

### Testing Framework

```python
# Example: Prompt testing
from prompt_library import PromptTester

tester = PromptTester()

# Test prompt effectiveness
results = tester.evaluate_prompt(
    prompt="system-prompts/data-analyst",
    test_cases="test-data/analysis-scenarios.json",
    metrics=["accuracy", "completeness", "clarity"]
)

print(f"Accuracy: {results.accuracy:.2%}")
print(f"Completeness: {results.completeness:.2%}")
print(f"Clarity: {results.clarity:.2%}")
```

## 🎨 Customization Guidelines

### Prompt Engineering Best Practices

1. **Be Specific**: Provide clear, specific instructions
2. **Use Examples**: Include examples of desired output
3. **Set Context**: Provide relevant background information
4. **Define Constraints**: Specify limitations and requirements
5. **Test Iteratively**: Refine prompts based on results

### Customization Patterns

```python
# Pattern 1: Role-based customization
def create_analyst_prompt(domain: str, expertise_level: str):
    base_prompt = SystemPrompts.get("data-analyst")
    return base_prompt.format(
        domain=domain,
        expertise=expertise_level,
        output_style="professional"
    )

# Pattern 2: Task-specific customization
def create_processing_prompt(task_type: str, data_format: str):
    template = TaskPrompts.get("data-processing")
    return template.format(
        task=task_type,
        input_format=data_format,
        validation_rules="strict"
    )
```

## 🔗 Integration Examples

### With FastAPI Agents

```python
from fastapi import FastAPI
from prompt_library import PromptManager

app = FastAPI()
prompts = PromptManager()

@app.post("/chat")
async def chat(request: ChatRequest):
    # Get appropriate prompt based on context
    prompt = prompts.get_contextual_prompt(
        user_intent=request.intent,
        conversation_history=request.history,
        agent_capabilities=request.capabilities
    )
    
    # Generate response using AI model
    response = await ai_model.generate(prompt, request.message)
    return {"response": response}
```

### With Streamlit Applications

```python
import streamlit as st
from prompt_library import UserPrompts

# Initialize prompt manager
prompts = UserPrompts()

# Display welcome message
st.markdown(prompts.get("welcome"))

# Handle user input
user_input = st.text_input("What would you like to know?")
if user_input:
    # Get task guidance prompt
    guidance = prompts.get("task-guidance", context=user_input)
    st.info(guidance)
```

## 📚 Documentation

- **[Prompt Engineering Guide](docs/prompt-engineering.md)** - Best practices for prompt design
- **[Template Reference](docs/template-reference.md)** - Complete template documentation
- **[Integration Examples](docs/integration-examples.md)** - Code examples and patterns
- **[Testing Guide](docs/testing-guide.md)** - Prompt testing and validation

## 🧪 Testing

### Test Structure

```bash
tests/
├── unit/              # Individual prompt tests
├── integration/       # End-to-end prompt testing
├── performance/       # Prompt performance benchmarks
└── fixtures/          # Test data and scenarios
```

### Running Tests

```bash
# Test all prompts
pytest tests/

# Test specific category
pytest tests/unit/test_system_prompts.py

# Performance testing
pytest tests/performance/ -v
```

## 🤝 Contributing

To contribute to the Prompt Library:

1. **Follow Guidelines**: Use established prompt patterns and formats
2. **Test Thoroughly**: Validate prompts with multiple test cases
3. **Document Usage**: Provide clear usage examples and documentation
4. **Submit PR**: Create pull request with detailed description

## 📄 License

This Prompt Library is part of the AI Agent Factory project and follows the same licensing terms.
