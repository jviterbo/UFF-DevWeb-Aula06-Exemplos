# Lista de Recados — Exemplo da Aula 06 (Flask + Jinja2 + Flask-WTF)

Aplicação web de exemplo utilizada na **Aula 06** da disciplina **Introdução ao Desenvolvimento Web**: **Templates Dinâmicos com Jinja2 & Herança de Layout** (no Instituto de Computação – UFF).

Ela reúne, em um único projeto pequeno e executável, os conceitos vistos em aula:

- renderização de páginas com **templates Jinja2** (`{{ }}`, `{% for %}`, `{% if %}`);
- **herança de templates** (`{% extends %}` e `{% block %}`) com um layout base em **Bootstrap 5**;
- **formulários com Flask-WTF** (classe `FlaskForm`, validadores, proteção CSRF);
- o padrão **Post-Redirect-Get (PRG)** e o uso de `redirect()`, `url_for()` e `request.args`, vistos na Aula 05.

> Os dados ficam **apenas em memória** (uma lista Python). Ao reiniciar o servidor, a lista volta ao estado inicial. Na Aula 07, essa lista será substituída por um banco de dados SQLite com Flask-SQLAlchemy.

---

## Sumário

1. [O que a aplicação faz](#1-o-que-a-aplicação-faz)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Como executar](#3-como-executar)
4. [Estrutura do projeto](#4-estrutura-do-projeto)
5. [Mapa de rotas](#5-mapa-de-rotas)
6. [Onde cada conceito da aula aparece no código](#6-onde-cada-conceito-da-aula-aparece-no-código)
7. [Roteiro para explorar a aplicação](#7-roteiro-para-explorar-a-aplicação)
8. [Pontos de atenção (limitações didáticas)](#8-pontos-de-atenção-limitações-didáticas)
9. [Problemas comuns](#10-problemas-comuns)
10. [Tecnologias e versões](#11-tecnologias-e-versões)
11. [Referências](#12-referências)
12. [Licença](#13-licença)

---

## 1. O que a aplicação faz

A **Lista de Recados** é uma lista de tarefas simples. Cada recado tem um **título**, uma **descrição** e um **estado** (pendente ou concluído).

| Tela | O que o usuário faz |
|------|---------------------|
| **Página inicial** (`/`) | Vê todos os recados. Recados concluídos aparecem em verde, com os botões *concluído* e *remover*; os pendentes têm o botão *detalhes*. |
| **Novo recado** (`/novo`) | Preenche título e descrição em um formulário validado. Em caso de erro, as mensagens aparecem sob cada campo. |
| **Detalhes** (`/recado?id=N`) | Lê a descrição e, se o recado estiver pendente, pode marcá-lo como concluído, removê-lo ou voltar à lista. |

Todas as páginas compartilham a mesma barra de navegação e o mesmo CSS, definidos uma única vez no `base.html`.

---

## 2. Pré-requisitos

- **Python 3.11 ou superior** (o projeto foi desenvolvido e testado com Python 3.12).
- **pip** (já vem com o Python).
- Um navegador moderno.
- **Conexão com a internet** na primeira visualização de cada sessão: o Bootstrap é carregado via CDN (`cdn.jsdelivr.net`). Sem internet, a aplicação funciona, mas sem a estilização.
- *(Opcional)* **Git**, para clonar o repositório.

Para conferir sua versão do Python:

```bash
python --version
```

> No Windows, se `python` não for reconhecido, tente `py --version`. No Linux/macOS, pode ser necessário usar `python3`.

---

## 3. Como executar

### 3.1 Obter o código

Com Git:

```bash
git clone https://github.com/jviterbo/UFF-DevWeb-Aula06-Exemplos.git
cd UFF-DevWeb-Aula06-Exemplos
```

Ou baixe o ZIP pelo botão **Code → Download ZIP** na página do repositório, extraia e abra a pasta no terminal.

### 3.2 Criar e ativar o ambiente virtual

O ambiente virtual (`venv`) isola as dependências deste projeto das demais instaladas no seu computador (veja a Aula 05).

**Windows (Prompt de Comando ou PowerShell):**

```bat
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Quando o ambiente estiver ativo, o terminal mostra `(venv)` no início da linha.

### 3.3 Instalar as dependências

```bash
pip install -r requirements.txt
```

Isso instala o Flask, o Jinja2 (que vem junto com o Flask) e o Flask-WTF, entre outras bibliotecas auxiliares.

### 3.4 Iniciar o servidor

```bash
python app.py
```

ou, alternativamente:

```bash
flask run --debug
```

Em seguida, abra no navegador: **http://127.0.0.1:5000**

Para encerrar o servidor, pressione `Ctrl + C` no terminal.

> O modo debug (`debug=True`) reinicia o servidor automaticamente a cada alteração nos arquivos e exibe erros detalhados no navegador. É ótimo para estudar, mas **nunca deve ser usado em produção**.

---

## 4. Estrutura do projeto

```text
UFF-DevWeb-Aula06-Exemplos/
├── app.py               # Aplicação Flask: configuração, dados em memória e rotas
├── forms.py             # Classe RecadoForm (Flask-WTF)
├── requirements.txt     # Dependências do projeto
├── static/              # Arquivos estáticos (CSS, imagens, JS) — vazia neste exemplo
└── templates/
    ├── base.html        # Layout-mestre: <head>, Bootstrap e navbar
    ├── index.html       # Lista de recados (estende base.html)
    ├── novo.html        # Formulário de novo recado (estende base.html)
    └── recado.html      # Detalhes de um recado (estende base.html)
```

| Arquivo | Responsabilidade |
|---------|------------------|
| `app.py` | Cria a aplicação, define a `SECRET_KEY`, guarda a lista `recados` e declara as 5 rotas. |
| `forms.py` | Descreve o formulário de cadastro como uma classe Python, com seus campos e validadores. |
| `templates/base.html` | Estrutura HTML comum a todas as páginas. Define os blocos `titulo` e `conteudo`. |
| `templates/index.html` | Percorre a lista com `{% for %}` e decide o que exibir com `{% if %}`. |
| `templates/novo.html` | Renderiza o formulário Flask-WTF, incluindo o token CSRF e as mensagens de erro. |
| `templates/recado.html` | Exibe um único recado e os botões de ação, conforme o seu estado. |

---

## 5. Mapa de rotas

| URL | Métodos | Função (`app.py`) | Template | O que faz |
|-----|---------|-------------------|----------|-----------|
| `/` | `GET` | `index()` | `index.html` | Lista todos os recados. |
| `/novo` | `GET`, `POST` | `novo_recado()` | `novo.html` | **GET:** exibe o formulário vazio. **POST:** valida; se estiver correto, adiciona o recado e redireciona para `/`; senão, reexibe o formulário com os erros. |
| `/recado?id=N` | `GET` | `recado()` | `recado.html` | Exibe os detalhes do recado de número `N`. |
| `/conclui?id=N` | `GET` | `conclui_recado()` | — | Marca o recado `N` como concluído e redireciona para `/`. |
| `/remove?id=N` | `GET` | `remove_recado()` | — | Remove o recado `N`, renumera os demais e redireciona para `/`. |

O parâmetro `id` é enviado pela **query string** e lido com `request.args.get("id")` (visto na Aula 05).

### Modelo de dados

Cada recado é um dicionário Python dentro da lista `recados`:

```python
{
    "id": "1",                       # posição na lista (texto), começando em 1
    "texto": "Revisar o Capítulo 3", # título — obrigatório, até 80 caracteres
    "descr": "Reler o capítulo...",  # descrição — obrigatória, até 280 caracteres
    "concluido": False,              # estado do recado
}
```

---

## 6. Onde cada conceito da aula aparece no código

### 6.1 Passagem de variáveis (`{{ }}`)

A view envia variáveis com argumentos nomeados, e o template as exibe:

```python
# app.py
return render_template("index.html", recados=recados, titulo="Meus Recados")
```

```html
<!-- templates/index.html -->
<h1>{{ titulo }}</h1>
```

Em `recado.html`, o dicionário inteiro é enviado e acessamos seus campos com ponto: `{{ recado.texto }}` e `{{ recado.descr }}`.

### 6.2 Repetição e condição (`{% for %}` e `{% if %}`)

Em `templates/index.html`, o laço gera um `<li>` por recado, e o `if` muda a aparência e os botões conforme o estado:

```html
{% for recado in recados %}
  <li class="list-group-item {% if recado.concluido %}list-group-item-success{% endif %}">
    {% if recado.concluido %}
      ... badges "concluído" e "remover" ...
    {% else %}
      ... badge "detalhes" ...
    {% endif %}
  </li>
{% endfor %}

{% if not recados %}
  <p>Nenhum recado cadastrado ainda.</p>
{% endif %}
```

### 6.3 Herança de templates (`{% extends %}` e `{% block %}`)

O `base.html` define a estrutura comum e dois blocos:

```html
<title>{% block titulo %}Meus Recados{% endblock %}</title>
...
<div class="container mt-4">
  {% block conteudo %}{% endblock %}
</div>
```

As demais páginas começam com `{% extends "base.html" %}` e preenchem apenas os blocos. Alterar a navbar em `base.html` muda **todas** as páginas de uma só vez.

### 6.4 Formulários com Flask-WTF

| Etapa | Onde | Trecho |
|-------|------|--------|
| Configuração | `app.py` | `app.config["SECRET_KEY"] = "..."` |
| Classe do formulário | `forms.py` | `class RecadoForm(FlaskForm)` com `StringField`, `SubmitField` e os validadores `DataRequired()` e `Length(max=...)` |
| Renderização no HTML | `novo.html` | `{{ form.hidden_tag() }}`, `{{ form.texto(class="form-control") }}`, `{{ form.texto.label(...) }}` |
| Mensagens de erro | `novo.html` | `{% for erro in form.texto.errors %}` |
| Tratamento na view | `app.py` | `form = RecadoForm()` e `if form.validate_on_submit():` |

`form.hidden_tag()` insere o **token CSRF**. Sem ele, a validação sempre falha, mesmo com os campos preenchidos corretamente.

### 6.5 Padrão PRG, `redirect()` e `url_for()`

Depois de um POST bem-sucedido, a view **não** devolve uma página: ela redireciona para a lista. Assim, atualizar a página (F5) não reenvia o formulário.

```python
if form.validate_on_submit():
    recados.append({...})
    return redirect(url_for("index"))   # POST -> Redirect -> GET
return render_template("novo.html", form=form)
```

O `url_for()` também é usado nos templates para gerar links, como `{{ url_for('novo_recado') }}`, sem escrever a URL manualmente.

---

## 7. Roteiro para explorar a aplicação

Experimente, nesta ordem, observando o que acontece na tela **e** no terminal onde o servidor está rodando:

1. Abra `http://127.0.0.1:5000` e veja os três recados iniciais. Qual deles aparece em verde? Por quê?
2. Clique em **detalhes** em um recado pendente e leia a descrição.
3. Clique em **Marcar como concluído**. Você volta à lista e o recado agora está em verde.
4. Clique em **Novo recado** e envie o formulário **em branco**. Quais mensagens de erro aparecem?
5. Preencha o formulário corretamente e envie. Em seguida, **atualize a página (F5)**. O recado foi cadastrado duas vezes? Por que não? (Dica: padrão PRG.)
6. Clique em **remover** em um recado concluído e observe o terminal: qual requisição foi feita?
7. Abra o código-fonte da página no navegador (`Ctrl + U`) na tela de novo recado e encontre o campo oculto `csrf_token`.
8. Pare o servidor (`Ctrl + C`), inicie-o novamente e veja que os recados voltaram ao estado inicial.
9. No `base.html`, altere o texto da navbar e atualize as três telas: a mudança aparece em todas.

---

## 8. Pontos de atenção (limitações didáticas)

Este exemplo foi escrito para ser **simples**, e por isso tem limitações propositais. Algumas dessas limitações serão tratadas nas próximas aulas:

- **Dados em memória.** A lista `recados` é uma variável global compartilhada por todos os usuários e é perdida ao reiniciar o servidor (relembre as *variáveis de aplicação* da Aula 05). A persistência real vem na **Aula 07**, com SQLite.
- **Alterações de estado via `GET`.** As rotas `/conclui` e `/remove` modificam dados, mas respondem a `GET`. Na prática, ações que alteram dados devem usar `POST`, pois um simples link (ou um robô de busca) poderia disparar a remoção.
- **Identificador por posição.** O `id` é a posição do recado na lista, e é renumerado a cada remoção. Um link antigo pode passar a apontar para outro recado. Um banco de dados resolve isso com chaves primárias estáveis.
- **Sem validação do parâmetro `id`.** Acessar `/recado` (sem `id`) ou `/recado?id=99` causa erro `500` (`TypeError` / `IndexError`). Um tratamento adequado devolveria um erro `404`.
- **Chave secreta no código.** O valor de `SECRET_KEY` está escrito no `app.py` por simplicidade. Em um projeto real, ele deve vir de uma variável de ambiente e **nunca** ser publicado em um repositório.
- **Modo debug ligado.** Adequado apenas para desenvolvimento.
- **Sem confirmação ao remover.** Um clique em *remover* apaga o recado imediatamente.

---

## 9. Problemas de execução comuns

| Sintoma | Causa provável e solução |
|---------|--------------------------|
| `ModuleNotFoundError: No module named 'flask'` | O ambiente virtual não está ativo, ou as dependências não foram instaladas. Ative o `venv` e rode `pip install -r requirements.txt`. |
| `ModuleNotFoundError: No module named 'flask_wtf'` | Mesmo caso acima: rode `pip install -r requirements.txt` com o `venv` ativo. |
| PowerShell: *"a execução de scripts foi desabilitada neste sistema"* ao ativar o `venv` | Execute `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ou use o Prompt de Comando (`cmd`). |
| `Address already in use` / porta 5000 ocupada | Outro programa (ou outra cópia do servidor) está usando a porta. Encerre-o ou rode `flask run --debug --port 5001`. |
| Página sem estilo (sem cores, botões simples) | O Bootstrap não foi carregado. Verifique a conexão com a internet (o CSS vem do CDN). |
| O formulário "não faz nada" ao enviar | Verifique se `{{ form.hidden_tag() }}` está dentro da `<form>` e se a `SECRET_KEY` está definida. |
| Erro `500` em `/recado` | Falta o parâmetro `id` ou ele não existe na lista (veja a [seção 8](#8-pontos-de-atenção-limitações-didáticas)). Use os links da própria aplicação. |
| Alterei o código e nada mudou | Sem o modo debug, é preciso reiniciar o servidor. Use `python app.py` (que liga o debug) ou `flask run --debug`. |

---

## 10. Tecnologias e versões

| Tecnologia | Versão | Papel |
|------------|--------|-------|
| Python | 3.11+ (testado com 3.12) | Linguagem |
| Flask | 3.1.3 | Micro-framework web |
| Jinja2 | 3.1.6 | Motor de templates (instalado junto com o Flask) |
| Flask-WTF | ≥ 1.2 | Formulários, validação e proteção CSRF |
| Werkzeug, Click, Blinker, ItsDangerous, MarkupSafe | conforme `requirements.txt` | Dependências do Flask |
| Bootstrap | 5.3.3 (via CDN) | Estilização e layout responsivo |

---

## 11. Referências

- [Documentação do Flask](https://flask.palletsprojects.com/)
- [Documentação do Jinja2 — Template Designer](https://jinja.palletsprojects.com/en/stable/templates/)
- [Documentação do Flask-WTF](https://flask-wtf.readthedocs.io/)
- [Documentação do WTForms](https://wtforms.readthedocs.io/)
- [Bootstrap 5.3 — Documentação](https://getbootstrap.com/docs/5.3/)
- GRINBERG, Miguel. *Desenvolvimento Web com Flask: Criando Aplicações Web com Python*. 2. ed. São Paulo: Novatec, 2018.

---

## 12. Licença

Este projeto é distribuído sob a licença **GNU GPL v3.0**. Consulte o arquivo [`LICENSE`](LICENSE) para os detalhes.
