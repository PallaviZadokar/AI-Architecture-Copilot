import asyncio

from app.agents.requirements_agent import analyze_requirements


async def main():

    project = """
    Build an e-commerce application.

    Users should be able to register, login,
    browse products, search products,
    add products to cart and make payments.

    The application should support approximately
    10,000 concurrent users.

    It needs to integrate with an external payment gateway.
    """

    result = await analyze_requirements(project)

    print("\n===== REQUIREMENTS RESULT =====\n")

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
