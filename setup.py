"""
Setup script for ByToBy-Pro-v3
"""

import os
import sys
from setuptools import setup, find_packages
from pathlib import Path

# Read requirements
def get_requirements():
    """Get requirements from requirements.txt"""
    requirements_path = Path(__file__).parent / 'requirements.txt'
    if requirements_path.exists():
        with open(requirements_path, 'r') as f:
            requirements = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith('#')
            ]
        return requirements
    return []

# Read README
def get_readme():
    """Get README content"""
    readme_path = Path(__file__).parent / 'README.md'
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "ByToBy-Pro-v3 - Advanced Trading Analytics Platform"

# Setup configuration
setup(
    name="bytoby-pro-v3",
    version="3.0.0",
    author="ByToBy Team",
    author_email="support@bytoby.com",
    description="Advanced AI-Powered Trading Analytics Platform",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ByToBy-Pro-v3",
    project_urls={
        "Documentation": "https://docs.bytoby.com",
        "Source": "https://github.com/yourusername/ByToBy-Pro-v3",
        "Tracker": "https://github.com/yourusername/ByToBy-Pro-v3/issues",
    },
    packages=find_packages(include=['backend*', 'pages*', 'database*']),
    python_requires=">=3.9",
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.4.1",
            "isort>=5.12.0",
        ],
        "ml": [
            "tensorflow>=2.13.0",
            "torch>=2.0.1",
            "transformers>=4.31.0",
            "scikit-learn>=1.3.0",
        ],
        "docker": [
            "docker>=6.1.3",
        ],
        "all": [
            "tensorflow>=2.13.0",
            "torch>=2.0.1",
            "transformers>=4.31.0",
            "docker>=6.1.3",
            "kubernetes>=26.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bytoby=app:main",
            "bytoby-cli=scripts.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "trading", "finance", "ai", "machine-learning",
        "stock-market", "crypto", "analytics", "streamlit",
        "data-science", "quantitative-finance"
    ],
    include_package_data=True,
    zip_safe=False,
    package_data={
        'backend': ['*.yaml', '*.json'],
        'assets': ['css/*.css', 'js/*.js', 'images/*'],
    },
)
