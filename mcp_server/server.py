from fastmcp import FastMCP


mcp = FastMCP(
    name="Architecture Copilot MCP"
)


# ============================================================
# TECHNOLOGY CATALOG
# ============================================================

TECHNOLOGY_CATALOG = {

    "frontend": [
        {
            "technology": "React + TypeScript",
            "description": "Component-based frontend development.",
            "alternatives": [
                "Angular",
                "Vue.js",
                "Next.js",
            ],
        }
    ],

    "backend": [
        {
            "technology": "FastAPI",
            "description": "High-performance Python API framework.",
            "alternatives": [
                "Django",
                "Flask",
                "Node.js + NestJS",
            ],
        }
    ],

    "database": [
        {
            "technology": "PostgreSQL",
            "description": "Relational database with strong ACID transactions.",
            "alternatives": [
                "MySQL",
                "MongoDB",
                "MariaDB",
            ],
        }
    ],

    "cache": [
        {
            "technology": "Redis",
            "description": "In-memory datastore for caching and distributed locking.",
            "alternatives": [
                "Memcached",
            ],
        }
    ],

    "payments": [
        {
            "technology": "Razorpay",
            "description": "Indian payment gateway supporting online payments and webhooks.",
            "alternatives": [
                "PayU",
                "Stripe",
            ],
        }
    ],

    "maps": [
        {
            "technology": "Google Maps Platform",
            "description": "Maps, geocoding and location services.",
            "alternatives": [
                "Mapbox",
                "HERE Maps",
                "OpenStreetMap",
            ],
        }
    ],

    "storage": [
        {
            "technology": "Amazon S3",
            "description": "Object storage for images, documents and generated files.",
            "alternatives": [
                "Azure Blob Storage",
                "Google Cloud Storage",
                "MinIO",
            ],
        }
    ],

    "notifications": [
        {
            "technology": "Twilio",
            "description": "SMS and communication platform.",
            "alternatives": [
                "AWS SNS",
                "SendGrid",
            ],
        }
    ],
}


# ============================================================
# ARCHITECTURE PATTERNS
# ============================================================

ARCHITECTURE_PATTERNS = {

    "travel": {
        "pattern": "Modular Monolith",
        "reason": (
            "Suitable for a POC because booking, inventory, "
            "payments and user management can be maintained "
            "as separate modules without microservice overhead."
        ),
    },

    "booking": {
        "pattern": "Modular Monolith",
        "reason": (
            "Booking systems require transactional consistency "
            "and benefit from keeping inventory and booking "
            "operations within a simple transactional boundary."
        ),
    },

    "ecommerce": {
        "pattern": "Modular Monolith",
        "reason": (
            "Provides rapid development while keeping clear "
            "domain boundaries for future service extraction."
        ),
    },

    "iot": {
        "pattern": "Event-driven Architecture",
        "reason": (
            "Large volumes of asynchronous device events "
            "justify event-driven processing."
        ),
    },

    "saas": {
        "pattern": "Modular Monolith",
        "reason": (
            "Allows rapid POC development while preserving "
            "clear module boundaries."
        ),
    },
}


# ============================================================
# MCP TOOL: TECHNOLOGY OPTIONS
# ============================================================

@mcp.tool
def get_technology_options(
    category: str,
) -> list:

    """
    Return technology options for an architecture category.
    """

    return TECHNOLOGY_CATALOG.get(
        category.lower().strip(),
        [],
    )


# ============================================================
# MCP TOOL: COMPARE TECHNOLOGIES
# ============================================================

@mcp.tool
def compare_technologies(
    technology_a: str,
    technology_b: str,
) -> dict:

    """
    Compare two technologies.
    """

    a = technology_a.lower()
    b = technology_b.lower()

    if (
        "postgres" in a
        and "mongo" in b
    ) or (
        "mongo" in a
        and "postgres" in b
    ):
        return {
            "comparison": "PostgreSQL vs MongoDB",
            "postgresql": (
                "Best for relational data, transactions, "
                "complex queries and strong consistency."
            ),
            "mongodb": (
                "Best for flexible document-oriented "
                "data models."
            ),
            "recommendation": (
                "Prefer PostgreSQL for booking and payment "
                "systems where transactional consistency matters."
            ),
        }

    if (
        "redis" in a
        and "memcached" in b
    ) or (
        "memcached" in a
        and "redis" in b
    ):
        return {
            "comparison": "Redis vs Memcached",
            "redis": (
                "Supports caching, TTL, atomic operations, "
                "distributed locking and richer data structures."
            ),
            "memcached": (
                "Simple and lightweight distributed caching."
            ),
            "recommendation": (
                "Prefer Redis when caching and distributed "
                "locking are both required."
            ),
        }

    if (
        "kafka" in a
        and "rabbitmq" in b
    ) or (
        "rabbitmq" in a
        and "kafka" in b
    ):
        return {
            "comparison": "Kafka vs RabbitMQ",
            "kafka": (
                "Best for high-volume event streaming, "
                "event replay and distributed data pipelines."
            ),
            "rabbitmq": (
                "Best for traditional asynchronous messaging "
                "and task queues."
            ),
            "recommendation": (
                "Prefer RabbitMQ for simple POC background "
                "processing unless event streaming is required."
            ),
        }

    if (
        "fastapi" in a
        and "nestjs" in b
    ) or (
        "nestjs" in a
        and "fastapi" in b
    ):
        return {
            "comparison": "FastAPI vs NestJS",
            "fastapi": (
                "Python API framework with strong performance "
                "and rapid development."
            ),
            "nestjs": (
                "TypeScript backend framework with strong "
                "modular architecture."
            ),
            "recommendation": (
                "Prefer FastAPI when the organization is "
                "Python-centric or AI integration is important."
            ),
        }

    return {
        "comparison": f"{technology_a} vs {technology_b}",
        "message": (
            "No predefined comparison is currently "
            "available in the MCP technology catalog."
        ),
    }


# ============================================================
# MCP TOOL: ARCHITECTURE PATTERN
# ============================================================

@mcp.tool
def get_architecture_pattern(
    project_type: str,
) -> dict:

    """
    Return a recommended architecture pattern.
    """

    project_type = project_type.lower().strip()

    for key, pattern in ARCHITECTURE_PATTERNS.items():

        if key in project_type:

            return pattern

    return {
        "pattern": "Modular Monolith",
        "reason": (
            "A good default for a POC because it minimizes "
            "operational complexity while preserving "
            "clear module boundaries."
        ),
    }


# ============================================================
# MCP TOOL: BOOKING ARCHITECTURE GUIDANCE
# ============================================================

@mcp.tool
def get_booking_architecture_guidance() -> dict:

    """
    Architecture guidance for booking/rental systems.
    """

    return {
        "inventory": (
            "Maintain bike availability in PostgreSQL "
            "as the source of truth."
        ),
        "booking": (
            "Use database transactions to prevent "
            "double booking."
        ),
        "locking": (
            "Redis distributed locking can be introduced "
            "when concurrent booking volume requires it."
        ),
        "payment": (
            "Use payment gateway webhooks and maintain "
            "payment status independently from booking status."
        ),
        "recommendation": (
            "For a POC, PostgreSQL + FastAPI + Redis "
            "is sufficient. Avoid microservices and Kafka "
            "unless requirements justify them."
        ),
    }


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8001,
    )
