from flask import Flask, jsonify, request
import mysql.connector
app = Flask (__name__)

# Conectar ao banco de dados
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="ac3"
)

# Criar tabela de desenvolvedores
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS desenvolvedores (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), habilidades VARCHAR(255))")
mycursor.execute("USE ac3")

@app.route("/dev/", methods=["GET"])

#Retorna todos os desenvolvedores
def getAllDev():
    mycursor.execute("SELECT * FROM desenvolvedores")
    desenvolvedores = mycursor.fetchall()
    result = []
    for desenvolvedor in desenvolvedores:
        dev = {"id": desenvolvedor[0], "nome": desenvolvedor[1], "habilidades": desenvolvedor[2].split(",")}
        result.append(dev)
    return jsonify(result)

#Retona desenvolvedor pelo id da busca
@app.route("/dev/<int:id>", methods=["GET"])
def getDeveloperById(id):
    # Buscar o desenvolvedor com o ID informado no banco de dados
    mycursor.execute(f"SELECT * FROM desenvolvedores WHERE id ={id}")
    desenvolvedor = mycursor.fetchone()

    if desenvolvedor is not None:
        # Transformar o resultado em um dicionário
        dev = {"id": desenvolvedor[0], "nome": desenvolvedor[1], "habilidades": desenvolvedor[2].split(",")}
        return jsonify(dev)
    else:
        return jsonify({"mensagem": f"Desenvolvedor com ID {id} nao encontrado."}), 404


@app.route("/cadastro/", methods=["POST"]) 
def addDev(): 
    # Adicionar novo desenvolvedor ao banco de dados 
    nome = request.form.get('nome')
    habilidades = request.form.getlist('habilidades')
    habilidades_str = ",".join(habilidades)
    sql = "INSERT INTO desenvolvedores (nome, habilidades) VALUES (%s, %s)"
    val = (nome, habilidades_str)
    mycursor.execute(sql, val) 
    mydb.commit()
    return "Desenvolvedor adicionado com sucesso!"

@app.route("/dev/<int:id>", methods=["DELETE"])
def deleteDev(id):
    # Deletar desenvolvedor com o id especificado do banco de dados
    mycursor.execute(f"DELETE FROM desenvolvedores WHERE id = {id}")
    mydb.commit()

    # Verificar se algum registro foi afetado pela operação
    if mycursor.rowcount == 0:
        return jsonify({"status": "erro", "mensagem": "Desenvolvedor nao encontrado"}), 404

    return jsonify({"status": "sucesso", "mensagem": "Desenvolvedor excluído com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)