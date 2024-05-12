# AutoGemini
AutoGemini é um ChatBot que possui o poder de executar código Python para interagir com o usuário. Ele foi desenvolvido com o intuito de auxiliar em todos os tipos de tarefas, desde cálculos matemáticos, análise de dados e até mesmo tarefas como organizar arquivos.

## Como funciona?
O AutoGemini utiliza a API do Google Gemini para interpretar as prompts do usuário, respondendo com texto e/ou código Python. O código é executado, e o resultado é retornado para o Gemini.

O ChatBot ao realizar uma tarefa que foi solicitada pelo usuário, caso necessário, ele irá utilizar Python para explorar o problema e resolve-lo.

Tarefas complexas, o AutoGemini irá quebrar em partes menores e resolver cada uma delas, como por exemplo, explorar um arquivo csv com pandas, antes de processar os dados.

## Como utilizar?
Crie um arquivo `.env` na raiz do projeto seguindo o modelo do arquivo `.env.example` e preencha as variáveis de ambiente.
Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```
Execute o arquivo `main.py`:
```bash
python main.py
```
Obs: É interessante que você utilize um ambiente virtual para instalar as dependências, o AutoGemini pode instalar mais dependências durante a execução.

Dentro do arquivo `definition.txt` você pode editar o prompt inicial do ChatBot, e contextualizar para o seu sistema, caso necessário.

## Exemplo de uso
### Organizar arquivos por tipo de extensão

[![Video - Organizar Arquivos](https://img.youtube.com/vi/Ava7yJnzMw8/0.jpg)](https://www.youtube.com/watch?v=Ava7yJnzMw8)

