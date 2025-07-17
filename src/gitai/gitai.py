import argparse
import os
import subprocess
import sys
import tempfile
from textwrap import dedent

from colorama import Back, Fore, Style, init
from dotenv import load_dotenv

# Initialize colorama for cross-platform colored output
init(autoreset=True)


# Utility functions for colored console output
def print_header(message):
    """Print header messages with cyan color and rocket emoji"""
    print(f"{Fore.CYAN}{Style.BRIGHT}🚀 {message}{Style.RESET_ALL}")


def print_success(message):
    """Print success messages with green color and checkmark emoji"""
    print(f"{Fore.GREEN}{Style.BRIGHT}✅ {message}{Style.RESET_ALL}")


def print_info(message):
    """Print info messages with blue color and info emoji"""
    print(f"{Fore.BLUE}{Style.BRIGHT}ℹ️  {message}{Style.RESET_ALL}")


def print_warning(message):
    """Print warning messages with yellow color and warning emoji"""
    print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  {message}{Style.RESET_ALL}")


def print_error(message):
    """Print error messages with red color and error emoji"""
    print(f"{Fore.RED}{Style.BRIGHT}❌ {message}{Style.RESET_ALL}")


def print_git_operation(message):
    """Print git operation messages with magenta color and git emoji"""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}🔄 {message}{Style.RESET_ALL}")


def print_ai_message(message):
    """Print AI-related messages with cyan color and robot emoji"""
    print(f"{Fore.CYAN}{Style.BRIGHT}🤖 {message}{Style.RESET_ALL}")


def print_commit_message(message):
    """Print commit message with special formatting"""
    print(f"\n{Fore.WHITE}{Back.BLUE}{Style.BRIGHT} Generated commit message: {Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}{Style.BRIGHT}{message}{Style.RESET_ALL}")
    print()


def get_language_emoji(language):
    """Get appropriate emoji for programming language"""
    language_emojis = {
        'Node.js': '🟢',
        'Python': '🐍',
        'Java': '☕',
        'Go': '🐹',
        'PHP': '🐘',
        'Ruby': '💎',
        'Rust': '🦀',
        'Haskell': '🎩',
        'Swift': '🍎',
        'Elixir': '💧',
        'Dart': '🎯',
        'Scala': '⚖️',
        'Perl': '🐪',
        'R': '📊',
        'C#': '🔷',
        'C/C++': '⚙️',
        'JavaScript': '🟨',
        'TypeScript': '🔷',
        'Unknown': '❓'
    }
    return language_emojis.get(language, '❓')


def print_detected_language(language):
    """Print detected programming language with appropriate emoji"""
    emoji = get_language_emoji(language)
    print_info(f'{emoji} Linguagem detectada: {language}')
    print()


exe_dir = os.path.dirname(sys.executable)
print_header('Gitai v.0.2.5-beta')
print_info(f'📁 exe_dir: {exe_dir}')
print()

# Construct the path to the .env file
env_path = os.path.join(exe_dir, '.env')

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# List of required environment variables
required_env_vars = ['PROVIDER', 'MODEL', 'API_KEY', 'LANGUAGE']

# Check if each required environment variable is set and not blank
for var in required_env_vars:
    if not os.getenv(var):
        print_error(f'The environment variable {var} is not set or is blank.')
        print_error(f'Please set the value in the .env file located at: {env_path}')
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

elif provider == 'anthropic':
    from anthropic import Anthropic

    anthropic_client = Anthropic(api_key=api_key)

