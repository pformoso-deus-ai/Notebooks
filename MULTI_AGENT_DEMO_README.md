# 🎬 Multi-Agent DDA Demo Guide

This guide provides comprehensive instructions for running the **Multi-Agent DDA Demo** that showcases the complete SynapseFlow system working with Data Delivery Agreements.

## 🚀 **Quick Start**

### **1. Basic Demo (Complete Workflow)**
```bash
# Run the complete multi-agent demonstration
python multi_agent_dda_demo.py
```

### **2. Interactive Demo (Choose Your Path)**
```bash
# Run interactive demo with user choices
python multi_agent_dda_demo.py --interactive
```

### **3. Specific DDA File Demo**
```bash
# Use a specific DDA file
python multi_agent_dda_demo.py examples/crohns_disease_dda.md

# Use specific file with interactive mode
python multi_agent_dda_demo.py examples/sample_dda.md --interactive
```

## 📋 **Demo Overview**

The **Multi-Agent DDA Demo** demonstrates the complete SynapseFlow workflow:

### **🤖 Agents Involved**
- **Knowledge Manager Agent**: Handles complex operations, validation, and conflict resolution
- **Data Architect Agent**: Processes DDA documents and creates domain models
- **Data Engineer Agent**: Implements and validates the models

### **🔄 Workflow Demonstrated**
1. **Agent Registration**: Agents register their capabilities in the knowledge graph
2. **DDA Processing**: Document parsing and entity/relationship extraction
3. **Knowledge Graph Creation**: Building the domain model
4. **Agent Collaboration**: Communication and task handoff between agents
5. **Event-Driven Communication**: Asynchronous messaging via event bus
6. **Validation & Conflict Resolution**: Advanced knowledge management features

## 🎯 **Demo Scenarios**

### **Scenario 1: Complete Workflow Demo**
**Duration**: 15-20 minutes
**Audience**: Technical and business stakeholders
**Focus**: End-to-end system capabilities

```bash
python multi_agent_dda_demo.py
```

**What You'll See**:
- All agents working together seamlessly
- DDA document processing in real-time
- Knowledge graph creation and updates
- Agent communication patterns
- Event-driven architecture in action

### **Scenario 2: Interactive Exploration**
**Duration**: 20-30 minutes
**Audience**: Developers, architects, technical teams
**Focus**: Deep dive into specific components

```bash
python multi_agent_dda_demo.py --interactive
```

**What You'll See**:
- Choose which aspects to explore
- Step-by-step breakdown of each process
- Detailed agent interaction patterns
- Custom DDA file processing

### **Scenario 3: Specific Domain Demo**
**Duration**: 10-15 minutes
**Audience**: Domain experts, business analysts
**Focus**: Real-world DDA processing

```bash
python multi_agent_dda_demo.py examples/crohns_disease_dda.md
```

**What You'll See**:
- Healthcare domain processing
- Medical entity extraction
- Clinical relationship modeling
- Domain-specific validation

## 📚 **Available DDA Files**

The demo automatically discovers DDA files in the `examples/` directory:

### **Healthcare Domain DDAs**
- `crohns_disease_dda.md` - Inflammatory bowel disease management
- `multiple_sclerosis_management_dda.md` - MS treatment and monitoring
- `lupus_management_dda.md` - Systemic lupus management
- `rheumatoid_arthritis_management_dda.md` - RA treatment protocols
- `type_1_diabetes_management_dda.md` - Diabetes care management

### **Business Domain DDAs**
- `sample_dda.md` - Customer analytics domain
- `autoimmune_disease_dda.md` - Medical research domain
- `ibd_template_dda.md` - Inflammatory bowel disease template

### **Research Domain DDAs**
- `autoimmune_disease_biobank_dda.md` - Biobank data management
- `autoimmune_disease_clinical_trials_dda.md` - Clinical trial data
- `inflammatory_bowel_disease_research_dda.md` - IBD research data

## 🔧 **Demo Setup Requirements**

### **System Requirements**
- Python 3.11+
- SynapseFlow dependencies installed
- No external services required (uses in-memory backend)

### **Dependencies**
```bash
# Install required packages
pip install asyncio pathlib

# Or use uv
uv add asyncio pathlib
```

### **File Structure**
```
examples/
├── crohns_disease_dda.md          # Healthcare domain
├── sample_dda.md                  # Business domain
├── multiple_sclerosis_management_dda.md
├── lupus_management_dda.md
└── ... (other DDA files)

multi_agent_dda_demo.py            # Main demo script
MULTI_AGENT_DEMO_README.md         # This guide
```

## 📊 **Demo Content Breakdown**

### **Demo 1: Agent Registration and Discovery**
- **Duration**: 2-3 minutes
- **Content**: Agent initialization, capability registration, permission matrix
- **Key Points**: 
  - Agent roles and responsibilities
  - Permission-based access control
  - Service discovery mechanisms

### **Demo 2: DDA Document Processing**
- **Duration**: 3-4 minutes
- **Content**: Document selection, parsing, entity extraction
- **Key Points**:
  - DDA structure understanding
  - Entity and relationship discovery
  - Domain and stakeholder identification

