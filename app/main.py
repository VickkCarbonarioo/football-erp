from fastapi import FastAPI


# Cria a aplicação principal do Football ERP.
# A partir deste objeto vamos registrar nossas rotas,
# configurações e funcionalidades da API.
app = FastAPI(
    title="Football ERP",
    description="Sistema ERP para gestão estratégica de clubes de futebol.",
    version="0.1.0"
)


# Rota inicial da API.
# Quando alguém acessar "/", o sistema executará esta função.
@app.get("/")
def home():
    return {
        "message": "Football ERP está funcionando!",
        "version": "0.1.0"
    }