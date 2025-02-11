import argparse
import os
import subprocess
import sys
import tempfile
from textwrap import dedent

from dotenv import load_dotenv

exe_dir = os.path.dirname(sys.executable)
print('Gitai v.0.2.2-beta')
print('exe_dir:', exe_dir)

# Construct the path to the .env file
env_path = os.path.join(exe_dir, '.env')

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# List of required environment variables
required_env_vars = ['PROVIDER', 'MODEL', 'API_KEY', 'LANGUAGE']

# Check if each required environment variable is set and not blank
for var in required_env_vars:
    if not os.getenv(var):
        print(f'Error: the environment variable {var} is not set or is blank.')
        print(f'Please set the value in the .env file located at: {env_path}')
        sys.exit(1)

provider = os.getenv('PROVIDER')
model = os.getenv('MODEL')
api_key = os.getenv('API_KEY')
language = os.getenv('LANGUAGE')

if provider == 'openai':
    from openai import OpenAI

    openai_client = OpenAI(api_key=api_key)

elif provider == 'groq':
    from groq import Groq

    groq_client = Groq(api_key=api_key)
else:
    print(f'Error: Provider {provider} is not supported.')
    sys.exit(1)


def detect_project_language(project_path):
    # Indicator files in the project's root directory
    indicator_files = {
        'Node.js': ['package.json', 'yarn.lock', 'package-lock.json', 'npm-shrinkwrap.json'],
        'Python': ['requirements.txt', 'Pipfile', 'pyproject.toml', 'setup.py', 'setup.cfg', 'manage.py'],
        'Java': ['pom.xml', 'build.gradle', 'build.gradle.kts', 'build.xml', '.java-version'],
        'Go': ['go.mod', 'Gopkg.lock'],
        'PHP': ['composer.json', 'composer.lock', 'index.php'],
        'Ruby': ['Gemfile', 'Gemfile.lock', 'Rakefile', 'config.ru', '.ruby-version'],
        'Rust': ['Cargo.toml', 'Cargo.lock'],
        'Haskell': ['stack.yaml', 'cabal.project'],
        'Swift': ['Package.swift'],
        'Elixir': ['mix.exs'],
        'Dart': ['pubspec.yaml'],
        'Scala': ['build.sbt'],
        'Perl': ['Makefile.PL', 'Build.PL'],
        'R': ['.Rproj']
    }

    # File extension indicators in the project's root directory
    extension_indicators = {
        'C#': ['.csproj', '.sln'],
        'Haskell': ['.cabal'],
        'Swift': ['.xcodeproj', '.xcworkspace'],
        'Kotlin': ['.kt', '.kts'],
        'C/C++': ['.c', '.cpp', '.h', '.hpp'],
        'JavaScript': ['.js', '.jsx'],
        'TypeScript': ['.ts', '.tsx'],
        'Python': ['.py'],
        'Java': ['.java']
    }

    try:
        root_files = os.listdir(project_path)
    except Exception:
        return "Unknown"

    # Check for indicator files in the project root
    for prog_language, indicators in indicator_files.items():
        for indicator in indicators:
            # If the indicator is specified with a subdirectory (e.g., 'project/build.properties')
            if os.path.sep in indicator:
                if os.path.exists(os.path.join(project_path, indicator)):
                    return prog_language
            else:
                if indicator in root_files:
                    return prog_language

    # Check for file extensions in the project root
    for prog_language, extensions in extension_indicators.items():
        for file in root_files:
            if any(file.endswith(ext) for ext in extensions):
                return prog_language

    # Recursive search for indicator files in subdirectories
    for root, dirs, files in os.walk(project_path):
        for file in files:
            # Node.js indicators
            if file in ['package.json', 'yarn.lock', 'package-lock.json']:
                return 'Node.js'
            # PHP indicator
            if file.endswith('.php'):
                return 'PHP'
            # Python indicator
            if file.endswith('.py'):
                return 'Python'
            # Java indicator
            if file.endswith('.java'):
                return 'Java'
            # Ruby indicators
            if file in ['Gemfile', 'Rakefile']:
                return 'Ruby'
            # Rust indicators
            if file in ['Cargo.toml', 'Cargo.lock']:
                return 'Rust'
            # C# indicator
            if file.endswith('.csproj'):
                return 'C#'
            # Dart indicator
            if file == 'pubspec.yaml':
                return 'Dart'
            # Swift indicator
            if file == 'Package.swift':
                return 'Swift'

    return "Unknown"


def generate_commit_message(diff_output, project_language, base_message):
    prompt = dedent(f"""
    Based on the information provided below, create a commit message following the Conventional Commits standard, 
    which is widely adopted to make commit messages more descriptive and useful. This standard uses specific prefixes 
    to categorize the type of change made, followed by a brief description. 

    The most common prefixes of the Conventional Commits standard are:
        - feat: A new feature
        - fix: A bug fix
        - chore: Maintenance changes or minor fixes that do not alter functionality

    For your information and better understanding, the project in question uses the programming language {project_language}.

    Basic change description provided by the developer, which you should use as the basis for your message: '{base_message}'

    Below are the detailed changes (including modified files and what was added, changed, or removed) generated by the 'git diff' command: 

    ```
    {diff_output}
    ```

    Based on the above information, improve the basic description to create an objective commit message.

    Mandatory rules:
    - You must follow the Conventional Commits standard.
    - The first line of the message must start with one of the Conventional Commits prefixes (feat, fix, chore, etc.) followed by a concise description explaining what was done.
    - After the first line, always add an objective explanation of the changes made, the reason for the change, and, if applicable, the impact of the change.
    - Whenever possible, mention only the main modified files in the commit message without including the path.
    - DO NOT add any comments or additional explanations beyond the generated commit message.
    - DO NOT use symbols such as ``` or any other formatting to denote the commit message.
    - DO NOT add line breaks or whitespace before the commit message.
    - The output must be ONLY the final commit message as per the instructions.
    - You must use the language '{language}' in your response generation.
    """)

    return call_provider_api(prompt)


