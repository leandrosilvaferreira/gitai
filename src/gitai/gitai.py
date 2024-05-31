import os
import subprocess
import sys
from textwrap import dedent
import argparse

from dotenv import load_dotenv

# Obtém o caminho do diretório do executável
exe_dir = os.path.dirname(sys.executable)
print('exe_dir:', exe_dir)

# Constrói o caminho do arquivo .env
env_path = os.path.join(exe_dir, '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path=env_path)

# Lista de variáveis de ambiente necessárias
required_env_vars = ['PROVIDER', 'MODEL', 'API_KEY', 'LANGUAGE']

# Verifica se cada variável de ambiente necessária está definida e não está em branco
for var in required_env_vars:
    if not os.getenv(var):
        print(f'Erro: a variável de ambiente {var} não está definida ou está em branco.')
        print(f'Por favor, defina o valor no arquivo .env localizado em: {env_path}')
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
    print(f'Erro: Provedor {provider} não suportado.')
    sys.exit(1)


def detect_project_language(project_path):
    language_files = {
        'Node.js': ['package.json', 'yarn.lock'],
        'Python': ['requirements.txt', 'Pipfile', 'pyproject.toml'],
        'Java': ['pom.xml', 'build.gradle', 'build.gradle.kts', '.java-version'],
        'Go': ['go.mod', 'Gopkg.lock'],
        'PHP': ['composer.json', 'composer.lock']
    }

    for message_language, files in language_files.items():
        if any(os.path.exists(os.path.join(project_path, file)) for file in files):
            return message_language

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.php'):
                return 'PHP'

    return "Desconhecido"


def generate_commit_message(status_output, project_language, base_message):
    prompt = dedent(f"""
    Com base nas informações fornecidas abaixo, crie uma mensagem de commit seguindo o padrão de Conventional Commits, 
    que é amplamente adotado para tornar as mensagens de commit mais descritivas e úteis. Este padrão utiliza prefixos 
    específicos para categorizar o tipo de mudança realizada, seguido de uma breve descrição. 

    Os prefixos do padrão de Conventional Commits mais comuns são:
        - feat: Uma nova funcionalidade
        - fix: Uma correção de bug
        - chore: Mudanças de manutenção ou pequenas correções que não alteram a funcionalidade

    A título de informação e para seu melhor entendimento, o projeto em questão utiliza a linguagem de programação {project_language}.

    Descrição básica da mudança fornecida pelo programador a qual você deve usar como base para o início da sua mensagem: '{base_message}'

    Abaixo seguem as mudanças detalhadas (incluindo arquivos modificados e o que foi incluído, alterado ou excluído) geradas pelo comando 'git status': 

    ```
    {status_output}
    ```

    Com base nas informações acima, melhore a descrição básica para criar uma mensagem de commit objetiva, clara e 
    seguindo o padrão de Conventional Commits. 

    A mensagem deve começar com o prefixo apropriado seguido de uma descrição concisa que explique o que foi feito, 
    o motivo da mudança e, se aplicável, o impacto da mudança.

    Sempre que possível, cite na mensagem de commit somente os arquivos principais modificados sem incluir o path.

    A mensagem final gerada não deve ter símbolos ``` ou qualquer outra formatação e deve ser obrigatoriamente no idioma {language}.
    """)

    return call_provider_api(prompt)


def call_provider_api(prompt):
    messages = [
        {
            "role": "system",
            "content": dedent(f"""
                            Você é um assistente que ajuda a gerar mensagens de commit para um repositório Git. 
                            As mensagens de commit devem seguir o padrão de Conventional Commits, que usa prefixos específicos para categorizar o tipo de mudança realizada (feat, fix, chore, etc.). 
                            A descrição deve ser concisa e clara, explicando o que foi feito, o motivo da mudança e, se aplicável, o impacto da mudança.
                            As mensagens devem ser geradas com base nas alterações fornecidas pelo comando 'git status' e em uma descrição básica fornecida pelo usuário opcionalmente. 

                            Regras importantes:
                            - NÃO adicione comentários ou explicações adicionais além da mensagem de commit gerada.
                            - NÃO utilize símbolos como ``` para identificar a mensagem de commit.
                            - NÃO adicione quebras de linha ou espaços em branco antes da mensagem de commit.
                            - A saída deve ser APENAS a mensagem de commit final conforme as instruções.
                            - A primeira linha da mensagem deve obrigatoriamente começar com um dos prefixos do padrão de Conventional Commits (feat, fix, chore, etc.).
                            - Após a primeira linha, sempre adicione uma explicação objetiva das alterações realizadas.

                            Se as instruções não forem seguidas corretamente, o resultado não será aceito.
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
                temperature=1,
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
                temperature=1,
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].message.content.strip()

        case _:
            print(f'Erro: Provedor {provider} não suportado.')
            sys.exit(1)


def run_git_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, encoding='utf-8')
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando:\n-> {command}\nerror: {e.stderr}")
        print(f"\n\nSaída de erro padrão:\n {e.output}")
        sys.exit(1)


def has_uncommitted_changes():
    status_output, _ = run_git_command(['git', 'status', '--porcelain'])
    return len(status_output) > 0


def commit_changes(commit_message):
    while has_uncommitted_changes():
        run_git_command(['git', 'add', '.'])
        _, commit_result = run_git_command(['git', 'commit', '-m', commit_message])
        if commit_result != 0:
            break


def main():
    parser = argparse.ArgumentParser(
        description='Gitai commit and push script.',
        usage="gitai <caminho_do_projeto> '<mensagem_genérica>' [--push]"
    )
    parser.add_argument('project_path', type=str, help='The path to the project.')
    parser.add_argument('base_message', type=str, help='The base commit message.')
    parser.add_argument('--push', action='store_true', default=False, help='Whether to push after committing.')

    args = parser.parse_args()
    os.chdir(args.project_path)

    project_language = detect_project_language(args.project_path)
    status_output, _ = run_git_command(['git', 'status'])
    diff_output, _ = run_git_command(['git', 'diff'])

    commit_message = generate_commit_message(status_output + "\n" + diff_output, project_language, args.base_message)

    print("\n\nMensagem de commit gerada:\n")
    print(commit_message)
    print("\n")

    commit_changes(commit_message)
    print("-> Gitai concluiu o commit com sucesso.")

    if args.push:
        run_git_command(['git', 'fetch'])
        status_output, _ = run_git_command(['git', 'status', '-uno'])

        if 'have diverged' in status_output:
            print(f"Existem alterações remotas no branch atual, faça merge primeiro antes de fazer push.\nMsg:\n{status_output}")
            sys.exit(1)

        run_git_command(['git', 'push'])
        print("-> Gitai concluiu o push com sucesso.")


if __name__ == "__main__":
    main()
