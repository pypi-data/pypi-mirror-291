from setuptools import setup, find_packages

setup(
    name="nusterai",
    version="0.1.0",
    description="A package for routing prompts to different LLMs based on difficulty.",
    author="Shashidhar Naidu Boya",
    author_email="shashidharnaiduboya@nusterai.com",
    url="https://github.com/shashidharnaiduboya-nusterAi/NusterAI",
    packages=find_packages(),
    install_requires=[
        "textstat>=0.7.0",
        "google-generativeai>=0.3.0",
        "openai>=0.27.0"
    ],
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
