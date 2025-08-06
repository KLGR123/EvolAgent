# EvolAgent

> **🏆 GAIA Leaderboard Achievement**  
> Achieved a score of **65.12** on the [GAIA benchmark test dataset](https://huggingface.co/spaces/gaia-benchmark/leaderboard), demonstrating state-of-the-art performance in general AI assistant capabilities.

## Overview

EvolAgent is an advanced AI agent framework that combines cognitive science principles with modern language models to create intelligent, adaptive agents capable of complex reasoning and problem-solving. Built on psychological theories of human cognition, EvolAgent implements a sophisticated multi-agent architecture with hierarchical memory systems.

## 🚀 Key Features

### Core Architecture
- **Multi-Agent Collaboration**: Coordinated team of specialized agents (Planner, Developer, Tester, Critic)
- **Hierarchical Cross-Task Memory**: Multi-layered memory system inspired by cognitive psychology
- **Meta Tool Learning**: Dynamic tool acquisition and usage optimization
- **RAG Knowledge Update**: Real-time knowledge integration and retrieval
- **Multi-Path Sampling**: Self-consistency through diverse solution approaches

### Advanced Capabilities
- **Cognitive Memory System**: Working, procedural, semantic, and episodic memory integration
- **Dynamic Task Decomposition**: Intelligent problem breakdown and solution synthesis
- **Real-time Learning**: Continuous improvement through experience accumulation
- **Web-based Log Viewer**: Comprehensive experiment tracking and analysis interface

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [Cognitive Framework](#cognitive-framework)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EvolAgent
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup web crawling capabilities**
   ```bash
   crawl4ai-setup
   crawl4ai-doctor
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## 🚀 Quick Start

### Basic Usage

1. **Run cold start initialization** (optional, for initial knowledge base)
   ```bash
   export TOKENIZERS_PARALLELISM=true
   python coldstart.py
   ```

2. **Execute main agent pipeline**
   ```bash
   python run.py
   ```

3. **Start web-based log viewer** (for experiment analysis)
   ```bash
   python server.py
   ```

4. **Clean workspace** (after experiments)
   ```bash
   rm -rf workspace/*
   ```

### Configuration

Edit `config.yaml` to customize:
- Model selection and parameters
- Memory system configuration
- Pipeline behavior
- Logging preferences

## 🏗️ Architecture

EvolAgent implements a sophisticated multi-agent architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Planner       │───▶│   Developer     │───▶│   Tester        │
│   (Strategy)    │    │ (Implementation)│    │   (Validation)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────▼───────────────────────┘
                        ┌─────────────────┐
                        │     Critic      │
                        │  (Evaluation)   │
                        └─────────────────┘
```

### Agent Roles

- **Planner**: Strategic task decomposition and solution planning
- **Developer**: Code implementation and technical execution
- **Tester**: Solution validation and quality assurance
- **Critic**: Multi-perspective evaluation and best solution selection

## 🧠 Cognitive Framework

EvolAgent's design is grounded in established cognitive science theories:

### Memory Architecture

Based on Atkinson and Shiffrin (1968) and Baddeley and Hitch (1974):

- **Working Memory**: Current context, recent inputs, and active reasoning
- **Long-term Memory** (three distinct types):
  - **Procedural Memory**: System rules and behavioral patterns
  - **Semantic Memory**: World knowledge and facts
  - **Episodic Memory**: Historical experiences and past behaviors

### Memory Priority System
```
Procedural (System) > Semantic (Few-shots) > Episodic (Experiments)
```

This hierarchy ensures that:
1. Core system behaviors take precedence
2. Curated examples guide learning
3. Experimental data informs adaptation

### Theoretical Foundation

- **Soar Architecture**: Multi-memory cognitive system (Laird, 2012)
- **Working Memory Theory**: Baddeley & Hitch (1974)
- **Memory Systems**: Atkinson & Shiffrin (1968)
- **Semantic Memory**: Lindes & Laird (2016)
- **Episodic Memory**: Nuxoll & Laird (2007)

## ⚙️ Configuration

### Key Configuration Files

- `config.yaml`: Main system configuration
- `.env`: Environment variables and API keys
- `src/memory/`: Memory system templates and examples

### Customization Options

- **Model Selection**: Choose from various LLM providers
- **Memory Limits**: Configure memory capacity and retention
- **Pipeline Parameters**: Adjust iteration limits and thresholds
- **Logging Levels**: Control detail and output formats

## 📊 Monitoring and Analysis

EvolAgent includes a comprehensive web-based interface for experiment tracking:

- **Real-time Log Viewing**: Monitor agent execution in real-time
- **Task Search**: Quickly locate specific experiments by ID
- **Performance Analytics**: Analyze success rates and patterns
- **Multi-model Comparison**: Compare different model performances

Access the interface at `http://localhost:5002` after running `python server.py`.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for:

- Code style and standards
- Testing requirements
- Documentation expectations
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 References

- Atkinson, R. C., & Shiffrin, R. M. (1968). Human memory: A proposed system and its control processes.
- Baddeley, A., & Hitch, G. (1974). Working memory.
- Laird, J. E. (2012). The Soar Cognitive Architecture.
- Lindes, P., & Laird, J. E. (2016). Toward integrating cognitive linguistics and cognitive architectures.
- Nuxoll, A., & Laird, J. E. (2007). Extending cognitive architectures with episodic memory.

---

**Built with ❤️ for advancing AI agent capabilities**