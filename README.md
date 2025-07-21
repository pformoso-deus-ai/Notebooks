# SynapseFlow

> **Synapse** (neural connections) + **Flow** (data movement) = Intelligent agent collaboration

A powerful, enterprise-grade multi-agent system for automated domain knowledge graph creation, data modeling, and intelligent agent collaboration. Built with clean architecture principles and designed for production-scale data engineering workflows.

**SynapseFlow** enables seamless neural-like connections between specialized AI agents, creating a dynamic ecosystem where data flows intelligently through knowledge graphs, domain models, and automated workflows.

## 🚀 **Key Features**

### **🤖 Multi-Agent Neural Network**
- **Data Architect Agent**: Specialized in domain modeling and knowledge graph creation
- **Data Engineer Agent**: Handles data pipeline construction and knowledge graph building
- **Echo Agent**: Provides communication and testing capabilities
- **Extensible Agent Framework**: Easy to add new specialized agents
- **Neural Communication**: Seamless agent-to-agent messaging and collaboration

### **📊 Advanced Modeling Command System**
- **Automated DDA Processing**: Parse Domain Data Architecture documents
- **Knowledge Graph Creation**: Generate and update domain knowledge graphs using Graphiti
- **Intelligent Validation**: Comprehensive document validation and error handling
- **Performance Optimization**: Caching, batch processing, and memory management
- **Enterprise Features**: Backup/rollback, audit trails, and error recovery

### **🔧 Enterprise-Grade Infrastructure**
- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **Command Bus Pattern**: Decoupled command handling and execution
- **Async Processing**: High-performance asynchronous operations
- **Comprehensive Testing**: Unit, integration, and performance test suites
- **Production Monitoring**: Structured logging and observability

## 📋 **Quick Start**

### **Prerequisites**
- Python 3.12+
- Neo4j Database (for knowledge graph operations)
- Graphiti Framework (for graph operations)

### **Installation**

```bash
# Clone the repository
git clone <repository-url>
cd a2a_nsl

# Install dependencies using uv
uv sync

# Install the package in development mode
uv run pip install -e .
```

### **Basic Usage**

#### **1. Modeling Command - Create Knowledge Graphs**

```bash
# Process a DDA document and create a knowledge graph
uv run python -m multi_agent_system model examples/sample_dda.md --domain "Customer Analytics"

# Update existing graph
uv run python -m multi_agent_system model examples/sample_dda.md --update-existing

# Validate only (without creating graph)
uv run python -m multi_agent_system model examples/sample_dda.md --validate-only
```

#### **2. Agent Communication**

```bash
# Send a message to an agent
uv run python -m multi_agent_system send-message data-architect "Create a domain model for e-commerce"

# Execute a command through an agent
uv run python -m multi_agent_system execute-command data-engineer build-kg --domain "Sales Analytics"
```

#### **3. File Operations**

```bash
# Create a new file
uv run python -m multi_agent_system create-file data/models/customer.json

# Read file contents
uv run python -m multi_agent_system read-file data/models/customer.json
```

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │    │  Agent Servers  │    │  Communication  │
│                 │    │                 │    │     Channels    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Command Bus    │
                    │                 │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │    │     Domain      │    │ Infrastructure  │
│     Layer       │    │     Layer       │    │     Layer       │
│                 │    │                 │    │                 │
│ • Commands      │    │ • Models        │    │ • Graphiti      │
│ • Handlers      │    │ • Services      │    │ • Parsers       │
│ • Workflows     │    │ • Business      │    │ • Communication │
│ • Agents        │    │   Logic         │    │ • Storage       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📚 **Core Components**

### **Domain Layer**
- **Commands**: `ModelingCommand`, `FileCommand`, `ShellCommand`
- **Models**: `DDADocument`, `DataEntity`, `Relationship`
- **Services**: Domain business logic and validation

### **Application Layer**
- **Command Handlers**: Process and execute commands
- **Workflows**: Orchestrate complex operations
- **Agents**: Specialized AI agents for different tasks

### **Infrastructure Layer**
- **Graphiti Integration**: Knowledge graph operations
- **Parsers**: DDA document parsing and processing
- **Communication**: Agent-to-agent messaging
- **Storage**: File and data persistence

## 🔍 **Modeling Command Feature**

The Modeling Command is the flagship feature that enables automated domain knowledge graph creation from Domain Data Architecture (DDA) documents.

