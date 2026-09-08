Architecture Copilot — Capstone Report

1. Executive Summary
Architecture Copilot is an Agentic AI solution architecture assistant designed to help developers and technical teams make architecture and technology decisions when an experienced solution architect is not immediately available. The system accepts either a Business Requirements Document (BRD) or a natural-language project description and transforms the input into a structured high-level solution architecture.

The application follows a staged agent workflow consisting of requirements analysis, architecture design, technology selection, architecture validation, and optional architecture refinement based on developer or technical-lead feedback. Rather than asking a single model to perform all responsibilities at once, the implementation separates these tasks into specialized agents with dedicated prompts and structured JSON outputs.

The generated architecture contains a project summary, architecture style, components, technology choices, responsibilities, alternatives, rationales, data flows, integrations, security considerations, scalability considerations, assumptions, open questions, and validation findings. The Streamlit interface presents the architecture in a human-readable format and allows the user to either approve it or provide feedback for another refinement cycle.

The system also supports document ingestion for PDF, DOCX, and TXT files, architecture visualization through Mermaid and Graphviz, and architecture export through JSON. A PowerPoint generation service is included to create a presentation-oriented architecture deck, although the current Streamlit interface does not yet expose the PPTX export as a download option.

The implementation uses Python, Streamlit, the Microsoft Agent Framework, an OpenAI-compatible chat client configured for Groq, and an MCP-based architecture catalog connection. The architecture rules explicitly discourage unnecessary complexity for proof-of-concept systems and guide the agents toward practical technologies such as modular monoliths, REST APIs, PostgreSQL, Redis when justified, and Docker.

The current evaluation consists primarily of functional/manual testing of the application workflow. No formal benchmark, independently labeled architecture-quality dataset, comparative accuracy study, or controlled evaluation against human solution architects was performed. Therefore, the project demonstrates an implemented agentic architecture workflow but does not claim measured improvements in architecture quality, technology-selection accuracy, development productivity, or cost.

2. Problem and Users
2.1 Problem Statement
Developers working independently on proof-of-concept projects frequently need to make architecture and technology decisions without access to an experienced solution architect.

This creates several common problems:

Technology choices may be made based on popularity rather than requirements.
Important integrations may be overlooked.
Security and scalability requirements may not be considered early.
Architecture components may not align with the actual business requirements.
Developers may introduce unnecessary complexity such as microservices, Kubernetes, Kafka, or service meshes for small POCs.
Alternative technology options and trade-offs may not be documented.
Architecture decisions may need to be redesigned later when missing requirements are discovered.
Developers may have difficulty converting an unstructured BRD into a coherent technical architecture.
A conventional rule-based script can identify keywords or produce predefined architecture templates, but solution architecture requires interpretation of natural-language requirements, identification of relationships between requirements and components, technology trade-off reasoning, validation, and iterative adaptation.

Architecture Copilot addresses this problem by using multiple specialized AI agents in a structured workflow.

2.2 Target Users
The system is intended for:

Developers — obtain an initial architecture and technology recommendations for POCs and applications.
Technical Leads — review architectural decisions, alternatives, risks, and validation findings.
Solution Architects — use the generated architecture as an initial design or review artifact.
Project Managers — understand the major components, integrations, technology decisions, and open questions.
Clients — review a high-level architecture during project discussions and demonstrations.
Students and POC teams — convert business requirements into a structured architecture without requiring extensive architecture tooling.
2.3 Why an Agentic Approach
The architecture problem contains several distinct reasoning responsibilities.

Requirements need to be extracted before an architecture can be designed. Architecture components then need to be selected based on those requirements. Technologies need to be evaluated against project constraints, and the resulting architecture needs to be independently reviewed for gaps and inconsistencies.

The project therefore uses specialized agents rather than one large prompt:

Requirements Agent
Architecture Agent
Technology Agent
Validation Agent
Refinement Agent
This decomposition provides clearer responsibilities and makes each stage easier to inspect and modify.

3. Scope
3.1 In Scope
The project includes:

