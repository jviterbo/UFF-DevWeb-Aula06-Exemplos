from flask import Flask, render_template, redirect, url_for, request
from forms import RecadoForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave-secreta-aula06"  # necessária pelo Flask-WTF (proteção CSRF)

# "banco de dados" em memória, só para fins didáticos (Aula 07 troca isso por SQLite de verdade)
recados = [
    {"id":'1',
     "texto": "Revisar o Capítulo 3 de Flask", 
     "descr": "Reler o Capítulo 3 do livro Flask e fazer os exercícios.", 
     "concluido": True},
    {"id":'2',
     "texto": "Estudar slides da Aula 4", 
     "descr": "Estudar os slides da Aula 4, rodando os códigos disponíveis.", 
     "concluido": False},
    {"id":'3',
     "texto": "Fazer as atividades da Aula 5", 
     "descr": "Fazer e entregar todas as atividades propostas para a Aula 5.", 
     "concluido": True},
]


@app.route("/")
def index():
    return render_template("index.html", recados=recados, titulo="Meus Recados")


@app.route("/novo", methods=["GET", "POST"])
def novo_recado():
    form = RecadoForm()
    if form.validate_on_submit():
        id = len(recados)+1
        recados.append({"id": str(id), "texto": form.texto.data, "descr": form.descr.data, "concluido": False})
        return redirect(url_for("index"))
    return render_template("novo.html", form=form)

@app.route("/recado")
def recado():
    pos = int(request.args.get("id"))-1
    rec = recados[pos]
    return render_template("recado.html", recado=rec)

@app.route("/conclui")
def conclui_recado():
    pos = int(request.args.get("id"))-1
    recados[pos]["concluido"] = True
    return redirect(url_for("index"))

@app.route("/remove")
def remove_recado():
    pos = int(request.args.get("id"))-1
    recados.pop(pos)
    for i in range(len(recados)):
        recados[i]["id"] = str(i+1)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
