# Gitai - Automatize seus Commits no Git com IA

[![Release Notes](https://img.shields.io/github/release/leandrosilvaferreira/gitai)](https://github.com/leandrosilvaferreira/gitai/releases)
[![GitHub star chart](https://img.shields.io/github/stars/leandrosilvaferreira/gitai?style=social)](https://star-history.com/#leandrosilvaferreira/gitai)
[![GitHub fork](https://img.shields.io/github/forks/leandrosilvaferreira/gitai?style=social)](https://github.com/leandrosilvaferreira/gitai/fork)

Gitai é um projeto Python que serve como uma ferramenta de automação para gerenciamento de commits no Git. Ele é projetado para analisar projetos escritos em várias linguagens de programação, incluindo Node.js, Python, Java, Go e PHP.

A aplicação analisa as alterações feitas em um projeto, identifica a linguagem de programação usada e, com base nisso, gera uma mensagem de commit detalhada seguindo o padrão Conventional Commits. Este padrão é amplamente adotado para tornar as mensagens de commit mais descritivas e úteis.

Além disso, Gitai automatiza o processo de commit, adicionando todas as alterações ao índice do Git, realizando o commit com a mensagem gerada e, opcionalmente, fazendo push das alterações para o repositório remoto.

O projeto também utiliza as bibliotecas `openai`, `python-dotenv` e `pyinstaller` para criar um executável que inclui as dependências do ambiente virtual e que lê as variáveis de ambiente de um arquivo `.env` na mesma pasta que o executável.

## ⚡ Instalando a Aplicação

Depois de gerar o arquivo `.pkg`, você pode seguir os passos abaixo para instalar a aplicação no seu Mac:

1. Navegue até o local onde o arquivo `.pkg` foi salvo.
2. Dê um duplo clique no arquivo `.pkg` para iniciar o instalador.
3. Siga as instruções na tela para instalar a aplicação. Você pode precisar inserir sua senha de administrador.
4. Após a instalação, a aplicação estará disponível no seu diretório de Aplicativos.

Lembre-se de que, após a instalação, você deve configurar o arquivo `.env` com as variáveis de ambiente necessárias para a aplicação funcionar corretamente.

## 🌱 Configurando o .env

Antes de executar o aplicativo, você precisa configurar o arquivo `.env` na pasta `dist`. Este arquivo contém as variáveis de ambiente que o aplicativo precisa para funcionar corretamente.

Abra o arquivo `.env` em um editor de texto e preencha as variáveis de ambiente. Por exemplo:

```dotenv
OPENAI_API_KEY=your_openai_api_key
LANGUAGE=en
```

## 💻 Adicionando o Aplicativo ao Terminal

Para tornar o aplicativo disponível no terminal, você precisa adicionar o diretório do aplicativo ao `PATH` do sistema. O `PATH` é uma variável de ambiente que especifica uma lista de diretórios onde os comandos executáveis são procurados.

Você pode adicionar o diretório do aplicativo ao `PATH` adicionando a seguinte linha ao arquivo `.bash_profile` ou `.zshrc` (dependendo do shell que você está usando) no diretório inicial do usuário:

```bash
export PATH="$PATH:/Applications/Gitai/"
```

Depois de adicionar essa linha, você precisa executar o comando `source` para carregar as alterações:

```bash
source ~/.bash_profile  # Se você estiver usando bash
source ~/.zshrc  # Se você estiver usando zsh
```

Agora, você deve ser capaz de executar o aplicativo a partir do terminal.

## 🚀 Usando o Gitai

Depois de instalar e configurar o Gitai, você pode começar a usá-lo para gerar mensagens de commit automaticamente para o seu projeto.

Para usar o Gitai, você precisa abrir o terminal na raiz do seu projeto. Isso é importante porque o Gitai precisa ter acesso aos arquivos do seu projeto para analisar as alterações e gerar as mensagens de commit.

Uma vez que o terminal esteja aberto na raiz do seu projeto, você pode executar o Gitai com o seguinte comando:

```bash
gitai <caminho_do_projeto> '<mensagem_genérica>'
```

Substitua `<caminho_do_projeto>` pelo caminho do diretório do seu projeto e `<mensagem_genérica>` por uma descrição básica da mudança que você fez no projeto.

Se você estiver com o terminal aberto na raiz do seu projeto e a mudança foi para adicionar uma nova funcionalidade, você pode simplesmente digitar:

```bash
gitai . 'Adicionada nova funcionalidade'
```

Se você deseja analisar somente uma pasta específica ou um projeto em outra pasta, por exemplo, se você fez uma alteração no seu projeto localizado em `/Users/username/MeuProjeto`, você pode executar o Gitai com o seguinte comando:

```bash
gitai /Users/username/MeuProjeto 'Adicionada nova funcionalidade'
```

## 👨‍💻 Desenvolvimento

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)
- git

### Configuração do Ambiente

1. Clone o repositório para a sua máquina local usando `git clone`.

```bash
git clone <url-do-repositorio>
```

2. Navegue até o diretório do projeto.

```bash
cd <nome-do-projeto>
```

3. Instale as dependências do projeto.

```bash
pip install -r requirements.txt
```

### Gerando o Build

Para gerar o build do projeto, execute o script `build.sh` na raiz do projeto.

```bash
./build.sh
```

Este script irá gerar um executável do script Python usando o PyInstaller e copiará o arquivo `.env.example` para a pasta `dist`.

### Gerando o Instalador para macOS

Para gerar um instalador para macOS, você precisa usar a ferramenta Packages.

#### Instalando o Packages

1. Acesse o site oficial do Packages em http://s.sudre.free.fr/Software/Packages/about.html
2. Clique no link "Download" na página.
3. Após o download do arquivo `.dmg`, abra-o.
4. Arraste o ícone do Packages para a pasta de Aplicativos.

Agora, o Packages deve estar instalado e pronto para uso no seu Mac.

#### Criando o Instalador

1. Abra o Packages e clique em "New Project".
2. Selecione "Distribution" e clique em "Next".
3. Dê um nome ao seu projeto e escolha onde salvá-lo.
4. No painel esquerdo, clique em "Project" e preencha os detalhes do seu projeto.
5. No painel esquerdo, clique em "Settings" e configure as opções de instalação.
6. No painel esquerdo, clique em "Scripts" e adicione um script de pós-instalação que instala as bibliotecas Python necessárias.
7. No painel esquerdo, clique em "Payload" e adicione o executável e o arquivo `.env` de exemplo ao diretório de instalação.
8. No menu "Build", selecione "Build".

Isso irá criar um arquivo `.pkg` que instala o seu aplicativo.

O Gitai irá analisar as alterações feitas no seu projeto, identificar a linguagem de programação usada e, com base nisso, gerar uma mensagem de commit detalhada seguindo o padrão Conventional Commits. Em seguida, ele irá adicionar todas as alterações ao índice do Git e realizar o commit com a mensagem gerada.

## 🙌 Contribuindo

Agradecemos o seu interesse em contribuir para o Gitai! Aqui estão algumas diretrizes que podem ajudá-lo no processo:

1. **Fork o Repositório**: Faça um fork do repositório Gitai para a sua conta do GitHub. Isso significa que você terá uma cópia do repositório em sua própria conta, permitindo que você faça alterações sem afetar o projeto original.

2. **Clone o Repositório**: Clone o repositório para a sua máquina local para que você possa fazer alterações.

3. **Crie uma Branch**: Crie uma nova branch em seu fork para fazer suas alterações. Isso ajuda a separar suas alterações de outras que possam estar acontecendo simultaneamente.

4. **Faça suas Alterações**: Faça as alterações que você acha que melhorariam o projeto. Isso pode ser a adição de uma nova funcionalidade, a correção de um bug ou a melhoria da documentação.

5. **Teste suas Alterações**: Certifique-se de que suas alterações não quebram nada e que o código ainda funciona como esperado.

6. **Envie um Pull Request**: Envie um pull request para o repositório original propondo suas alterações. Certifique-se de dar uma descrição detalhada de suas alterações para que os mantenedores do projeto possam entender o que você fez e por quê.

## 📄Código de Conduta

Pedimos que todos os contribuintes sigam nosso código de conduta. Respeito mútuo é fundamental para um ambiente de colaboração saudável. Por favor, seja profissional e respeitoso com os outros contribuintes.

## 🙋 Suporte

Se você tiver alguma dúvida ou problema, por favor, abra uma issue. Faremos o nosso melhor para ajudá-lo.

## 📨 Contato

Se você quiser entrar em contato com os mantenedores do projeto, por favor, envie um e-mail para: [leandro@notyped.com](mailto:leandro@notyped.com)

Obrigado por seu interesse em nosso projeto. Estamos ansiosos para ver suas contribuições!

## 🤓 Autor

**Leandro Silva Ferreira**

- GitHub: [@leandrosilvaferreira](https://github.com/leandrosilvaferreira)
- Twitter: [@leandrosfer](https://twitter.com/leandrosfer)
- Email: [leandro@notyped.com](mailto:leandro@notyped.com)
- LinkedIn: [Leandro Ferreira](https://www.linkedin.com/in/leandrosilvaferreira/)

## 🙌 Contribuidores

Obrigado a estes incríveis contribuidores

<a href="https://github.com/leandrosilvaferreira/gitai/graphs/contributors">
<img src="https://contrib.rocks/image?repo=leandrosilvaferreira/gitai" />
</a>

[![Star History Chart](https://api.star-history.com/svg?repos=leandrosilvaferreira/gitai&type=Timeline)](https://star-history.com/#leandrosilvaferreira/gitai&Date)

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Isso significa que você é livre para copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software, desde que forneça o devido crédito ao autor original e reproduza a licença em todas as cópias ou partes substanciais do software.

Para mais detalhes, veja o arquivo [LICENSE](LICENSE.md) no repositório.