Accepting natural-language project descriptions.
Uploading BRDs in PDF, DOCX, and TXT formats.
Extracting textual requirements from uploaded documents.
AI-based requirements analysis.
Identification of functional and non-functional requirements.
Identification of user roles and business workflows.
Identification of data and integration requirements.
Identification of security and performance requirements.
Generation of a high-level architecture.
Selection of architecture style.
Identification of architecture components.
Technology recommendations.
Alternative technology recommendations.
Technology rationale and risk analysis.
Architecture validation.
Identification of missing requirements, issues, risks, and recommendations.
Developer/technical-lead feedback.
Iterative architecture refinement.
Human approval of the proposed architecture.
Markdown rendering of the generated architecture.
Mermaid-based high-level diagrams.
Graphviz architecture diagram generation.
JSON architecture download.
PowerPoint architecture generation service.
MCP integration for an architecture technology/pattern catalog.
JSON extraction and validation of LLM responses.
Architecture complexity rules for POC-oriented designs.
3.2 Out of Scope
The current implementation does not include:

Automatic deployment of the generated architecture.
Generation of production infrastructure such as Terraform or CloudFormation.
Automatic creation of application source code from the architecture.
Live integration with Jira, Azure DevOps, GitHub, GitLab, or other project-management systems.
Automated cloud-cost estimation.
Automated performance benchmarking.
Automated security scanning of the generated architecture.
Formal architecture compliance certification.
A dedicated human solution-architect approval workflow.
Persistent project/version history in a database.
Automated comparison between multiple architecture alternatives.
Formal quantitative evaluation against human-designed architectures.
4. Architecture
The Architecture Copilot follows a sequential multi-agent workflow in which each stage produces structured information for the next stage.

flowchart TD

    U[Developer / Technical Lead / Client]

    U --> UI[Streamlit Interface]

    UI --> INPUT{Input Type}

    INPUT -->|BRD| PARSER[Document Parser]
    INPUT -->|Project Description| TEXT[Natural Language Input]

    PARSER --> REQ[Requirements Agent]
    TEXT --> REQ

    REQ --> ARCH[Architecture Agent]

    ARCH --> TECH[Technology Selection Agent]

    TECH --> VALIDATE[Validation Agent]

    VALIDATE --> INITIAL[Initial Architecture]

    INITIAL --> REVIEW{Developer Review}

    REVIEW -->|Approve| FINAL[Final Architecture]

    REVIEW -->|Feedback| REFINE[Refinement Agent]

    REFINE --> FINAL

    FINAL --> RENDER[Architecture Renderer]

    RENDER --> MERMAID[Mermaid Diagram]
    RENDER --> JSON[JSON Download]

    FINAL --> PPT[PPTX Generation Service]

    ARCH -. architecture patterns .-> MCP[MCP Architecture Catalog]
    TECH -. technology catalog .-> MCP

4.1 Input Layer
The Streamlit application provides two input modes:

Upload BRD
Describe Project
The upload mode supports:

PDF
DOCX
TXT
The document parser extracts plain text from the uploaded file before sending it to the Requirements Agent.

The natural-language mode directly passes the project description to the Requirements Agent.

4.2 Requirements Analysis
The Requirements Agent analyzes the supplied project input and identifies:

Functional requirements
Non-functional requirements
User roles
Business workflows
Data requirements
Integration requirements
Security requirements
Performance requirements
Scalability requirements
Business constraints
Assumptions
Open questions
The prompt explicitly instructs the agent not to invent facts. Missing information is expected to be recorded as assumptions or open questions.

4.3 Architecture Generation
The Architecture Agent receives the structured requirements and creates a high-level architecture.

The agent considers components such as:

Frontend
Backend/API
Authentication
Database
Cache
Search
Booking/order management
Payment
External integrations
File/object storage
Notifications
Background jobs
Monitoring
Deployment
The architecture is intentionally high level. The prompt discourages unnecessary infrastructure complexity unless the requirements justify it.

4.4 Technology Selection
The Technology Agent receives both the requirements and proposed architecture.

For each major technology decision, it produces:

Category
Recommended technology
Description
Alternatives
Rationale
Risks
The selection process considers:

POC development speed
Developer productivity
Requirements
Maintainability
Scalability
Cost
Ecosystem
Operational complexity
Security
Integration requirements
4.5 Architecture Validation
The Validation Agent independently reviews:

Requirements
Architecture
Technology stack
It checks:

