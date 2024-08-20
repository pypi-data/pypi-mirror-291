from setuptools import setup, find_packages

setup(
    name="pytest_zephyr_scale_integration",
    version="0.1.0",
    description="A library for integrating Jira Zephyr Scale (Adaptavist\TM4J) with pytest",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "python-dotenv",
        "requests",
        "requests-toolbelt",
    ],
    entry_points={
        'pytest11': [
            'pytest_zephyr_scale_integration = pytest_zephyr_scale_integration.conftest',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)