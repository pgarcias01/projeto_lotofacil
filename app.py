from flask import Flask, jsonify
import os
from projeto_lotofacil.BuscaResultado import buscar_resultado

app = Flask(__name__)

@app.route('/<int:concurso>/')
def busca(concurso):
    return  jsonify(buscar_resultado(concurso))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)