Requirement coverage
Architectural consistency
Technology compatibility
Integration completeness
Security
Scalability
Performance
Reliability
Data flow
POC practicality
Unnecessary complexity
The validation result contains:

Overall status
Strengths
Issues
Missing requirements
Risks
Recommendations
The supported validation statuses are:

PASS
PASS_WITH_WARNINGS
FAIL
4.6 Human Feedback and Refinement
The developer or technical lead can review the generated architecture and provide feedback such as:

Changing the backend technology.
Replacing a cloud provider.
Adding an authentication system.
Removing unnecessary infrastructure.
Adding caching.
Supporting additional geographical locations.
Replacing a messaging system.
The Refinement Agent receives:

Original requirements
Current architecture
Current technology stack
Validation results
Developer feedback
It then produces a revised architecture.

The refinement prompt explicitly instructs the agent not to blindly accept feedback. If a requested technology is inappropriate, the agent should consider the trade-off and choose a more suitable alternative.

5. Agent Design
Agent	Responsibility	Input	Output	Termination
Requirements Agent	Analyze project requirements	BRD or project description	Structured requirements JSON	Returns requirements object
Architecture Agent	Design high-level architecture	Requirements	Architecture JSON	Returns architecture object
Technology Agent	Recommend technologies	Requirements + architecture	Technology recommendations JSON	Returns technology object
Validation Agent	Review architecture quality	Requirements + architecture + technology	Validation JSON	Returns validation result
Refinement Agent	Apply developer feedback	Requirements + architecture + technology + validation + feedback	Refined architecture JSON	Returns revised architecture

5.1 Requirements Agent
The Requirements Agent is responsible for converting unstructured business input into architecture-relevant information.

Its primary purpose is to create a structured intermediate representation that downstream agents can consume.

The agent is instructed to avoid inventing facts and to distinguish known information from assumptions and open questions.

5.2 Architecture Agent
The Architecture Agent acts as a Senior Solution Architect.

It converts requirements into a high-level architecture and provides component-level decisions.

Each component contains:

Name
Technology
Responsibility
Alternatives
Rationale
This structure makes architecture decisions explainable rather than presenting only a list of technologies.

5.3 Technology Agent
The Technology Agent evaluates technology decisions separately from the initial architecture generation.

This separation is important because architecture and technology selection are related but distinct decisions.

For example, the architecture may require a relational database, while the Technology Agent can evaluate PostgreSQL against alternatives such as MySQL or another relational database based on project constraints.

5.4 Validation Agent
The Validation Agent provides a second reasoning stage after the architecture and technology decisions have been produced.

Its purpose is not to redesign the architecture but to identify problems and recommendations.

This separation prevents the initial architecture-generation stage from being the only source of architectural reasoning.

5.5 Refinement Agent
The Refinement Agent enables iterative architecture design.

Instead of requiring the user to regenerate an architecture from scratch, the system maintains the previous requirements, architecture, technology stack, and validation result and supplies these together with developer feedback.

This creates a feedback loop:

Requirements
     ↓
Architecture
     ↓
Technology
     ↓
Validation
     ↓
Developer Review
     ↓
Feedback
     ↓
Refinement
     ↓
Final Architecture

6. Data and Knowledge
6.1 Project Input
The primary data source is the project input supplied by the user.

It can originate from:

PDF BRD
DOCX BRD
TXT document
Natural-language project description
The system does not currently persist uploaded project documents in a database.

6.2 Document Parsing
The document_parser.py service provides separate extraction functions:

extract_pdf
extract_docx
extract_txt
parse_document
PDF files are processed using pypdf.

DOCX files are processed using python-docx.

TXT files are decoded as UTF-8 with invalid characters ignored.

The parser uses the file extension to select the appropriate extraction method.

6.3 Structured AI Data
The system defines Pydantic models for important architecture concepts, including:

Requirement
RequirementAnalysis
ArchitectureComponent
Architecture
TechnologyRecommendation
TechnologyStack
ValidationResult
FinalArchitecture
These models provide a typed representation of the expected architecture information.

6.4 Architecture Knowledge through MCP
The project includes an MCP integration named architecture_catalog.

The MCP tool is configured as an MCPStreamableHTTPTool and points to the configured MCP_SERVER_URL.

Its declared purpose is to provide:

Architecture technology catalog and architecture pattern knowledge service.

