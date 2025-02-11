# Gitai - Automated Conventional Commits in Git with AI

Choose your language / Escolha o idioma:
- 🇺🇸 [English](#-english)
- 🇧🇷 [Português](#-português)

---

# 🇺🇸 English

[![Release Notes](https://img.shields.io/github/release/leandrosilvaferreira/gitai)](https://github.com/leandrosilvaferreira/gitai/releases)
[![GitHub star chart](https://img.shields.io/github/stars/leandrosilvaferreira/gitai?style=social)](https://star-history.com/#leandrosilvaferreira/gitai)
[![GitHub fork](https://img.shields.io/github/forks/leandrosilvaferreira/gitai?style=social)](https://github.com/leandrosilvaferreira/gitai/fork)

Gitai is a Python project that serves as an automation tool for managing Git commits. It is designed to analyze projects written in various programming languages, including Node.js, Python, Java, Go, and PHP.

The application analyzes the changes made in a project, identifies the programming language used, and based on that, generates a detailed commit message following the Conventional Commits standard. This standard is widely adopted to make commit messages more descriptive and useful.

Additionally, Gitai automates the commit process by adding all changes to the Git staging area, committing with the generated message, and optionally pushing the changes to the remote repository.

For generating the commit message, you can choose between the advanced language models from `OpenAI` or `Groq`.

The project also uses the libraries `openai`, `groq`, `python-dotenv`, and `pyinstaller` to create an executable that includes the dependencies of the virtual environment and reads environment variables from a `.env` file located in the same folder as the executable.

## 💻 Screenshot

![Gitai](docs/gitai.jpg)

![Gitai](docs/commits.jpg)

## 🎥 Video Tutorial

Click the image below to watch the video tutorial about Gitai:

[![AUTOMATED GIT COMMITS WITH AI: GITAI (OPEN SOURCE AND FREE)](http://img.youtube.com/vi/GAQ4mmGxg7c/0.jpg)](https://www.youtube.com/watch?v=GAQ4mmGxg7c "AUTOMATED GIT COMMITS WITH AI: GITAI (OPEN SOURCE AND FREE)")

## ⚡ Installing the Application on Mac

After generating the `.pkg` file, you can follow the steps below to install the application on your Mac:

1. Navigate to the location where the `.pkg` file was saved.
2. Double-click the `.pkg` file to launch the installer.
3. Follow the on-screen instructions to install the application. You may be required to enter your administrator password.
4. After installation, the application will be available in your Applications directory.

Remember that after installation, you must configure the `.env` file with the necessary environment variables for the application to function correctly.

## 🤖 Choosing the AI Model

Gitai supports two AI providers for generating commit messages: `OpenAI` and `Groq`.

Each has its own characteristics, costs, and usage limits.

Both providers are highly capable, but your choice may depend on your specific needs and available budget.

If you need high processing power and can cover the costs, OpenAI is an excellent option. On the other hand, if you prefer a free service and can manage within usage limits, Groq is a viable and efficient alternative.

Below is detailed information about each provider to help you choose the best one for your needs.

### OpenAI

OpenAI is a paid service that offers advanced language models.

The most efficient available model is `gpt-4o`, which has a context window of 128K tokens.

- **Cost**: 
  - $2.50 per 1M tokens for Input
  - $10.00 per 1M tokens for Output
- **Website**: [OpenAI](https://platform.openai.com/docs/introduction)

### Groq

Groq is a free service, but with usage limits.

The recommended model is `mixtral-8x7b-32768`, which offers a context window of 32,768 tokens.

- **Usage Limits**:
  - **Requests per Minute**: 30
  - **Requests per Day**: 14,400
  - **Tokens per Minute**: 5,000
- **Website**: [Groq](https://console.groq.com/)

## 🌱 Configuring the .env

Before running the application, you need to configure the `.env` file in the `dist` folder or in the folder where Gitai was installed. This file contains the environment variables required for the application to function correctly.

You can choose to use either the `OpenAI` provider or `Groq`.

Open the `.env` file in a text editor and fill in the environment variables.

### Example configuration for OpenAI

```dotenv
PROVIDER=openai
API_KEY=your_openai_api_key
MODEL=gpt-4o
LANGUAGE=en
```

### Example configuration for Groq

```dotenv
PROVIDER=groq
API_KEY=your_groq_api_key
MODEL=mixtral-8x7b-32768
LANGUAGE=en
```

## 💻 Adding the Application to the Terminal

To make the application available in the terminal, you need to add the application directory to your system's `PATH`. The `PATH` is an environment variable that specifies a list of directories where executable commands are searched for.

You can add the application's directory to the `PATH` by appending the following line to your `.bash_profile` or `.zshrc` file (depending on the shell you are using) in your home directory:

```bash
export PATH="$PATH:/Applications/Gitai/"
```

After adding this line, you need to execute the `source` command to load the changes:

```bash
source ~/.bash_profile  # If you are using bash
source ~/.zshrc  # If you are using zsh
```

Now, you should be able to run the application from the terminal.

## 🚀 Using Gitai

After installing and configuring Gitai, you can start using it to automatically generate commit messages for your project.

To use Gitai, open the terminal in your project's root directory. This is important because Gitai needs access to your project's files to analyze the changes and generate commit messages.

Once the terminal is open in your project's root, you can run Gitai with the following command:

```bash
gitai <project_path> '<generic_message>'
```

Replace `<project_path>` with the path to your project's directory and `<generic_message>` with a basic description of the change you made in the project.

For example, if you have the terminal open in your project's root and the change was to add a new feature, you can simply type:

```bash
gitai . 'Added new feature'
```

If you wish to analyze only a specific folder or a project in another directory, for example, if you made a change in your project located at `/Users/username/MyProject`, you can run Gitai with the following command:

```bash
gitai /Users/username/MyProject 'Added new feature'
```

To automatically generate the commit and push it, you can add the `--push` flag to the command:

```bash
gitai . 'Added new feature' --push
```

## 🚀 Generating Release Notes

The `releaser.py` script is used to generate release notes for any Git project. It analyzes the commits made since the last tag and generates a detailed release document.

For detailed instructions on how to use the `releaser.py` script, please refer to the [RELEASER.md](RELEASER.md) document.

## 👨‍💻 Development

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- git

### Environment Setup

1. Clone the repository to your local machine using `git clone`.

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory.

   ```bash
   cd <project-name>
   ```

3. Install the project dependencies.

   ```bash
   pip install -r requirements.txt
   ```

### Generating the Executable

To build the project, run the `build.sh` script in the root of the project.

```bash
./build.sh
```

This script will generate an executable of the Python script using PyInstaller called `gitai` and will copy the `.env.example` file to the `dist` folder.

If you want to generate an executable for a specific platform, you can use the following commands:

### Generating the Installer for Windows

To generate an installer for Windows, you need to use the Inno Setup tool.

#### Installing Inno Setup

1. Visit the official Inno Setup website at [http://www.jrsoftware.org/isinfo.php](http://www.jrsoftware.org/isinfo.php).
2. Click on the "Download" link on the page.
3. Download the latest version of Inno Setup.
4. After downloading the `.exe` file, open it.
5. Follow the on-screen instructions to install Inno Setup.
6. After installation, Inno Setup should be available on your computer.
7. Open Inno Setup and click on "File" > "New" to create a new installation script.
8. Fill in your project details, such as name, version, and description.
9. Add the necessary files to the installer, including the executable generated by PyInstaller and the example `.env` file.
10. Configure the installation options, such as the installation directory and shortcuts.
11. Click on "Build" to generate the installer.
12. After building, you will have an `.exe` file that can be distributed and used to install your application on Windows.
13. Run the installer on the target computer to install the application.
14. After installation, the application will be available in the Start menu and in the installation directory.

### Generating the Installer for Linux

To generate an installer for Linux, you need to use the Makeself tool.

#### Installing Makeself

1. Visit the official Makeself website at [https://makeself.io/](https://makeself.io/).
2. Click on the "Download" link on the page.
3. Download the latest version of Makeself.
4. After downloading the `.run` file, open it.
5. Follow the on-screen instructions to install Makeself.
6. After installation, Makeself should be available on your computer.
7. Open the terminal and navigate to the directory where the executable generated by PyInstaller is located.
8. Execute the following command to create the installer:

   ```bash
   makeself <source_directory> <installer_name> "<installer_description>" <installation_command>
   ```

   Replace `<source_directory>` with the directory where the executable is located, `<installer_name>` with the name of the installer file, `<installer_description>` with a description of the installer, and `<installation_command>` with an installation command.

   For example:

   ```bash
   makeself dist/ GitaiInstaller.run "Gitai Installer" "./gitai"
   ```

This will create a `.run` file that can be distributed and used to install your application on Linux.

### Generating the Installer for macOS

To generate an installer for macOS, you need to use the Packages tool.

#### Installing Packages

1. Visit the official Packages website at [http://s.sudre.free.fr/Software/Packages/about.html](http://s.sudre.free.fr/Software/Packages/about.html).
2. Click on the "Download" link on the page.
3. After downloading the `.dmg` file, open it.
4. Drag the Packages icon to the Applications folder.

Now, Packages should be installed and ready to use on your Mac.

#### Creating the Installer

1. Open Packages and click on "New Project".
2. Select "Distribution" and click "Next".
3. Give your project a name and choose where to save it.
4. In the left panel, click on "Project" and fill in your project details.
5. In the left panel, click on "Settings" and configure the installation options.
6. In the left panel, click on "Scripts" and add a post-installation script that installs the necessary Python libraries.
7. In the left panel, click on "Payload" and add the executable and the example `.env` file to the installation directory.
8. In the "Build" menu, select "Build".

This will create a `.pkg` file that installs your application.

Gitai will analyze the changes made in your project, identify the programming language used, and based on that, generate a detailed commit message following the Conventional Commits standard. Then, it will add all changes to the Git staging area and commit with the generated message.

## 📝 TODO

- [x] Generate release for Mac
- [x] Generate release for Windows
- [x] Generate release for Linux
- [x] Update the documentation to include installation instructions for Windows and Linux
- [x] Add the possibility of using the GROQ API to generate commit messages
- [x] Translate the documentation to English
- [x] Translate prompts to English
- [ ] Automatically add the executable binary to the PATH
- [ ] Add support for more programming languages
- [ ] Add automated tests

## 🙌 Contributing

We appreciate your interest in contributing to Gitai! Here are some guidelines to help you through the process:

1. **Fork the Repository**: Fork the Gitai repository to your GitHub account. This means you will have a copy of the repository in your own account, allowing you to make changes without affecting the original project.
2. **Clone the Repository**: Clone the repository to your local machine so that you can make changes.
3. **Create a Branch**: Create a new branch in your fork for your changes. This helps separate your changes from others that may be happening simultaneously.
4. **Make Your Changes**: Make the changes that you believe will improve the project. This can be adding a new feature, fixing a bug, or improving the documentation.
5. **Test Your Changes**: Ensure that your changes do not break anything and that the code still works as expected.
6. **Submit a Pull Request**: Submit a pull request to the original repository proposing your changes. Make sure to provide a detailed description of your changes so that the project maintainers can understand what you did and why.

## 📄 Code of Conduct

We ask that all contributors follow our code of conduct. Mutual respect is essential for a healthy collaborative environment. Please be professional and respectful to all contributors.

## 🙋 Support

If you have any questions or issues, please open an issue. We will do our best to help you.

## 📨 Contact

If you wish to contact the project maintainers, please send an email to: [leandro@notyped.com](mailto:leandro@notyped.com)

Thank you for your interest in our project. We look forward to your contributions!

## 🤓 Author

**Leandro Silva Ferreira**

- GitHub: [@leandrosilvaferreira](https://github.com/leandrosilvaferreira)
- Twitter: [@leandrosfer](https://twitter.com/leandrosfer)
- Email: [leandro@notyped.com](mailto:leandro@notyped.com)
- LinkedIn: [Leandro Ferreira](https://www.linkedin.com/in/leandrosilvaferreira/)

## 👨‍💻 Last 30 Days Activity

![Alt](https://repobeats.axiom.co/api/embed/0202ff53ce643fbe0bbb419d2addc4aafd2313a6.svg "Repobeats analytics image")

## 🙌 Contributors

Thanks to these amazing contributors

<a href="https://github.com/leandrosilvaferreira/gitai/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=leandrosilvaferreira/gitai" />
</a>

[![Star History Chart](https://api.star-history.com/svg?repos=leandrosilvaferreira/gitai&type=Timeline)](https://star-history.com/#leandrosilvaferreira/gitai&Date)

## 📄 License

This project is licensed under the MIT License. This means you are free to copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided that you give appropriate credit to the original author and reproduce the license in all copies or substantial portions of the software.

For more details, see the [LICENSE](LICENSE.md) file in the repository.

---

## 🇧🇷 Português

# Gitai - Conventional Commits automatizados no Git com IA

[![Release Notes](https://img.shields.io/github/release/leandrosilvaferreira/gitai)](https://github.com/leandrosilvaferreira/gitai/releases)
[![GitHub star chart](https://img.shields.io/github/stars/leandrosilvaferreira/gitai?style=social)](https://star-history.com/#leandrosilvaferreira/gitai)
[![GitHub fork](https://img.shields.io/github/forks/leandrosilvaferreira/gitai?style=social)](https://github.com/leandrosilvaferreira/gitai/fork)

Gitai é um projeto Python que serve como uma ferramenta de automação para gerenciamento de commits no Git. Ele é projetado para analisar projetos escritos em várias linguagens de programação, incluindo Node.js, Python, Java, Go e PHP.

A aplicação analisa as alterações feitas em um projeto, identifica a linguagem de programação usada e, com base nisso, gera uma mensagem de commit detalhada seguindo o padrão Conventional Commits. Este padrão é amplamente adotado para tornar as mensagens de commit mais descritivas e úteis.

Além disso, Gitai automatiza o processo de commit, adicionando todas as alterações ao índice do Git, realizando o commit com a mensagem gerada e, opcionalmente, fazendo push das alterações para o repositório remoto.

Para a geração da mensagem de commit, é possível escolher entre os modelos de linguagem avançados da `OpenAI` ou `Groq`.

O projeto também utiliza as bibliotecas `openai`, `groq`, `python-dotenv` e `pyinstaller` para criar um executável que inclui as dependências do ambiente virtual e que lê as variáveis de ambiente de um arquivo `.env` na mesma pasta que o executável.

## 💻 Screenshot

![Gitai](docs/gitai.jpg)

![Gitai](docs/commits.jpg)

## 🎥 Tutorial em Vídeo

Clique na imagem abaixo para assistir ao tutorial em vídeo sobre o Gitai:

[![AUTOMATIZAÇÃO DE COMMITS DO GIT COM IA: GITAI (OPEN SOURCE E GRATUITO)](http://img.youtube.com/vi/GAQ4mmGxg7c/0.jpg)](https://www.youtube.com/watch?v=GAQ4mmGxg7c "AUTOMATIZAÇÃO DE COMMITS DO GIT COM IA: GITAI (OPEN SOURCE E GRATUITO)")


## ⚡ Instalando a Aplicação no Mac

Depois de gerar o arquivo `.pkg`, você pode seguir os passos abaixo para instalar a aplicação no seu Mac:

1. Navegue até o local onde o arquivo `.pkg` foi salvo.
2. Dê um duplo clique no arquivo `.pkg` para iniciar o instalador.
3. Siga as instruções na tela para instalar a aplicação. Você pode precisar inserir sua senha de administrador.
4. Após a instalação, a aplicação estará disponível no seu diretório de Aplicativos.

Lembre-se de que, após a instalação, você deve configurar o arquivo `.env` com as variáveis de ambiente necessárias para a aplicação funcionar corretamente.

## 🤖 Escolhendo o Modelo de IA

O Gitai oferece suporte a dois provedores de IA para gerar mensagens de commit: `OpenAI` e `Groq`. 

Cada um tem suas características, custos e limites de utilização. 

Ambos os provedores são altamente capazes, mas sua escolha pode depender de suas necessidades específicas e do orçamento disponível. 

Se você precisa de uma grande capacidade de processamento e pode arcar com os custos, OpenAI é uma excelente opção. Por outro lado, se você prefere um serviço sem custo e pode gerenciar dentro dos limites de utilização, Groq é uma alternativa viável e eficiente.

Abaixo estão as informações detalhadas sobre cada provedor para ajudá-lo a escolher o melhor para suas necessidades.

### OpenAI

OpenAI é um serviço pago que oferece modelos de linguagem avançados. 

O modelo mais eficiente disponível é o `gpt-4o`, que tem uma janela de contexto de 128K tokens. 

- **Custo**: 
  - $2.50 por 1M tokens para Input
  - $10.00 por 1M tokens para Output
- **Site**: [OpenAI](https://platform.openai.com/docs/introduction)

### Groq

Groq é um serviço gratuito, mas com limites de utilização. 

O modelo recomendado é o `mixtral-8x7b-32768`, que oferece uma janela de contexto de 32,768 tokens.

- **Limites de Utilização**:
  - **Requests por Minuto**: 30
  - **Requests por Dia**: 14,400
  - **Tokens por Minuto**: 5,000
- **Site**: [Groq](https://console.groq.com/)



## 🌱 Configurando o .env

Antes de executar o aplicativo, você precisa configurar o arquivo `.env` na pasta `dist` ou na pasta onde o GITAI foi instalado. Este arquivo contém as variáveis de ambiente que o aplicativo precisa para funcionar corretamente.

Você pode escolher entre usar o provedor `OpenAI` ou `Groq`.

Abra o arquivo `.env` em um editor de texto e preencha as variáveis de ambiente.

### Exemplo de configuração para OpenAI

```dotenv
PROVIDER=openai
API_KEY=your_openai_api_key
MODEL=gpt-4o
LANGUAGE=en
```

### Exemplo de configuração para Groq

```dotenv
PROVIDER=groq
API_KEY=your_groq_api_key
MODEL=mixtral-8x7b-32768
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
Para gerar o commit e fazer push de forma automática, você pode adicionar a flag `--push` ao comando:

```bash
gitai . 'Adicionada nova funcionalidade' --push
```

## 🚀 Gerando Notas de Lançamento (Release Notes)

O script `releaser.py` é usado para gerar notas de lançamento para qualquer projeto Git. Ele analisa os commits feitos desde a última tag e gera um documento de lançamento detalhado.

Para instruções detalhadas sobre como usar o script `releaser.py`, consulte o documento [RELEASER.md](RELEASER.md).

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

### Gerando o executável

Para executar o build do projeto, execute o script `build.sh` na raiz do projeto.

```bash
./build.sh
```

Este script irá gerar um executável do script Python usando o PyInstaller chamado `gitai` e copiará o arquivo `.env.example` para a pasta `dist`.

Caso você queira gerar um executável para uma plataforma específica, você pode usar os seguintes comandos:

### Gerando o Instalador para Windows

Para gerar um instalador para Windows, você precisa usar a ferramenta Inno Setup.

#### Instalando o Inno Setup

1. Acesse o site oficial do Inno Setup em http://www.jrsoftware.org/isinfo.php
2. Clique no link "Download" na página.
3. Baixe a versão mais recente do Inno Setup.
4. Após o download do arquivo `.exe`, abra-o.
5. Siga as instruções na tela para instalar o Inno Setup.
6. Após a instalação, o Inno Setup deve estar disponível no seu computador.
7. Abra o Inno Setup e clique em "File" > "New" para criar um novo script de instalação.
8. Preencha os detalhes do seu projeto, como nome, versão e descrição.
9. Adicione os arquivos necessários ao instalador, incluindo o executável gerado pelo PyInstaller e o arquivo `.env` de exemplo.
10. Configure as opções de instalação, como o diretório de instalação e os atalhos.
11. Clique em "Build" para gerar o instalador.
12. Após a compilação, você terá um arquivo `.exe` que pode ser distribuído e usado para instalar o seu aplicativo no Windows.
13. Execute o instalador no computador de destino para instalar o aplicativo.
14. Após a instalação, o aplicativo estará disponível no menu Iniciar e no diretório de instalação.

### Gerando o Instalador para Linux

Para gerar um instalador para Linux, você precisa usar a ferramenta Makeself.

#### Instalando o Makeself

1. Acesse o site oficial do Makeself em https://makeself.io/
2. Clique no link "Download" na página.
3. Baixe a versão mais recente do Makeself.
4. Após o download do arquivo `.run`, abra-o.
5. Siga as instruções na tela para instalar o Makeself.
6. Após a instalação, o Makeself deve estar disponível no seu computador.
7. Abra o terminal e navegue até o diretório onde o executável gerado pelo PyInstaller está localizado.
8. Execute o seguinte comando para criar o instalador:

```bash
makeself <diretório_de_origem> <nome_do_instalador> "<descrição_do_instalador>" <comando_de_instalação>
```

Substitua `<diretório_de_origem>` pelo diretório onde o executável gerado pelo PyInstaller está localizado, `<nome_do_instalador>` pelo nome do arquivo do instalador, `<descrição_do_instalador>` por uma descrição do instalador e `<comando_de_instalação>` por um comando de instalação.

Por exemplo:

```bash
makeself dist/ GitaiInstaller.run "Instalador do Gitai" "./gitai"
```

Isso irá criar um arquivo `.run` que pode ser distribuído e usado para instalar o seu aplicativo no Linux.

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

## 📝 TODO

- [x] Gerar release para Mac
- [x] Gerar release para Windows
- [x] Gerar release para Linux
- [x] Atualizar a documentação para incluir instruções de instalação para Windows e Linux
- [x] Adicionar possibilidade de utilizar a API do GROQ para gerar mensagens de commit
- [x] Traduzir a documentação para Inglês
- [x] Traduzir prompts para Inglês 
- [ ] Adicionar binário executável automaticamente no PATH
- [ ] Adicionar suporte para mais linguagens de programação
- [ ] Adicionar testes automatizados


## 🙌 Contribuindo

Agradecemos o seu interesse em contribuir para o Gitai! Aqui estão algumas diretrizes que podem ajudá-lo no processo:

1. **Fork o Repositório**: Faça um fork do repositório Gitai para a sua conta do GitHub. Isso significa que você terá uma cópia do repositório em sua própria conta, permitindo que você faça alterações sem afetar o projeto original.

2. **Clone o Repositório**: Clone o repositório para a sua máquina local para que você possa fazer alterações.

3. **Crie uma Branch**: Crie uma nova branch em seu fork para fazer suas alterações. Isso ajuda a separar suas alterações de outras que possam estar acontecendo simultaneamente.

4. **Faça suas Alterações**: Faça as alterações que você acha que melhorariam o projeto. Isso pode ser a adição de uma nova funcionalidade, a correção de um bug ou a melhoria da documentação.

5. **Teste suas Alterações**: Certifique-se de que suas alterações não quebram nada e que o código ainda funciona como esperado.

6. **Envie um Pull Request**: Envie um pull request para o repositório original propondo suas alterações. Certifique-se de dar uma descrição detalhada de suas alterações para que os mantenedores do projeto possam entender o que você fez e por quê.

## 📄 Código de Conduta

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

## 👨‍💻 Atividades últimos 30 dias

![Alt](https://repobeats.axiom.co/api/embed/0202ff53ce643fbe0bbb419d2addc4aafd2313a6.svg "Repobeats analytics image")

## 🙌 Contribuidores

Obrigado a estes incríveis contribuidores

<a href="https://github.com/leandrosilvaferreira/gitai/graphs/contributors">
<img src="https://contrib.rocks/image?repo=leandrosilvaferreira/gitai" />
</a>

[![Star History Chart](https://api.star-history.com/svg?repos=leandrosilvaferreira/gitai&type=Timeline)](https://star-history.com/#leandrosilvaferreira/gitai&Date)

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Isso significa que você é livre para copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software, desde que forneça o devido crédito ao autor original e reproduza a licença em todas as cópias ou partes substanciais do software.

Para mais detalhes, veja o arquivo [LICENSE](LICENSE.md) no repositório.
