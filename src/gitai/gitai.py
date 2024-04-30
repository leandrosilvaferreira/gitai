import os
import subprocess
import sys
from textwrap import dedent
import argparse

import openai
from dotenv import load_dotenv

# Obtém o caminho do diretório do executável
exe_dir = os.path.dirname(sys.executable)
print('exe_dir:', exe_dir)

# Constrói o caminho do arquivo .env
env_path = os.path.join(exe_dir, '.env')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path=env_path)

# Lista de variáveis de ambiente necessárias
required_env_vars = ['OPENAI_MODEL', 'OPENAI_API_KEY', 'LANGUAGE']

# Verifica se cada variável de ambiente necessária está definida e não está em branco
for var in required_env_vars:
    if not os.getenv(var):
        print(f'Erro: a variável de ambiente {var} não está definida ou está em branco.')
        print(f'Por favor, defina o valor no arquivo .env localizado em: {env_path}')
        sys.exit(1)

openai.api_key = os.getenv('OPENAI_API_KEY')
model = os.getenv('OPENAI_MODEL')
language = os.getenv('LANGUAGE')


def detect_project_language(project_path):
    # Expanded dictionary with characteristic files for each language
    language_files = {
        'Node.js': ['package.json', 'yarn.lock'],
        'Python': ['requirements.txt', 'Pipfile', 'pyproject.toml'],
        'Java': ['pom.xml', 'build.gradle', 'build.gradle.kts', '.java-version'],
        'Go': ['go.mod', 'Gopkg.lock'],
        'PHP': ['composer.json', 'composer.lock']
    }

    # Check for the existence of characteristic files in the project directory
    for message_language, files in language_files.items():
        if not isinstance(files, list):
            files = [files]
        if any(os.path.exists(os.path.join(project_path, file)) for file in files):
            return message_language

    # Additional check for PHP projects without dependency managers
    # Look for .php files in the project directory
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
    
    A mensagem final gerada não deve ter símboloes ``` ou qualquer outra formatação e deve ser no idioma {language}.
    """)

    # print(prompt)

    # O código para chamar a API da OpenAI e processar a resposta permanece o mesmo...
    response = openai.chat.completions.create(
        model=model,
        temperature=0.5,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content.replace('```', '').strip()


def run_git_command(command):
    """Executa um comando git e retorna a saída."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, encoding='utf-8')
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando:\n-> {command}\nerror: {e.stderr}")
        print(f"\n\nSaída de erro padrão:\n {e.output}")
        sys.exit(1)


def has_uncommitted_changes():
    # Verifica se há mudanças não commitadas
    status_output, _ = run_git_command(['git', 'status', '--porcelain'])
    return len(status_output) > 0


def commit_changes(commit_message):
    # Continua tentando commitar até que não haja mais mudanças feitas pelo hook de pré-commit
    while has_uncommitted_changes():
        # Adiciona todos os arquivos modificados
        run_git_command(['git', 'add', '.'])

        # Tenta fazer o commit
        _, commit_result = run_git_command(['git', 'commit', '-m', commit_message])

        # Se o commit foi bem-sucedido, sai do loop
        if commit_result != 0:
            break


def main():
    # Cria o parser
    parser = argparse.ArgumentParser(
        description='Gitai commit and push script.',
        usage="gitai <caminho_do_projeto> '<mensagem_genérica>' [--push]"
    )
    parser.add_argument('project_path', type=str, help='The path to the project.')
    parser.add_argument('base_message', type=str, help='The base commit message.')
    parser.add_argument('--push', action='store_true', default=False, help='Whether to push after committing.')

    # Analisa os argumentos
    args = parser.parse_args()

    # Muda para o diretório do projeto
    os.chdir(args.project_path)

    # Detecta a linguagem do projeto
    project_language = detect_project_language(args.project_path)

    # Obtém a lista de arquivos modificados que ainda não foram adicionados ao índice
    status_output, _ = run_git_command(['git', 'status'])

    # Obtém as alterações detalhadas
    diff_output, _ = run_git_command(['git', 'diff'])

    # Gera a mensagem de commit
    commit_message = generate_commit_message(status_output + "\n" + diff_output, project_language, args.base_message)

    print("\n\nMensagem de commit gerada:\n")
    print(commit_message)
    print("\n")

    # Faz o commit
    commit_changes(commit_message)
    print("-> Gitai concluiu o commit com sucesso.")

    # Se push_after_commit for true, executa git push
    if args.push:
        # Verifica se existem atualizações remotas
        run_git_command(['git', 'fetch'])  # Atualiza as informações locais
        status_output, _ = run_git_command(['git', 'status', '-uno'])

        if 'have diverged' in status_output:
            print(f"Existem alterações remotas no branch atual, faça merge primeiro antes de fazer push.\nMsg:\n{status_output}")
            sys.exit(1)  # Interrompe o script se houver alterações remotas

        run_git_command(['git', 'push'])
        print("-> Gitai concluiu o push com sucesso.")


if __name__ == "__main__":
    main()
