ARCHITECTURE_RULES = """

Architecture complexity rules:

For a POC:

Prefer:
- Modular monolith
- REST APIs
- PostgreSQL
- Redis only when justified
- Docker
- Managed cloud services where appropriate

Avoid unless justified:
- Kubernetes
- Kafka
- RabbitMQ
- Service mesh
- Microservices
- Distributed tracing
- Complex observability stacks

Introduce these technologies only if requirements indicate:

Kafka:
- high-volume event streaming
- event replay
- many independent consumers

RabbitMQ:
- reliable asynchronous jobs
- task queues
- workflow messaging

Redis:
- caching
- session storage
- rate limiting
- distributed locking

Kubernetes:
- multiple services
- horizontal scaling
- production orchestration requirements
- organizational platform standards

Microservices:
- independent deployment
- strong service boundaries
- organizational/team scaling
- independent scaling requirements
"""
