# DARWIN System v0.1.0

**DARWIN**: Dynamic Agent-based Research for Social Autonomous Worlds with AI and Social Networks

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-API-purple.svg)](https://anthropic.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-blue.svg)](https://deepseek.com/)

<div align="center">
  <img src="docs/images/darwin_network.png" alt="DARWIN Network Visualization" width="100%" style="max-width: 1400px"/>
  <p><em>DARWIN's Multi-Platform Social Dynamics: Visualizing information propagation patterns and herd effects across social networks, featuring muti agent actions, cross-platform interactions, and million-agent simulation capabilities.</em></p>
</div>

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Getting Started](#-getting-started)
- [Usage Examples](#-usage-examples)
- [Advanced Configuration](#-advanced-configuration)
- [Performance & Scaling](#-performance--scaling)
- [Research Applications](#-research-applications)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact & Support](#-contact--support)

## 🌍 Overview

DARWIN is a groundbreaking, open-source simulation platform inspired by the principles of evolution and adaptation. It's designed to study the ever-evolving dynamics of social media with up to one million adaptive, AI-driven agents.

### 🌱 What Makes DARWIN Special?

Social media is a living, breathing ecosystem where information spreads, opinions evolve, and collective behaviors emerge. Studying these phenomena in real-world settings often proves challenging due to ethical, logistical, and cost-related constraints. DARWIN provides a revolutionary solution by creating a dynamic environment where AI agents interact, adapt, and evolve over time.

DARWIN reimagines social media simulation as an evolving ecosystem by:
- Combining the power of large language models (LLMs) with agent-based modeling
- Creating dynamic environments for up to one million concurrent agents
- Enabling agents to develop unique personalities, goals, and adaptive behaviors
- Supporting realistic evolution of behaviors, preferences, and strategies

### Why Choose DARWIN?

- **Scale & Realism**: Simulate massive social networks with AI-driven agents that exhibit human-like behaviors
- **Research Flexibility**: Study everything from information cascades to opinion dynamics
- **Cost-Effective**: Alternative to expensive real-world social experiments
- **Ethical Research**: Safe environment for studying sensitive social phenomena
- **Reproducibility**: Controlled conditions for repeatable experiments

## 🌟 Key Features

### Core Capabilities

#### 1. Massive-Scale Simulation
- Support for 1M+ concurrent agents
- Distributed processing architecture
- Efficient memory management
- Real-time interaction processing

#### 2. AI-Powered Agent Behavior
- Integration with multiple LLM providers
  - OpenAI GPT models (GPT-3.5, GPT-4)
  - Anthropic Claude models (Claude 3 Opus/Sonnet/Haiku, Claude 2/2.1)
  - DeepSeek models (Chat 67B, Coder 33B, MoE 16B)
  - Open-source alternatives (Llama 3)
- Personality modeling
- Dynamic behavior adaptation
- Natural language interaction

#### 3. Platform Simulation
- Twitter-like environment
  - Tweet generation
  - Retweet mechanics
  - Follow/unfollow dynamics
- Reddit-like environment
  - Subreddit simulation
  - Voting systems
  - Comment threads
- Custom platform modeling capability

### Technical Features

#### 1. Modular Architecture
- Pluggable LLM backends
  - OpenAI API integration
  - Anthropic API integration
  - DeepSeek API integration
  - VLLM for open-source models
- Customizable agent behaviors
- Extensible platform models
- Flexible data collection

#### 2. Advanced Analytics
- Real-time metrics
- Network analysis
- Sentiment tracking
- Trend detection
- Custom metric definition

## 💡 System Architecture

### Core Components

1. **Environment Server**
   - Central simulation coordinator
   - State management
   - Event processing
   - Data persistence

2. **Agent Framework**
   - Personality modeling
   - Decision engine
   - Interaction handler
   - Memory management

3. **LLM Integration Layer**
   - Model abstraction
   - Multiple API support (OpenAI, Anthropic)
   - Request handling
   - Response processing
   - Error management

4. **Analytics Engine**
   - Data collection
   - Metric computation
   - Visualization
   - Export capabilities

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- CUDA-compatible GPU (for large-scale simulations)
- 16GB+ RAM (100GB+ for million-agent simulations)
- OpenAI API key (optional)
- Anthropic API key (optional)
- DeepSeek API key (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/AICell-labs/DARWIN.git
cd DARWIN

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -e .
```

### Environment Setup

```bash
# Create .env file
cat << EOF > .env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE_URL=your_openai_base_url  # Optional
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE_URL=your_deepseek_base_url  # Optional
EOF
```

## 📊 Usage Examples

### Basic Twitter Simulation with Mixed Models
```yaml
# config.yaml
model:
  cfgs:
    - model_type: gpt-4  # OpenAI GPT-4
      num: 10
      temperature: 0.7
    - model_type: claude-3-sonnet  # Anthropic Claude 3
      num: 10
      temperature: 0.7
    - model_type: deepseek-chat  # DeepSeek Chat
      num: 10
      temperature: 0.7
    - model_type: llama-3  # Open source model
      num: 10
      server_url: http://your_server:port/v1
      model_path: path/to/model
      temperature: 0.7
```

```bash
python scripts/DARWIN_twitter_basic/twitter_simulation_large.py \
    --config_path config.yaml
```

### Reddit Community Simulation
```bash
python scripts/DARWIN_reddit_basic/reddit_simulation_gpt.py \
    --config_path scripts/DARWIN_reddit_basic/gpt_example.yaml
```

### Million-Agent Simulation
```bash
python scripts/DARWIN_twitter_large_scale/twitter_simulation_1m.py \
    --config_path scripts/DARWIN_twitter_large_scale/twitter_1m.yaml
```

## ⚙️ Advanced Configuration

### Model Selection
```yaml
# config.yaml
model:
  provider: "anthropic"  # or "openai", "vllm"
  name: "claude-3-sonnet"  # or "gpt-4", "llama-3"
  temperature: 0.7
  max_tokens: 150
```

### Agent Configuration
```yaml
agents:
  count: 1000000
  personality_distribution:
    extrovert: 0.3
    introvert: 0.3
    neutral: 0.4
  activity_patterns:
    daily_active: 0.6
    weekly_active: 0.3
    monthly_active: 0.1
```

## 📈 Performance & Scaling

### Resource Requirements

| Scale | Agents | GPU | RAM | Storage |
|-------|--------|-----|-----|---------|
| Small | <1000 | Optional | 16GB | 10GB |
| Medium | <10000 | T4/V100 | 32GB | 50GB |
| Large | <100000 | A100 | 64GB | 200GB |
| Massive | 1M+ | Multiple A100 | 100GB+ | 500GB+ |

### Optimization Tips
- Use batch processing for agent updates
- Implement caching for frequent operations
- Utilize distributed computing for large-scale simulations
- Enable database sharding for improved performance

## 🔬 Research Applications

### Supported Research Areas
1. **Information Diffusion**
   - Viral content analysis
   - Information cascade patterns
   - Influence mapping

2. **Social Dynamics**
   - Opinion formation
   - Group polarization
   - Echo chamber effects

3. **Behavioral Studies**
   - User engagement patterns
   - Content consumption habits
   - Interaction preferences

4. **Network Effects**
   - Community formation
   - Influence networks
   - Trust relationships

## 📁 Project Structure

```
.
├── DARWIN/                # Core package directory
├── src/                  # Source code directory
│   └── DARWIN/           # Main DARWIN package
│       ├── DARWIN_api/          # API implementations
│       ├── DARWIN_config/       # Configuration management
│       ├── DARWIN_core/         # Core functionality
│       ├── DARWIN_data_gen/     # Data generation utilities
│       ├── DARWIN_models/       # Model implementations
│       └── DARWIN_utils/        # Utility functions
├── scripts/              # Simulation scripts
│   ├── DARWIN_reddit_ecommerce/     # Reddit E-commerce simulation
│   ├── DARWIN_reddit_basic/         # Basic Reddit examples
│   ├── DARWIN_reddit_counterfactual/# Reddit counterfactual studies
│   ├── DARWIN_reddit_human_aligned/ # Human-aligned Reddit simulation
│   ├── DARWIN_twitter_basic/        # Basic Twitter examples
│   ├── DARWIN_twitter_standard/     # Standard Twitter simulation
│   ├── DARWIN_twitter_large_scale/  # Million-agent simulation
│   └── DARWIN_deployment/           # Deployment scripts and tools
├── datasets/             # Data storage and datasets
│   ├── DARWIN_ecommerce_data/      # E-commerce related data
│   └── DARWIN_social_media/        # Social media data
│       ├── DARWIN_twitter_data/     # Twitter datasets
│       └── DARWIN_reddit_data/      # Reddit datasets
├── data_generators/      # Data generation tools
│   ├── DARWIN_reddit_generator/     # Reddit data generation
│   └── DARWIN_twitter_generator/    # Twitter data generation
├── logs/                # System logs
├── docs/                # Documentation
│   ├── DARWIN_api_docs/       # API documentation
│   ├── DARWIN_user_guide/     # User guide and tutorials
│   └── DARWIN_developer_docs/ # Developer documentation
├── test/                # Test suite
│   ├── DARWIN_agent_test/          # Agent testing
│   ├── DARWIN_infrastructure_test/ # Infrastructure testing
│   ├── DARWIN_network_test/        # Network testing
│   └── DARWIN_test_data/          # Test data resources
└── visualization/       # Visualization tools
    ├── DARWIN_network_dynamics/        # Network dynamics visualization
    ├── DARWIN_reddit_human_aligned_vis/# Human-aligned Reddit visualization
    ├── DARWIN_reddit_counterfactual_vis/# Counterfactual Reddit visualization
    └── DARWIN_twitter_standard_vis/    # Standard Twitter visualization
```

### Directory Details

#### Core Components
- `DARWIN/`: Core package directory containing the platform implementation
- `src/DARWIN/`: Main source code implementation of the simulation platform
  - `DARWIN_api/`: API implementations for various services
  - `DARWIN_config/`: Configuration management systems
  - `DARWIN_core/`: Core functionality and features
  - `DARWIN_data_gen/`: Data generation utilities
  - `DARWIN_models/`: Model implementations
  - `DARWIN_utils/`: Utility functions and helpers
- `scripts/`: Collection of simulation scripts for different scenarios
  - Reddit simulations with various scales and purposes
  - Twitter simulations including million-agent capability
  - Example implementations and demos

#### Data Management
- `datasets/`: Organized data storage
  - `DARWIN_ecommerce_data/`: E-commerce related datasets
  - `DARWIN_social_media/`: Social media data
    - `DARWIN_twitter_data/`: Twitter datasets
    - `DARWIN_reddit_data/`: Reddit datasets
- `data_generators/`: Tools for generating synthetic data
  - `DARWIN_reddit_generator/`: Reddit data generation tools
  - `DARWIN_twitter_generator/`: Twitter data generation tools

#### Development Tools
- `logs/`: System logs and monitoring data
- `visualization/`: Data visualization and analysis tools
  - Social network graph visualization
  - Metrics and analytics displays

#### Documentation & Testing
- `docs/`: Comprehensive documentation
  - `DARWIN_api_docs/`: API reference and documentation
  - `DARWIN_user_guide/`: User guides and tutorials
    - Contains tutorials and examples
    - Step-by-step guides
  - `DARWIN_developer_docs/`: Developer documentation and guides
- `test/`: Test suite and resources
  - `DARWIN_agent_test/`: Agent behavior testing
  - `DARWIN_infrastructure_test/`: Infrastructure testing
  - `DARWIN_network_test/`: Network simulation testing
  - `DARWIN_test_data/`: Test data and resources

#### Configuration
- `requirements.txt`: Python package dependencies
- `pyproject.toml`: Project metadata and build configuration
- `.env`: Environment configuration (API keys, etc.)


## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Code style and standards
- Pull request process
- Development setup
- Testing requirements

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 📫 Contact & Support

- **Email**: [aicell.labs@gmail.com](mailto:aicell.labs@gmail.com)
- **Twitter**: [@AICell_World](https://twitter.com/AICell_World)

---

*DARWIN is maintained by the AICell Labs team and contributors.*