else:
    print_error(f'Provider {provider} is not supported.')
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

    The ONLY accepted prefixes for this project are:
        - feat: A new feature
        - fix: A bug fix
        - docs: Documentation changes
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
    - The first line of the message must start with one of these EXACT prefixes (feat, fix, docs, chore) followed by a concise description explaining what was done.
    - After the first line, always add an objective explanation of the changes made, the reason for the change, and, if applicable, the impact of the change.
    - Whenever possible, mention only the main modified files in the commit message without including the path.
    - DO NOT add any comments or additional explanations beyond the generated commit message.
    - DO NOT use symbols such as ``` or any other formatting to denote the commit message.
    - DO NOT add line breaks or whitespace before the commit message.
    - The output must be ONLY the final commit message as per the instructions.
    - You must use the language '{language}' in your response generation.

    <output_format>
    Your response must follow this exact format:
    
    Line 1: [prefix]: [concise description]
    Line 2: [empty line]
    Line 3+: [detailed explanation of changes, reasons, and impact]
    
    Example:
    feat: add defaultOrganizationName field to CreateUserDto

    Add defaultOrganizationName field to CreateUserDto for custom workspace naming. Allow users to specify a default organization name in CreateUserDto, which is used as the workspace name in UserService. This change provides flexibility for users to define their workspace name, enhancing user personalization and improving the user experience. Modified files include UserService.java and CreateUserDto.java.
    </output_format>
    """)

    commit_message = call_provider_api(prompt)
    signature = "\n\n🤖 Commit generated with [Gitai](https://github.com/leandrosilvaferreira/gitai)"
    return commit_message + signature


def call_provider_api(prompt):
    messages = [
        {
            "role": "system",
            "content": dedent(f"""
                            You are an assistant that helps generate commit messages for a Git repository. 
                            Commit messages must follow the Conventional Commits standard, which uses ONLY these specific prefixes to categorize the type of change made: feat, fix, docs, chore. 
                            The description must be concise and clear, explaining what was done, the reason for the change, and, if applicable, the impact of the change.
                            The messages must be generated based on the changes provided by the 'git diff' command and an optional basic description provided by the user. 

                            Mandatory rules:
                            - DO NOT add any comments or additional explanations beyond the generated commit message.
                            - DO NOT use symbols such as ``` or any other formatting to denote the commit message.
                            - DO NOT add line breaks or whitespace before the commit message.
                            - The output must be ONLY the final commit message as per the instructions.
                            - The first line of the message must start with one of these EXACT prefixes: feat, fix, docs, chore.
                            - After the first line, always add an objective explanation of the changes made, the reason for the change, and, if applicable, the impact of the change.

                            <output_format>
                            CRITICAL: Your response must follow this exact structure:
                            
                            Line 1: [prefix]: [concise description]
                            (where prefix must be exactly one of: feat, fix, docs, chore)
                            Line 2: [EMPTY LINE - mandatory line break]
                            Line 3+: [detailed explanation]
                            
                            CORRECT format example:
                            feat: add user authentication system

                            Implement JWT-based authentication with login and registration endpoints. Add middleware for route protection and user session management. This enhancement improves application security and enables personalized user experiences.
                            
                            INCORRECT format (everything in one line):
                            feat: add user authentication system - Implement JWT-based authentication with login and registration endpoints...
                            </output_format>

                            If the instructions are not followed correctly, the result will not be accepted.
                        """)
        },
        {"role": "user", "content": prompt}
    ]

    match provider:
        case 'openai':
            print_ai_message(f'Provider: {provider} - Model: {model}')
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
            print_ai_message(f'Provider: {provider} - Model: {model}')
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
        case 'anthropic':
            print(f'Provider: {provider} - Model: {model}')
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=500,
                temperature=0.5,
                system=messages[0]["content"],
                messages=[{"role": "user", "content": messages[1]["content"]}]
            )
            return response.content[0].text.strip()

        case _:
            print_error(f'Provider {provider} is not supported.')
            sys.exit(1)


def run_git_command(command, exit_on_error=True):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        if exit_on_error:
            print_error(f"Error executing command: {' '.join(command)}")
            print_error(f"Standard output: {result.stdout}")
            print_error(f"Error output: {result.stderr}")
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
            print_warning("Conflitos detectados durante git pull:")
            print_error(output)
            return False
        else:
            print_error(f"Error executing git pull: {output}")
            sys.exit(1)
    else:
        print_success("Git pull executed successfully.")
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
        print_warning("Uncommitted local changes detected.")
        project_language = detect_project_language(args.project_path)
        print_detected_language(project_language)
        diff_output, _ = run_git_command(['git', 'diff'])
        commit_message = generate_commit_message(diff_output, project_language, args.base_message)

        print_commit_message(commit_message)

        commit_changes(commit_message)
        print_success("Gitai successfully committed local changes.")
    else:
        print_info("No local changes to commit before git pull.")

    # Execute git pull after committing local changes
    pull_successful = perform_git_pull()

    if not pull_successful:
        print_error("Git pull failed due to conflicts. Please resolve the conflicts manually.")
        sys.exit(1)

    # Check if there are new conflicts after the pull
    if has_uncommitted_changes():
        print_warning("Conflicts or uncommitted changes detected after pull.")
        project_language = detect_project_language(args.project_path)
        print_detected_language(project_language)
        diff_output, _ = run_git_command(['git', 'diff'])
        commit_message = generate_commit_message(diff_output, project_language, "Resolving conflicts after git pull")

        print_commit_message(commit_message)

        commit_changes(commit_message)
        print_success("Gitai successfully committed changes after pull.")
    else:
        print_info("No changes to commit after git pull.")

    if args.push:
        if is_branch_ahead():
            run_git_command(['git', 'push'])
            print_success("Gitai successfully pushed changes.")
        else:
            print_info("No changes to push. The local branch is synchronized with the remote.")


if __name__ == "__main__":
    main()
