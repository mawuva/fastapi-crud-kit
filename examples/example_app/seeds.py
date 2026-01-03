"""Database seeds for populating initial data."""

from sqlalchemy.ext.asyncio import AsyncSession

from .database import AsyncSessionLocal
from .catalogs.models import Category, Tag
from .articles.models import Article


async def seed_database() -> None:
    """Populate database with initial seed data."""
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        from sqlalchemy import select
        
        result = await session.execute(select(Category))
        existing_categories = result.scalars().all()
        
        if existing_categories:
            print("Database already seeded. Skipping...")
            return
        
        # Create Categories
        categories_data = [
            {"name": "Technology", "description": "Articles about technology and innovation"},
            {"name": "Science", "description": "Scientific articles and research"},
            {"name": "Health", "description": "Health and wellness articles"},
            {"name": "Business", "description": "Business and finance articles"},
            {"name": "Lifestyle", "description": "Lifestyle and culture articles"},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            session.add(category)
            categories.append(category)
        
        # Create Tags
        tags_data = [
            {"name": "Python", "description": "Python programming language"},
            {"name": "FastAPI", "description": "FastAPI web framework"},
            {"name": "Web Development", "description": "Web development topics"},
            {"name": "Data Science", "description": "Data science and analytics"},
            {"name": "Machine Learning", "description": "Machine learning and AI"},
            {"name": "DevOps", "description": "DevOps practices and tools"},
            {"name": "Best Practices", "description": "Best practices and tips"},
        ]
        
        tags = []
        for tag_data in tags_data:
            tag = Tag(**tag_data)
            session.add(tag)
            tags.append(tag)
        
        # Flush to get IDs without committing
        await session.flush()
        
        # Refresh to ensure objects are loaded with IDs
        for category in categories:
            await session.refresh(category)
        for tag in tags:
            await session.refresh(tag)
        
        # Create Articles
        articles_data = [
            {
                "title": "Getting Started with FastAPI",
                "content": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. This article will guide you through the basics of FastAPI and how to get started building your first API.",
                "category": categories[0],  # Technology
                "tags": [tags[0], tags[1], tags[2]],  # Python, FastAPI, Web Development
            },
            {
                "title": "Introduction to Data Science",
                "content": "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from structured and unstructured data. Learn the fundamentals of data science in this comprehensive guide.",
                "category": categories[1],  # Science
                "tags": [tags[3], tags[4]],  # Data Science, Machine Learning
            },
            {
                "title": "Healthy Living Tips",
                "content": "Maintaining a healthy lifestyle is essential for overall well-being. This article provides practical tips and advice for improving your health through diet, exercise, and mindfulness practices.",
                "category": categories[2],  # Health
                "tags": [tags[6]],  # Best Practices
            },
            {
                "title": "Building Scalable Web Applications",
                "content": "Scalability is a crucial aspect of modern web applications. This article explores best practices for building applications that can handle growth and increased load, including architecture patterns and deployment strategies.",
                "category": categories[0],  # Technology
                "tags": [tags[2], tags[5], tags[6]],  # Web Development, DevOps, Best Practices
            },
            {
                "title": "Python Best Practices for 2024",
                "content": "Python continues to evolve, and so do the best practices for writing clean, maintainable code. This article covers the latest Python best practices, including type hints, async programming, and code organization.",
                "category": categories[0],  # Technology
                "tags": [tags[0], tags[6]],  # Python, Best Practices
            },
        ]
        
        for article_data in articles_data:
            tags_list = article_data.pop("tags")
            category = article_data.pop("category")
            article = Article(**article_data, category=category)
            article.tags = tags_list
            session.add(article)
        
        await session.commit()
        print("Database seeded successfully!")
        print(f"Created {len(categories)} categories, {len(tags)} tags, and {len(articles_data)} articles.")


if __name__ == "__main__":
    import asyncio
    from .database import init_db
    
    async def main():
        await init_db()
        await seed_database()
    
    asyncio.run(main())