The current orchestration code does not explicitly invoke the MCP tool from the five agent service functions shown in the implementation. Therefore, MCP integration is present in the architecture but should not be represented as an experimentally validated source of technology recommendations unless the MCP server is actively connected and used during the evaluated execution.

6.5 Architecture Rules
The project includes explicit architecture rules for controlling unnecessary complexity.

For POCs, the rules prefer:

Modular monoliths
REST APIs
PostgreSQL
Redis when justified
Docker
Managed cloud services when appropriate
The rules discourage technologies such as:

Kubernetes
Kafka
RabbitMQ
Service mesh
Microservices
Complex observability stacks
unless the requirements justify them.

For example, Kafka should only be introduced when requirements indicate high-volume event streaming, event replay, or multiple independent consumers.

Similarly, Kubernetes should only be introduced when requirements indicate multiple services, horizontal scaling, production orchestration, or organizational platform requirements.

This rule layer is an important architectural safeguard because it attempts to prevent the LLM from selecting complex infrastructure simply because those technologies are common in enterprise architectures.

7. Implementation
7.1 Technology Stack
The implementation uses:

Layer	Technology
Programming Language	Python
User Interface	Streamlit
Agent Framework	Microsoft Agent Framework
LLM Client	OpenAI-compatible Chat Completion Client
Model Provider	Groq
Default Model	openai/gpt-oss-120b
Document Parsing	pypdf, python-docx
Structured Data	Pydantic
Architecture Diagram	Mermaid / Graphviz
Presentation Export	python-pptx
External Knowledge Interface	MCP
Configuration	python-dotenv

7.2 LLM Configuration
The LLM client is implemented in app/core/llm.py.

The application reads:

GROQ_API_KEY
GROQ_MODEL
GROQ_BASE_URL
from environment configuration.

The default model configured by the application is:

openai/gpt-oss-120b

The default API endpoint is:

https://api.groq.com/openai/v1

The application uses an OpenAI-compatible client configured with the Groq endpoint.

7.3 Architecture Service Orchestration
The main orchestration is implemented in architecture_service.py.

The initial architecture workflow is:

analyze_requirements()
        ↓
generate_architecture()
        ↓
recommend_technology()
        ↓
validate_architecture()
        ↓
return initial architecture

The refinement workflow is:

initial requirements
        +
initial architecture
        +
technology stack
        +
validation
        +
developer feedback
        ↓
refine_architecture()
        ↓
final architecture

The orchestration is sequential because each downstream stage depends on the output of the previous stage.

7.4 Prompt Engineering
Each agent has a dedicated system-level prompt.

The prompts enforce structured JSON output and define the expected responsibilities of the agent.

The architecture prompt also contains explicit guidance to avoid unnecessary complexity.

For example, it instructs the architecture agent not to introduce microservices, Kafka, Kubernetes, service meshes, or complex observability platforms unless the requirements justify them.

The refinement prompt further instructs the model to preserve consistency between:

Requirements
Architecture
Technology
Integrations
Data flow
Security
Scalability
7.5 JSON Response Handling
LLM responses are not assumed to always be perfectly formatted.

The extract_json() utility provides defensive parsing.

It attempts to:

Remove Markdown code fences.
Parse the entire response as JSON.
Extract a JSON object if additional text exists.
Extract a JSON array if necessary.
Raise a detailed error if parsing fails.
This improves resilience when the model returns JSON surrounded by formatting or explanatory text.

The individual agents also validate that the result is a dictionary and, where required, contains expected fields such as recommendations.

7.6 User Interface
The Streamlit interface provides:

Application title and description.
BRD upload.
Natural-language project input.
Architecture generation.
Architecture visualization.
Developer feedback input.
Architecture refinement.
Architecture approval.
Final architecture display.
JSON download.
The application stores intermediate results in Streamlit session state:

input_mode
initial_result
final_result
This allows the architecture review and refinement workflow to remain within a single user session.

7.7 Architecture Rendering
The render_architecture() function transforms the structured architecture into Markdown.

The output includes:

Project summary
Architecture style
High-level architecture
Architecture components
Data flow
External integrations
Technology stack
Security considerations
Scalability considerations
Architecture validation
This provides a presentation-friendly representation without requiring the user to inspect raw JSON.

