import os
import subprocess
import sys
from textwrap import dedent
import argparse
from datetime import datetime

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
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
else:
    print(f'Erro: Provedor {provider} não suportado.')
    sys.exit(1)


def run_git_command(command):
    """Executa um comando git e retorna a saída."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando:\n-> {command}\nerror: {e.stderr}")
        print(f"\n\nSaída de erro padrão:\n {e.output}")
        sys.exit(1)


def get_commit_messages_since_tag(tag):
    """Obtém todas as mensagens de commit desde a tag especificada."""
    command = ['git', 'log', f'{tag}..HEAD', '--pretty=format:%h %s']
    return run_git_command(command).split('\n')


def generate_release_notes(commits, new_version, tag):
    """Gera as notas de release com base nos commits fornecidos."""
    prompt = dedent(f"""
    Você é um assistente que ajuda a gerar notas de release para um repositório Git. 
    Abaixo estão os commits desde a última tag {tag}. 
    Por favor, organize os commits nas seguintes categorias: Novidades, Correções e Outras alterações. 
    Gere uma mensagem de release em formato markdown no idioma '{language}' usando o seguinte modelo:

    ```
    # Release {new_version}
    <SUMMARY/>

    ### New
    - Descrição das novidades (commits).

    ### Fix
    - Descrição das correções (commits).

    ### Other changes
    - Descrição de outras alterações (commits).

    Agradecemos a todos os colaboradores que tornaram esta release possível! Para mais detalhes, consulte as notas completas da versão.

    **Full Changelog:** [Ver commits de {new_version}](https://github.com/leandrosilvaferreira/gitai/compare/{tag}...{new_version})
    ```

    Commits:
    {commits}
    
    Regras importantes:
        - O conteúdo gerado deve obrigatoriamente utilizar o idioma '{language}'.
        - Substituir <SUMMARY/> do modelo por um resumo de forma objetiva e entusiasmada das alterações realizadas desde a última tag {tag}
        - NÃO adicione comentários ou explicações adicionais.
        - NÃO utilize símbolos como ``` para identificar a mensagem de commit.
        - A mensagem deve ser clara, concisa, bem organizada.
        - Lembre-se de seguir o modelo fornecido.
        
    Se as instruções não forem seguidas corretamente, o resultado não será aceito.
    """)

    return call_provider_api(prompt)


def call_provider_api(prompt):
    messages = [
        {
            "role": "system",
            "content": dedent("""
                                Você é um assistente que ajuda a gerar notas de release para um repositório Git. 
                                As mensagens de commit devem ser organizadas em categorias como Novidades, Correções e Outras alterações. 
                                A saída deve ser um texto em markdown formatado conforme o modelo fornecido, sem comentários ou formatação adicional.
                            """)
        },
        {"role": "user", "content": prompt}
    ]

    """Chama a API do provedor especificado (OpenAI ou Groq) para gerar o conteúdo."""
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
        case _:
            print(f'Erro: Provedor {provider} não suportado.')
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Gerador de notas de release para o Git.',
        usage="releaser.py <tag_antiga> <nova_versao>"
    )
    parser.add_argument('old_tag', type=str, help='A tag antiga do Git.')
    parser.add_argument('new_version', type=str, help='A nova versão para a release.')

    args = parser.parse_args()

    commits = get_commit_messages_since_tag(args.old_tag)
    formatted_commits = '\n'.join(commits)

    release_notes = generate_release_notes(formatted_commits, args.new_version, args.old_tag)

    release_filename = os.path.join('dist', f"release_{args.new_version}.md")
    os.makedirs('dist', exist_ok=True)  # Certifica-se de que a pasta 'dist' existe
    with open(release_filename, 'w') as file:
        file.write(release_notes)

    print(f"Notas de release geradas com sucesso em {release_filename}.")


if __name__ == "__main__":
    main()