def call_provider_api(prompt):
    messages = [
        {
            "role": "system",
            "content": dedent(f"""
                            You are an assistant that helps generate commit messages for a Git repository. 
                            Commit messages must follow the Conventional Commits standard, which uses specific prefixes to categorize the type of change made (feat, fix, chore, etc.). 
                            The description must be concise and clear, explaining what was done, the reason for the change, and, if applicable, the impact of the change.
                            The messages must be generated based on the changes provided by the 'git diff' command and an optional basic description provided by the user. 

                            Mandatory rules:
                            - DO NOT add any comments or additional explanations beyond the generated commit message.
                            - DO NOT use symbols such as ``` or any other formatting to denote the commit message.
                            - DO NOT add line breaks or whitespace before the commit message.
                            - The output must be ONLY the final commit message as per the instructions.
                            - The first line of the message must start with one of the Conventional Commits prefixes (feat, fix, chore, etc.).
                            - After the first line, always add an objective explanation of the changes made, the reason for the change, and, if applicable, the impact of the change.

                            If the instructions are not followed correctly, the result will not be accepted.
                        """)
        },
        {"role": "user", "content": prompt}
    ]

    match provider:
        case 'openai':
            print(f'Provider: {provider} - Model: {model}')
            response = openai_client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.5,
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0)
            return response.choices[0].message.content.strip()
        case 'groq':
            print(f'Provider: {provider} - Model: {model}')
            response = groq_client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.5,
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].message.content.strip()

        case _:
            print(f'Error: Provider {provider} is not supported.')
            sys.exit(1)


def run_git_command(command, exit_on_error=True):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        if exit_on_error:
            print(f"Error executing command:\n-> {' '.join(command)}")
            print(f"Standard output:\n{result.stdout}")
            print(f"Error output:\n{result.stderr}")
            sys.exit(1)
        else:
            output = result.stdout.strip() + '\n' + result.stderr.strip()
            return output, result.returncode
    else:
        output = result.stdout.strip() + '\n' + result.stderr.strip()
        return output, result.returncode


def has_uncommitted_changes():
    status_output, _ = run_git_command(['git', 'status', '--porcelain'])
    return len(status_output.strip()) > 0


def is_branch_ahead():
    status_output, _ = run_git_command(['git', 'status', '-uno'])
    return "Your branch is ahead" in status_output or "Seu branch está à frente" in status_output


def commit_changes(commit_message):
    run_git_command(['git', 'add', '.'])
    # Write the commit message to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(commit_message)
        temp_filename = temp_file.name
    try:
        _, commit_result = run_git_command(['git', 'commit', '-F', temp_filename])
    finally:
        os.unlink(temp_filename)  # Remove the temporary file


def perform_git_pull():
    output, returncode = run_git_command(['git', 'pull'], exit_on_error=False)

    if returncode != 0:
        if 'CONFLICT' in output or 'CONFLITO' in output:
            print("Conflitos detectados durante git pull:")
            print(output)
            return False
        else:
            print(f"Error executing git pull:\n{output}")
            sys.exit(1)
    else:
        print("Git pull executed successfully.")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Gitai commit and push script.',
        usage="gitai <project_path> '<base_message>' [--push]"
    )
    parser.add_argument('project_path', type=str, help='The path to the project.')
    parser.add_argument('base_message', type=str, help='The base commit message.')
    parser.add_argument('--push', action='store_true', default=False, help='Whether to push after committing.')

    args = parser.parse_args()
    os.chdir(args.project_path)

    # Check if there are uncommitted changes before git pull
    if has_uncommitted_changes():
        print("Uncommitted local changes detected.")
        project_language = detect_project_language(args.project_path)
        diff_output, _ = run_git_command(['git', 'diff'])
        commit_message = generate_commit_message(diff_output, project_language, args.base_message)

        print("\n\nGenerated commit message:\n")
        print(commit_message)
        print("\n")

        commit_changes(commit_message)
        print("-> Gitai successfully committed local changes.")
    else:
        print("No local changes to commit before git pull.")

    # Execute git pull after committing local changes
    pull_successful = perform_git_pull()

    if not pull_successful:
        print("Git pull failed due to conflicts. Please resolve the conflicts manually.")
        sys.exit(1)

    # Check if there are new conflicts after the pull
    if has_uncommitted_changes():
        print("Conflicts or uncommitted changes detected after pull.")
        project_language = detect_project_language(args.project_path)
        diff_output, _ = run_git_command(['git', 'diff'])
        commit_message = generate_commit_message(diff_output, project_language, "Resolving conflicts after git pull")

        print("\n\nGenerated commit message for resolving conflicts:\n")
        print(commit_message)
        print("\n")

        commit_changes(commit_message)
        print("-> Gitai successfully committed changes after pull.")
    else:
        print("No changes to commit after git pull.")

    if args.push:
        if is_branch_ahead():
            run_git_command(['git', 'push'])
            print("-> Gitai successfully pushed changes.")
        else:
            print("No changes to push. The local branch is synchronized with the remote.")


if __name__ == "__main__":
    main()
