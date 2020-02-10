from flask import Flask, jsonify,request
import os
from BuscaResultado import buscar_resultado, max_concurso
from GerarCsv import  update_result

app = Flask(__name__)

@app.route('/<int:concurso>/')
def busca(concurso):
    return jsonify(buscar_resultado(concurso))

@app.route("/update")
def update():
    link = request.args.get('link')
    update_result(link)
    return "Update Successful"

@app.route("/maxconcurso")
def maxconcurso():
    return max_concurso()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

