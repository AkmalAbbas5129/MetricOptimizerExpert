# OptiGenius - Linaear Optimizer

The OptiGenius - Linaear Optimizer is a streamlit web application designed to solve optimization problems using advanced AI and machine learning models. This app leverages the power of Generative AI and Azure services to provide optimal solutions to complex optimization problems, generate insightful answer, and log user interactions for further analysis.

## Table of Contents
1. [Codebase](#codebase)
2. [Dependencies](#dependencies)
3. [Environment Configurations](#environment-configurations)
4. [Input Data](#example-input)
5. [Expected Output](#example-output)
6. [Installation and Execution Instructions](#installation-and-execution-instructions)
7. [Additional Documentation](#additional-documentation)

## Codebase

### File Structure
- `streamlit_app.py`: Main Streamlit application file, handles the UI and integrates with backend services.
- `openai_utils.py`: Utility functions for interacting with Azure OpenAI's GPT model, including functions for solving optimization problems.
- `azure_blob_utils.py`: Utility functions for interacting with Azure Blob Storage, including functions for logging user interactions.

## Dependencies

The project relies on several key libraries and services:

- **Streamlit**: For building the web interface.
- **Azure OpenAI**: For natural language processing and generating solutions.
- **Azure Storage**: For storing logs and user interaction data.
- **Pandas**: For data manipulation and logging.

### Required Python Packages
- `azure-storage-blob`
- `langchain`
- `langchain_core`
- `langchain_experimental`
- `langchain_openai`
- `pandas`
- `python-dotenv`
- `streamlit`

## Environment Configurations

To run the application, you'll need to set up environment variables and configuration files. Key configurations include:

- **Azure OpenAI API Credentials**: Store in '.env' for secure access.
- **Azure Blob Storage**: Connection strings and container names are also stored in `st.secrets`.

### Sample `.env` File
```env
AZURE_OPENAI_API_KEY = ""
AZURE_OPENAI_ENDPOINT = ""
api_version = ""
AZURE_DEPLOYMENT_NAME = ""
AZURE_EMBEDDING_DEPLOYMENT_NAME = ""
```

## Input Data

The application expects the following inputs from the user:

1. **Problem Statement**: A detailed description of the optimization problem to be solved. This should include the context and any relevant background information.
2. **Objective to Solve**: The specific goal or outcome that the optimization process aims to achieve. This could be minimizing costs, maximizing efficiency, etc.
3. **Constraints**: Any limitations or conditions that must be adhered to while solving the optimization problem. This may include resource limits, deadlines, or other operational constraints.

### Example Input
```markdown
**Problem Statement:** 
Optimize the supply chain logistics for a manufacturing company to minimize total transportation costs while meeting delivery deadlines.

**Objective to Solve:** 
Minimize the total transportation cost across all supply routes.

**Constraints:** 
- Each supplier can only supply a maximum of 1000 units.
- The delivery deadline for all orders is within 5 days.
- Transportation capacity for each route is limited to 500 units per day.
```
### Example Output
```markdown
**Solution:**
- Optimal solution to the question.
```
