## Gitai - Release Notes Generator

This document provides detailed instructions for using the `releaser.py` script to generate release notes for a git repository.

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- git

### Environment Setup

1. **Clone the Repository**: Clone the Gitai repository to your local machine using `git clone`.

   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**: Change to the project directory.

   ```bash
   cd <project-name>
   ```

3. **Install the Project Dependencies**: Install the required Python libraries.

   ```bash
   pip install -r requirements.txt
   ```

### Configuring the .env File

Before running the `releaser.py` script, you need to configure the `.env` file with the necessary environment variables. This file should be located in the root directory of the project.

#### Example Configuration for OpenAI

```dotenv
PROVIDER=openai
API_KEY=your_openai_api_key
MODEL=gpt-4o
LANGUAGE=en
```

#### Example Configuration for Groq

```dotenv
PROVIDER=groq
API_KEY=your_groq_api_key
MODEL=mixtral-8x7b-32768
LANGUAGE=en
```

### Using the `releaser.py` Script

The `releaser.py` script generates release notes based on the commits made since the last tag. Follow the steps below to use the script:

1. **Navigate to the Project Directory**: Ensure you are in the project directory.

   ```bash
   cd <project-name>
   ```

2. **Run the Script**: Execute the `releaser.py` script with the old tag and the new version as arguments.

   ```bash
   python src/gitai/releaser.py <old_tag> <new_version>
   ```

   Replace `<old_tag>` with the previous Git tag and `<new_version>` with the new release version.

### Example Usage

```bash
python src/gitai/releaser.py v0.2.0-beta v0.2.1-beta
```

This command will generate release notes for all commits made since the `v0.2.0-beta` tag and save them in a file named `release_v0.2.1-beta.md` in the `dist` directory.

### Output

The generated release notes will be saved in the `dist` directory with a filename in the format `release_<new_version>.md`.

### Additional Information

- The script uses the AI provider specified in the `.env` file to generate the release notes.
- Ensure that the `.env` file is correctly configured with the necessary API keys and model information.
- The generated release notes will follow the template and language specified in the script.

By following these instructions, you can easily generate release notes for git repositories using the `releaser.py` script.