### **Demo 3: Knowledge Graph Creation**
- **Duration**: 3-4 minutes
- **Content**: Data Architect processing, model creation, graph updates
- **Key Points**:
  - Domain model generation
  - Knowledge graph population
  - Entity relationship mapping

### **Demo 4: Agent Collaboration and Communication**
- **Duration**: 3-4 minutes
- **Content**: Task handoff, work requests, escalation
- **Key Points**:
  - Inter-agent messaging
  - Task delegation patterns
  - Escalation workflows

### **Demo 5: Event-Driven Communication**
- **Duration**: 2-3 minutes
- **Content**: Event publishing, subscription, processing
- **Key Points**:
  - Asynchronous communication
  - Event routing and handling
  - System decoupling

### **Demo 6: Validation and Conflict Resolution**
- **Duration**: 3-4 minutes
- **Content**: Validation rules, conflict detection, reasoning
- **Key Points**:
  - Data quality assurance
  - Conflict detection algorithms
  - Intelligent reasoning capabilities

## 🎭 **Presentation Tips**

### **Before the Demo**
1. **Test the system**: Ensure all components work correctly
2. **Choose DDA files**: Select domain-relevant examples for your audience
3. **Plan timing**: Allocate time for each demo section
4. **Prepare questions**: Anticipate audience inquiries

### **During the Demo**
1. **Start with overview**: Explain the multi-agent architecture
2. **Show real-time processing**: Let the audience see agents working
3. **Highlight collaboration**: Emphasize agent communication patterns
4. **Demonstrate escalation**: Show complex operation handling

### **After the Demo**
1. **Summarize capabilities**: Recap key features demonstrated
2. **Discuss use cases**: Connect to audience domain needs
3. **Q&A session**: Address technical and business questions
4. **Next steps**: Provide follow-up information

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Import Errors**
```bash
# Ensure src directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or run from project root
cd /path/to/Notebooks
python multi_agent_dda_demo.py
```

#### **2. DDA File Not Found**
```bash
# Check examples directory
ls examples/*_dda.md

# Verify file paths
python multi_agent_dda_demo.py examples/sample_dda.md
```

#### **3. Agent Initialization Errors**
```bash
# Check dependencies
pip install -r requirements.txt

# Verify Python version
python --version  # Should be 3.11+
```

#### **4. Communication Channel Issues**
```bash
# Reset demo environment
python multi_agent_dda_demo.py --interactive
# Choose Demo 1 to reinitialize agents
```

### **Demo Recovery Strategies**
1. **Restart specific demo**: Use interactive mode to retry failed sections
2. **Use different DDA**: Try alternative domain examples
3. **Skip problematic sections**: Focus on working features
4. **Fallback to basic demo**: Run core functionality only

## 📈 **Demo Success Metrics**

### **Technical Success**
- ✅ All agents initialize correctly
- ✅ DDA files are processed successfully
- ✅ Knowledge graph is created and updated
- ✅ Agent communication works properly
- ✅ Event system processes messages correctly

### **Business Success**
- ✅ Audience understands multi-agent value
- ✅ DDA processing workflow is clear
- ✅ Collaboration patterns are demonstrated
- ✅ Use cases are relevant and compelling

### **Presentation Success**
- ✅ Demo flows smoothly and on time
- ✅ Key concepts are effectively communicated
- ✅ Audience engagement is maintained
- ✅ Questions are addressed satisfactorily

## 🔍 **Advanced Demo Features**

### **Custom DDA Processing**
```bash
# Process your own DDA file
python multi_agent_dda_demo.py /path/to/your_dda.md
```

### **Specific Demo Sections**
```bash
# Run only specific demos in interactive mode
python multi_agent_dda_demo.py --interactive
# Then choose specific demo numbers
```

### **Integration with CLI Commands**
```bash
# Use the demo in conjunction with CLI commands
python -m multi_agent_system model examples/sample_dda.md
python multi_agent_dda_demo.py examples/sample_dda.md
```

## 📚 **Additional Resources**

### **Documentation**
- [Main README](README.md): Complete system overview
- [Demo README](DEMO_README.md): General demo guide
- [Technical Specs](NSL_KNOWLEDGE_MANAGEMENT_SPEC.md): Implementation details

### **Examples**
- [DDA Templates](examples/): Sample domain documents
- [CLI Commands](src/interfaces/cli.py): Command-line interface
- [Agent Code](src/application/agents/): Agent implementations

### **Support**
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and tutorials
- **Community**: Developer discussions and collaboration

## 🎉 **Demo Completion Checklist**

### **Before Presentation**
- [ ] System tested and working
- [ ] DDA files available and accessible
- [ ] Demo script tested successfully
- [ ] Timing planned and rehearsed
- [ ] Backup plans prepared

### **During Presentation**
- [ ] Multi-agent system initialized
- [ ] DDA processing demonstrated
- [ ] Knowledge graph creation shown
- [ ] Agent collaboration displayed
- [ ] Event system demonstrated
- [ ] Validation features showcased

### **After Presentation**
- [ ] Capabilities summarized
- [ ] Use cases discussed
- [ ] Questions addressed
- [ ] Next steps identified
- [ ] Feedback collected

---

**Happy Multi-Agent Demonstrating! 🚀**

*SynapseFlow: Where neural connections meet data flow, creating intelligent enterprise solutions.* 🧠⚡
