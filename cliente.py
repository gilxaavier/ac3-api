
from flask import Flask, jsonify, request
import mysql.connector
app = Flask (__name__)

# Conectar ao banco de dados
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="*******",
  database="ac3"
)

# Criar tabela de desenvolvedores
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS desenvolvedores (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), habilidades VARCHAR(255))")

@app.route("/dev/<int:id>/", methods=["GET"])
def getDeveloperById(id):
    # Buscar o desenvolvedor com o ID informado no banco de dados
    mycursor.execute("SELECT * FROM desenvolvedores WHERE id = %s", (id,))
    desenvolvedor = mycursor.fetchone()

    if desenvolvedor is not None:
        # Transformar o resultado em um dicionário
        d = {"id": desenvolvedor[0], "nome": desenvolvedor[1], "habilidades": desenvolvedor[2].split(",")}
        return jsonify(d)
    else:
        return jsonify({"mensagem": f"Desenvolvedor com ID {id} não encontrado."}), 404


@app.route("/dev/", methods=["POST"])
def addDeveloper():
    # Adicionar novo desenvolvedor ao banco de dados
    dados = request.get_json()
    nome = dados["nome"]
    habilidades = ",".join(dados["habilidades"])
    sql = "INSERT INTO desenvolvedores (nome, habilidades) VALUES (%s, %s)"
    val = (nome, habilidades)
    mycursor.execute(sql, val)
    mydb.commit()

    # Retornar dados do desenvolvedor cadastrado
    id = mycursor.lastrowid
    novo_desenvolvedor = {"id": id, "nome": nome, "habilidades": dados["habilidades"]}
    return jsonify(novo_desenvolvedor)

@app.route("/dev/excluir/<int:id>", methods=["DELETE"])
def delete_developer(id):
    # Deletar desenvolvedor com o id especificado do banco de dados
    mycursor.execute("DELETE FROM desenvolvedores WHERE id = %s", (id,))
    mydb.commit()

    # Verificar se algum registro foi afetado pela operação
    if mycursor.rowcount == 0:
        return jsonify({"status": "erro", "mensagem": "Desenvolvedor não encontrado"}), 404

    return jsonify({"status": "sucesso", "mensagem": "Desenvolvedor excluído com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)