7.8 Mermaid Diagram
The formatting utility also generates a simple Mermaid diagram.

The current implementation attempts to identify:

Frontend
Backend/API
Database
Cache
from the component names.

The generated high-level flow is approximately:

Users
  ↓
Frontend
  ↓ HTTPS / REST
Backend
  ↓
Database

If a cache component is detected, it is additionally connected to the backend.

This diagram is intentionally simplified and is intended for high-level presentation rather than deployment-level infrastructure design.

7.9 Graphviz Diagram
The project also contains a separate Graphviz-based diagram service.

generate_architecture_diagram() creates a Graphviz Digraph, adds architecture components as nodes, and connects the components sequentially.

The output is rendered as a PNG file.

The Graphviz implementation is therefore another visualization path alongside Mermaid.

7.10 PowerPoint Export
The ppt_service.py module provides PowerPoint generation using python-pptx.

The current implementation creates four slides:

Architecture Copilot title slide.
Architecture overview.
Technology decisions.
Architecture validation.
The generated presentation is returned as bytes through an in-memory BytesIO object.

The service exists in the project, but the provided Streamlit interface currently exposes JSON download rather than directly connecting create_architecture_ppt() to a PPTX download button.

8. Design Decisions
Decision 1: Use a Multi-Agent Workflow
Selected approach: Specialized Requirements, Architecture, Technology, Validation, and Refinement Agents.

Rejected alternative: One large prompt that performs the complete architecture process.

A single prompt would reduce implementation complexity but would combine requirements extraction, architecture design, technology selection, validation, and refinement into one operation.

The selected approach gives each responsibility a dedicated prompt and structured output. This makes the workflow easier to understand, debug, and extend.

Decision 2: Use Sequential Agent Orchestration
Selected approach: Each stage consumes the structured output from the previous stage.

Rejected alternative: Fully independent agents producing competing architectures simultaneously.

Architecture generation depends on requirements, technology selection depends on architecture, and validation depends on both architecture and technology.

Sequential orchestration therefore matches the dependency structure of the problem.

Decision 3: Separate Architecture and Technology Selection
Selected approach: Use separate Architecture and Technology Agents.

Rejected alternative: Have the Architecture Agent make all technology decisions without a separate review stage.

Separating the decisions allows technology recommendations to be evaluated against requirements, cost, maintainability, scalability, security, ecosystem, and operational complexity.

Decision 4: Add a Dedicated Validation Agent
Selected approach: Validate the architecture after technology selection.

Rejected alternative: Trust the initial architecture-generation response.

Architecture generation can omit requirements or introduce unnecessary components.

The Validation Agent provides an independent reasoning stage that explicitly checks requirement coverage, compatibility, security, scalability, reliability, and unnecessary complexity.

Decision 5: Add Iterative Refinement
Selected approach: Allow developers to submit feedback and regenerate the architecture.

Rejected alternative: Generate one architecture and require the user to restart the process for every change.

Architecture is inherently iterative.

Developers may know constraints that were not present in the original BRD, such as an existing cloud platform, preferred backend framework, authentication provider, or infrastructure restriction.

The refinement stage allows this knowledge to be incorporated without discarding the previous analysis.

Decision 6: Prefer Simple POC Architectures
Selected approach: Explicit architecture-complexity rules.

Rejected alternative: Allow the LLM to freely select any popular architecture technology.

The rules reduce the risk of overengineering.

A POC generally does not require Kubernetes, service meshes, Kafka, or microservices unless the requirements actually justify them.

Decision 7: Support Both BRD and Natural-Language Input
Selected approach: Provide document upload and direct project description.

Rejected alternative: Require every user to prepare a structured requirements file.

Allowing both modes makes the system usable when a formal BRD exists and when a developer only has an informal project idea.

9. Evaluation
9.1 Evaluation Approach
The current evaluation focuses on functional behavior and manual execution of the application rather than formal architecture-quality benchmarking.

The workflow can be exercised from project input through:

Input
  ↓
Requirements
  ↓
Architecture
  ↓
Technology
  ↓
Validation
  ↓
Approval / Feedback
  ↓
Refinement

The project does not currently contain an independently labeled benchmark dataset for evaluating whether generated architectures are objectively correct.

9.2 Functional Evaluation Areas
The implementation can be evaluated across the following areas:

