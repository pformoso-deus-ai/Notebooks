# Jinja2 Template Implementation Note

## Future Enhancement: Jinja2 Templates for DDA Generation

### Current State
- ✅ CLI template generator with basic string formatting
- ✅ 20+ DDA documents generated for autoimmune and inflammatory bowel disease domains
- ✅ Relationship parsing working correctly
- ✅ SynapseFlow successfully creating knowledge graphs with relationships

### Proposed Jinja2 Implementation

#### Benefits of Jinja2 Templates
1. **Dynamic Content Generation**: More sophisticated template logic
2. **Reusable Components**: Template inheritance and includes
3. **Conditional Logic**: Different sections based on domain type
4. **Variable Substitution**: Cleaner syntax than f-strings
5. **Template Validation**: Better error handling

#### Implementation Plan

```python
# Future implementation structure
from jinja2 import Environment, FileSystemLoader

class Jinja2DDATemplateGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates/dda'))
    
    def generate_dda(self, domain_config: Dict[str, Any]) -> str:
        template = self.env.get_template('base_dda.j2')
        return template.render(**domain_config)
```

#### Template Structure
```
templates/
└── dda/
    ├── base_dda.j2              # Base template with all sections
    ├── medical_domain.j2        # Medical-specific sections
    ├── research_domain.j2       # Research-specific sections
    ├── clinical_trial.j2        # Clinical trial specific
    └── components/
        ├── entities.j2          # Entity definitions
        ├── relationships.j2     # Relationship definitions
        ├── governance.j2        # Governance requirements
        └── quality.j2           # Data quality requirements
```

#### Example Jinja2 Template
```jinja2
# base_dda.j2
# Data Delivery Agreement (DDA) - {{ domain_name }}

## Document Information
- **Domain**: {{ domain_name }}
- **Stakeholders**: {{ stakeholders | join(', ') }}
- **Data Owner**: {{ data_owner }}
- **Effective Date**: {{ effective_date }}
- **Review Cycle**: {{ review_cycle }}

## Business Context
{{ business_context }}

## Data Entities
{% for entity in entities %}
### {{ entity.name }}
- **Description**: {{ entity.description }}
- **Key Attributes**:
{% for attr in entity.attributes %}
  - {{ attr.name }}{% if attr.is_primary %} (Primary Key){% endif %}{% if attr.is_foreign %} (Foreign Key){% endif %}
{% endfor %}
- **Business Rules**:
{% for rule in entity.business_rules %}
  - {{ rule }}
{% endfor %}
{% endfor %}

## Relationships
{% for category in relationship_categories %}
### {{ category.name }}
{% for rel in category.relationships %}
- **{{ rel.source }}** → **{{ rel.target }}** ({{ rel.type }})
  - {{ rel.description }}
{% endfor %}
{% endfor %}
```

#### CLI Integration
```bash
# Future enhanced CLI commands
uv run python -m multi_agent_system create-template --name "Crohn's Disease" --type medical
uv run python -m multi_agent_system create-template --name "Clinical Trial" --type research
uv run python -m multi_agent_system create-template --name "Biobank" --type biobank
```

#### Benefits for Current Use Case
1. **Autoimmune Disease Templates**: Pre-configured entities and relationships
2. **Inflammatory Bowel Disease Templates**: Specialized sections for IBD
3. **Research Domain Templates**: Clinical trial and biobank specific content
4. **Validation**: Template-level validation of required fields
5. **Consistency**: Ensures all DDA documents follow the same structure

### Migration Path
1. Keep current string-based templates for backward compatibility
2. Add Jinja2 as an optional template engine
3. Gradually migrate existing templates to Jinja2
4. Add template validation and testing

### Dependencies to Add
```toml
# pyproject.toml
[tool.poetry.dependencies]
jinja2 = "^3.1.0"
```

This enhancement would make DDA generation more robust, maintainable, and flexible while preserving all current functionality. 