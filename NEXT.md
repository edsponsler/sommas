# Project Summary

The project implements an "Automated Systematic Retrieval and Review" (ASRR) system in three phases: building a private search engine, creating a conversational analyst, and developing an implementation strategist capable of generating actionable implementation plans on Google Cloud.

**Capabilities:**

*   Ingesting and preprocessing documents from Google Cloud Storage.
*   Building a private search engine using Vertex AI Search.
*   Creating a conversational agent using Vertex AI Agent Builder and Streamlit.
*   Generating GCP architecture proposals using LangGraph and LLMs.
*   Providing a web interface for interacting with the agent.
*   Document-aware chunking strategy for text preprocessing.
*   MD5 hash check to avoid unnecessary re-indexing of the corpus.

**Development Status:**

The project appears to be a complete tutorial with detailed instructions for setting up and running the ASRR system. The `README.md` file suggests that the project has reached a functional state, covering all three phases of the ASRR implementation. The code includes features such as LangGraph integration for complex tasks, document-aware chunking, and MD5 hash checking for efficient data processing. The project also offers suggestions for future development, such as expanding the knowledge base and building more specialized tools.

**Key Components:**

*   `app.py`: Streamlit application for interacting with the ASRR agent.
*   `preprocess.py`: Data preprocessing pipeline for preparing the document corpus.
*   `tools.py`: Defines the LangGraph-based tool for generating GCP architecture proposals.
*   `README.md`: Provides detailed instructions and overview of the project.

# Chosen Activities

## Improvement

**Summary:** Add more robust error handling to the `search_knowledge_base` function in `app.py`. Implement try-except blocks to catch potential exceptions (e.g., `google.api_core.exceptions.ServiceUnavailable`) and provide more user-friendly error messages.

## Development

**Summary:** Implement unit tests for the core functions in `preprocess.py` and `tools.py` to ensure code reliability and prevent regressions. Focus on testing the document chunking logic, the LangGraph node functions, and the search query construction.

## New Feature

**Summary:** Enhance the knowledge base by integrating with external data sources (e.g., GCP documentation, Stack Overflow, research papers) and using Retrieval-Augmented Generation (RAG) techniques.

# Gemini CLI Prompts

## Improvement Prompt

Provide a detailed project outline for implementing robust error handling in the `search_knowledge_base` function within the `app.py` file of the ASRR project. The outline should include specific steps for identifying potential exceptions, implementing try-except blocks, and providing user-friendly error messages. Consider error scenarios such as Vertex AI Search service unavailability and invalid API responses. The outline should also specify how to log these errors for debugging and monitoring purposes.

## Development Prompt

Create a project outline for adding unit tests to the ASRR project, specifically targeting the core functions in `preprocess.py` and `tools.py`. The outline should include a strategy for selecting the functions to test, choosing a suitable testing framework (e.g., pytest), writing effective test cases for document chunking logic, LangGraph node functions, and search query construction, and integrating the tests into the project's development workflow. Furthermore, the outline should include instructions on how to run the tests and interpret the results.

## New Feature Prompt

Develop a project outline for enhancing the ASRR project's knowledge base with Retrieval-Augmented Generation (RAG). This outline should include steps for: 1) identifying and selecting relevant external data sources (e.g., GCP documentation, Stack Overflow, research papers); 2) integrating these data sources into the existing knowledge base; 3) implementing RAG techniques to retrieve relevant information from these sources and augment the LLM's prompt; 4) incorporating query expansion techniques to improve retrieval accuracy; 5) evaluating the performance of the RAG implementation; and 6) updating the `app.py` and `tools.py` files to utilize the new RAG-enhanced knowledge base. Include details about choosing appropriate libraries and APIs for data integration and retrieval.
```