Evaluation Area	Purpose
BRD Parsing	Confirm PDF, DOCX, and TXT input can be converted into text
Requirements Analysis	Verify structured requirement extraction
Architecture Generation	Verify architecture JSON is produced
Technology Selection	Verify recommendations, alternatives, rationale, and risks
Validation	Verify validation status and findings are returned
Refinement	Verify developer feedback can modify the architecture
Approval	Verify the initial architecture can be accepted without refinement
Rendering	Verify structured architecture is converted into readable Markdown
Mermaid Generation	Verify a high-level architecture diagram can be produced
JSON Export	Verify the final architecture can be downloaded
PPTX Service	Verify a presentation can be generated by the dedicated service

9.3 Structured Output Validation
Each agent expects a JSON response.

The implementation contains defensive parsing through extract_json() and explicit checks for dictionary responses.

The Technology Agent additionally verifies that the response contains the recommendations field.

The architecture service also verifies that the Refinement Agent returns an architecture field.

These checks reduce the chance that malformed model output silently propagates through the workflow.

9.4 Limitations of the Evaluation
The current implementation does not provide:

Human-labeled architecture correctness scores.
Precision or recall for requirement extraction.
Technology recommendation accuracy.
Architecture quality scoring.
Independent expert evaluation.
Comparison against a single-agent baseline.
Comparison against a rule-based architecture generator.
Quantitative developer productivity measurements.
Formal latency benchmarking.
Formal cost benchmarking across multiple runs.
Production deployment measurements.
Therefore, the project demonstrates functional implementation of the agentic workflow but does not establish statistically measured superiority over alternative architecture-generation approaches.

10. Results
The implemented system demonstrates an end-to-end architecture-generation workflow:

BRD / Project Description
          ↓
Requirements Analysis
          ↓
High-Level Architecture
          ↓
Technology Recommendations
          ↓
Architecture Validation
          ↓
Developer Feedback
          ↓
Architecture Refinement
          ↓
Final Architecture

The main qualitative implementation findings are:

The system can transform unstructured project input into structured architecture information.
Requirements analysis is separated from architecture design.
Technology recommendations include alternatives and rationale rather than only technology names.
Architecture validation is performed as a separate stage.
Developer feedback can be incorporated into a subsequent refinement cycle.
The architecture complexity rules discourage unnecessary infrastructure for POCs.
PDF, DOCX, and TXT document inputs are supported.
The generated architecture can be rendered into Markdown and downloaded as JSON.
Mermaid and Graphviz provide architecture visualization mechanisms.
A PowerPoint generation service is implemented for presentation-oriented output.
An MCP integration is provided for connecting an architecture catalog/pattern knowledge service.
10.1 Qualitative Workflow Result
The resulting system is not limited to producing a static architecture diagram. It creates an architecture decision artifact containing multiple layers of information:

Project Summary
       ↓
Requirements
       ↓
Architecture Style
       ↓
Components
       ↓
Technology Choices
       ↓
Alternatives
       ↓
Rationale
       ↓
Data Flow
       ↓
Integrations
       ↓
Security
       ↓
Scalability
       ↓
Validation
       ↓
Developer Feedback
       ↓
Changes

This structure makes the output more useful for technical discussions than a diagram alone.

10.2 Evaluation Result Interpretation
No numerical quality result is claimed because the project does not contain a formal architecture benchmark.

In particular, the implementation should not be interpreted as proving that the generated architecture is always correct or production-ready.

The system is better characterized as an AI-assisted architecture starting point that can accelerate architectural analysis and provide structured decision support while retaining human review.

The complete workflow can be summarized as follows:
                    ┌─────────────────────┐
                    │  BRD / Project Idea │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Requirements Agent  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Architecture Agent  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Technology Agent    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Validation Agent    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Initial Architecture│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Developer Review    │
                    └───────┬───────┬─────┘
                            │       │
                     Approve│       │Feedback
                            │       │
                            │       ▼
                            │ ┌──────────────────┐
                            │ │ Refinement Agent │
                            │ └────────┬─────────┘
                            │          │
                            └────┬─────┘
                                 ▼
                    ┌─────────────────────┐
                    │ Final Architecture  │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
           Markdown         JSON          PPTX
           / Mermaid       Download       Service
