import os
import subprocess
import sys
from textwrap import dedent
import argparse
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

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
    print(f'Error: Provider {provider} not supported.')
    print('Supported providers: openai, groq, anthropic')
    sys.exit(1)


def run_git_command(command):
    """Executes a git command and returns its output."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command:\n-> {command}\nerror: {e.stderr}")
        print(f"\n\nStandard error output:\n {e.output}")
        sys.exit(1)


def get_commit_messages_since_tag(tag):
    """Retrieves all commit messages since the specified tag."""
    command = ['git', 'log', f'{tag}..HEAD', '--pretty=format:%h %s']
    return run_git_command(command).split('\n')


def generate_release_notes(commits, new_version, tag):
    """Generates release notes based on the provided commits."""
    prompt = dedent(f"""
    You are an assistant that helps generate release notes for a Git repository.
    Below are the commits since the last tag {tag}.
    Please organize the commits into the following categories: New Features, Bug Fixes, and Other Changes.
    Generate a release message in markdown format in the language '{language}' using the following template:

    ```
    # Release {new_version}
    <SUMMARY/>

    ### New Features
    - Description of new features (commits).

    ### Bug Fixes
    - Description of bug fixes (commits).

    ### Other Changes
    - Description of other changes (commits).

    We thank all the contributors who made this release possible! For more details, please refer to the complete version notes.

    **Full Changelog:** [See commits for {new_version}](https://github.com/leandrosilvaferreira/gitai/compare/{tag}...{new_version})
    ```

    Commits:
    {commits}

    Important rules:
        - The generated content must be in the language '{language}'.
        - Replace <SUMMARY/> in the template with a brief and enthusiastic summary of the changes made since the last tag {tag}.
        - DO NOT add any additional comments or explanations.
        - DO NOT use symbols like ``` to denote commit messages.
        - The message must be clear, concise, and well-organized.
        - Remember to follow the provided template.

    If the instructions are not followed correctly, the result will not be accepted.
    """)

    return call_provider_api(prompt)


def call_provider_api(prompt):
    messages = [
        {
            "role": "system",
            "content": dedent("""
                                You are an assistant that helps generate release notes for a Git repository.
                                Commit messages should be organized into categories such as New Features, Bug Fixes, and Other Changes.
                                The output must be a markdown-formatted text according to the provided template, with no additional comments or formatting.
                            """)
        },
        {"role": "user", "content": prompt}
    ]

    """Calls the API of the specified provider (OpenAI, Groq, or Anthropic) to generate the content."""
    match provider:
        case 'openai':
            response = openai_client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=1,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0)
            return response.choices[0].message.content.strip()
        case 'groq':
            response = groq_client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=1,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].message.content.strip()
        case 'anthropic':
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=1,
                system=messages[0]["content"],
                messages=[{"role": "user", "content": messages[1]["content"]}]
            )
            return response.content[0].text.strip()
        case _:
            print(f'Error: Provider {provider} not supported.')
            print('Supported providers: openai, groq, anthropic')
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Git release notes generator.',
        usage="releaser.py <old_tag> <new_version>"
    )
    parser.add_argument('old_tag', type=str, help='The old Git tag.')
    parser.add_argument('new_version', type=str, help='The new release version.')

    args = parser.parse_args()

    commits = get_commit_messages_since_tag(args.old_tag)
    formatted_commits = '\n'.join(commits)

    release_notes = generate_release_notes(formatted_commits, args.new_version, args.old_tag)

    release_filename = os.path.join('dist', f"release_{args.new_version}.md")
    os.makedirs('dist', exist_ok=True)  # Ensure the 'dist' folder exists
    with open(release_filename, 'w') as file:
        file.write(release_notes)

    print(f"Release notes successfully generated in {release_filename}.")


if __name__ == "__main__":
    main()