### **Features**
- **Multi-format Support**: Markdown, YAML, JSON DDA documents
- **Intelligent Parsing**: Extract entities, relationships, and business rules
- **Graph Creation**: Generate knowledge graphs using Graphiti
- **Validation**: Comprehensive document and graph validation
- **Performance**: Caching, batch processing, and optimization
- **Enterprise**: Backup, rollback, and error recovery

### **Example DDA Document**

```markdown
# Customer Analytics Domain

## Domain Information
- **Domain**: Customer Analytics
- **Data Owner**: Chief Analytics Officer
- **Effective Date**: 2024-01-15
- **Stakeholders**: Marketing, Sales, Customer Success

## Business Context
Comprehensive customer analytics platform for understanding customer behavior, preferences, and lifecycle.

## Data Entities

### Customer
- **Description**: Core customer information and profile data
- **Attributes**: customer_id, name, email, phone, address, created_date
- **Business Rules**: 
  - customer_id must be unique
  - email must be valid format
  - created_date cannot be in the future

### Order
- **Description**: Customer purchase orders and transactions
- **Attributes**: order_id, customer_id, order_date, total_amount, status
- **Business Rules**:
  - order_id must be unique
  - customer_id must reference valid customer
  - total_amount must be positive

## Relationships

### Customer -> Order (1:N)
- **Type**: One-to-Many
- **Description**: A customer can have multiple orders
- **Constraints**: 
  - Order must have valid customer_id
  - Customer deletion cascades to orders
```

### **Usage Examples**

```bash
# Create a new knowledge graph
uv run python -m multi_agent_system model customer_analytics_dda.md

# Update existing graph with new information
uv run python -m multi_agent_system model updated_dda.md --update-existing

# Validate document without creating graph
uv run python -m multi_agent_system model dda.md --validate-only

# Specify custom output path
uv run python -m multi_agent_system model dda.md --output-path ./output/graphs/
```

## 🧪 **Testing**

The framework includes comprehensive testing infrastructure:

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test categories
uv run pytest tests/application/ -v
uv run pytest tests/infrastructure/ -v
uv run pytest tests/interfaces/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

### **Test Categories**
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Performance benchmarking
- **Interface Tests**: API and CLI testing

## 🐳 **Docker Support**

Build and run agents in containers:

```bash
# Build and run Data Architect agent
make run ROLE=arx

# Build and run Data Engineer agent  
make run ROLE=d

# Build specific agent
make build ROLE=arx
```

## 📖 **Documentation**

- **[Modeling Command Guide](docs/MODELING_COMMAND_GUIDE.md)**: Comprehensive user guide
- **[Technical Specification](MODELING_COMMAND_SPEC.md)**: Detailed technical docs
- **[Product Requirements](PRD.md)**: Product requirements document
- **[Development Plan](PLAN.md)**: Development roadmap and tasks

## 🔧 **Development**

### **Setup Development Environment**

```bash
# Install dependencies
make install

# Run quality checks
make lint
make format
make test

# Run all checks
make check
```

### **Project Structure**

```
a2a_nsl/
├── src/
│   ├── application/          # Application layer
│   │   ├── agents/          # AI agents
│   │   ├── commands/        # Command handlers
│   │   └── services/        # Application services
│   ├── domain/              # Domain layer
│   │   ├── commands.py      # Command definitions
│   │   ├── dda_models.py    # DDA domain models
│   │   └── agent.py         # Agent base classes
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── graphiti.py      # Graphiti integration
│   │   ├── parsers/         # Document parsers
│   │   └── communication/   # Communication channels
│   └── interfaces/          # Interface layer
│       └── cli.py           # Command-line interface
├── tests/                   # Test suite
├── docs/                    # Documentation
├── examples/                # Example files
└── Makefile                 # Build automation
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

## 📄 **License**

This project is licensed under the [MIT License](LICENSE).

## 🎯 **Roadmap**

- [ ] **Phase 5**: Advanced agent collaboration features
- [ ] **Phase 6**: Machine learning integration
- [ ] **Phase 7**: Cloud deployment and scaling
- [ ] **Phase 8**: Advanced analytics and insights

---

**SynapseFlow**: Empowering intelligent agent collaboration for enterprise data modeling and knowledge graph creation. 🚀

*Where neural connections meet data flow, creating intelligent enterprise solutions.* 🧠⚡

