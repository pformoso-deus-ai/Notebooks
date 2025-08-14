# 🎬 SynapseFlow Demo Guide

This guide provides comprehensive instructions for running demonstrations of the SynapseFlow system during presentations and meetings.

## 🚀 **Quick Start**

### **1. System Demo (Offline)**
```bash
# Run the complete system demonstration
python demo_presentation.py

# Run interactive demo with choices
python demo_presentation.py --interactive
```

### **2. Live API Demo (Online)**
```bash
# Start the API server first
uvicorn src.interfaces.kg_operations_api:app --host 0.0.0.0 --port 8000

# In another terminal, run the live demo
python live_api_demo.py

# Run interactive live demo
python live_api_demo.py --interactive
```

## 📋 **Demo Scripts Overview**

### **`demo_presentation.py` - System Demo**
- **Purpose**: Demonstrates the complete SynapseFlow system capabilities
- **Mode**: Offline (no external dependencies)
- **Use Case**: Presentations, meetings, system overview
- **Features**:
  - Multi-agent collaboration
  - Knowledge graph operations
  - Event-driven architecture
  - REST API functionality
  - Advanced knowledge management

### **`live_api_demo.py` - Live API Demo**
- **Purpose**: Shows real-time API functionality with live endpoints
- **Mode**: Online (requires running API server)
- **Use Case**: Technical demonstrations, API showcases
- **Features**:
  - Live entity CRUD operations
  - Real-time relationship management
  - Batch operations
  - Query execution
  - Event publishing
  - Statistics and monitoring

## 🎯 **Demo Scenarios**

### **Scenario 1: Executive Presentation**
**Duration**: 10-15 minutes
**Audience**: Business stakeholders, executives
**Focus**: Business value, system capabilities

```bash
# Run system demo with business focus
python demo_presentation.py
```

**Key Points to Highlight**:
- Multi-agent collaboration for complex tasks
- Automated knowledge graph creation
- Scalable event-driven architecture
- Enterprise-grade infrastructure

### **Scenario 2: Technical Deep Dive**
**Duration**: 20-30 minutes
**Audience**: Developers, architects, engineers
**Focus**: Technical implementation, API capabilities

```bash
# Start API server
uvicorn src.interfaces.kg_operations_api:app --host 0.0.0.0 --port 8000

# Run live API demo
python live_api_demo.py
```

**Key Points to Highlight**:
- REST API design and endpoints
- Event-driven messaging
- Knowledge graph operations
- Batch processing capabilities

### **Scenario 3: Interactive Workshop**
**Duration**: 45-60 minutes
**Audience**: Mixed technical and business
**Focus**: Hands-on experience, interactive exploration

```bash
# Run interactive demos
python demo_presentation.py --interactive
python live_api_demo.py --interactive
```

**Key Points to Highlight**:
- User choice and exploration
- Real-time system interaction
- Custom scenarios and use cases

## 🔧 **Demo Setup Requirements**

### **System Demo (Offline)**
- Python 3.11+
- SynapseFlow dependencies installed
- No external services required

### **Live API Demo (Online)**
- Python 3.11+
- SynapseFlow dependencies installed
- API server running on port 8000
- Network access to localhost:8000

### **Optional Enhancements**
- RabbitMQ for distributed event bus
- Neo4j for persistent knowledge graph
- Docker for containerized deployment

## 📊 **Demo Content Breakdown**

### **Demo 1: Basic Knowledge Graph Operations**
- Entity creation and management
- Relationship establishment
- Graph querying and traversal
- **Duration**: 3-5 minutes

### **Demo 2: Event-Driven Architecture**
- Event publishing and subscription
- Agent communication patterns
- Distributed messaging
- **Duration**: 3-5 minutes

### **Demo 3: Batch Operations**
- Multiple operation processing
- Transaction management
- Error handling and recovery
- **Duration**: 2-3 minutes

### **Demo 4: REST API Functionality**
- Health monitoring
- Statistics and metrics
- Pagination and filtering
- **Duration**: 3-4 minutes

### **Demo 5: Advanced Features**
- Custom event publishing
- Complex query execution
- System monitoring
- **Duration**: 3-4 minutes

## 🎭 **Presentation Tips**

### **Before the Demo**
1. **Test the system**: Ensure all components work correctly
2. **Prepare data**: Have sample DDA documents ready
3. **Check environment**: Verify Python dependencies and paths
4. **Plan timing**: Allocate time for each demo section

### **During the Demo**
1. **Start simple**: Begin with basic operations
2. **Show progress**: Display real-time results and feedback
3. **Explain concepts**: Connect technical features to business value
4. **Handle errors gracefully**: Use failures as learning opportunities

### **After the Demo**
1. **Summarize capabilities**: Recap key features demonstrated
2. **Discuss use cases**: Connect to audience needs
3. **Q&A session**: Address questions and concerns
4. **Next steps**: Provide follow-up information

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Import Errors**
```bash
# Ensure src directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### **2. API Connection Issues**
```bash
# Check if API server is running
curl http://localhost:8000/health

# Restart API server if needed
pkill -f uvicorn
uvicorn src.interfaces.kg_operations_api:app --host 0.0.0.0 --port 8000
```

#### **3. Permission Issues**
```bash
# Make demo scripts executable
chmod +x demo_presentation.py
chmod +x live_api_demo.py
```

#### **4. Dependency Issues**
```bash
# Install required packages
pip install fastapi uvicorn requests

# Or use uv
uv add fastapi uvicorn requests
```

### **Demo Recovery Strategies**
1. **Fallback to offline demo**: If API server fails
2. **Use sample data**: Pre-loaded examples for consistency
3. **Skip problematic sections**: Focus on working features
4. **Interactive mode**: Let audience choose working demos

## 📚 **Additional Resources**

### **Documentation**
- [Main README](README.md): Complete system overview
- [API Documentation](http://localhost:8000/docs): Interactive API docs
- [Technical Specs](NSL_KNOWLEDGE_MANAGEMENT_SPEC.md): Implementation details

### **Examples**
- [DDA Templates](examples/): Sample domain documents
- [Test Files](tests/): System validation examples
- [CLI Commands](src/interfaces/cli.py): Command-line interface

### **Support**
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and tutorials
- **Community**: Developer discussions and collaboration

## 🎉 **Demo Success Metrics**

### **Technical Success**
- ✅ All demo components execute without errors
- ✅ API endpoints respond correctly
- ✅ Knowledge graph operations complete successfully
- ✅ Event system processes messages properly

### **Business Success**
- ✅ Audience understands system value
- ✅ Technical capabilities are clear
- ✅ Use cases are relevant and compelling
- ✅ Questions are addressed satisfactorily

### **Presentation Success**
- ✅ Demo flows smoothly and on time
- ✅ Key points are effectively communicated
- ✅ Audience engagement is maintained
- ✅ Follow-up actions are identified

---

**Happy Demonstrating! 🚀**

*SynapseFlow: Where neural connections meet data flow, creating intelligent enterprise solutions.* 🧠⚡
