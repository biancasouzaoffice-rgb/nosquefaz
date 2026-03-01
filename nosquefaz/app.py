from flask import Flask, redirect, render_template, request
import urllib.parse

app = Flask(__name__)

WHATSAPP_NUMERO = "5537998122880"
LINK_ENTRADA = "/nosquefaz"

SABORES = [
    {"id": "carne_sol_creme_alho", "nome": "Carne de sol com creme de alho", "preco": 18.0},
    {"id": "carne_sol_requeijao", "nome": "Carne de sol com requeijão", "preco": 18.0},
    {"id": "fraldinha", "nome": "Fraldinha", "preco": 15.0},
    {"id": "lombo_abacaxi", "nome": "Lombo com abacaxi", "preco": 15.0},
    {"id": "frango_bacon", "nome": "Frango com bacon", "preco": 15.0},
    {"id": "frango_requeijao", "nome": "Frango com requeijão", "preco": 15.0},
]

TAXAS_ENTREGA = {
    "Centro": 10.0,
    "Bairro": 12.0,
    "Zona rural": 15.0,
}


def formato_brl(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_int_positivo(valor):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return 0
    return max(numero, 0)


def render_inicio(erro=""):
    return render_template("index.html", sabores=SABORES, taxas=TAXAS_ENTREGA, erro=erro)


def processar_pedido():
    nome = request.form.get("nome", "").strip()
    tipo = request.form.get("tipo", "").strip()
    data = request.form.get("data", "").strip()
    horario = request.form.get("horario", "").strip()
    pagamento = request.form.get("pagamento", "").strip()
    troco_para = request.form.get("troco_para", "").strip()
    bairro = request.form.get("bairro", "").strip()
    endereco = request.form.get("endereco", "").strip()
    observacao = request.form.get("observacao", "").strip()

    itens = []
    subtotal = 0.0

    for sabor in SABORES:
        qtd = parse_int_positivo(request.form.get(f"qtd_{sabor['id']}", "0"))
        if qtd == 0:
            continue

        valor_item = qtd * sabor["preco"]
        subtotal += valor_item
        itens.append(f"- {sabor['nome']} x{qtd} = R$ {formato_brl(valor_item)}")

    if not itens:
        return render_inicio("Selecione pelo menos 1 mini empadão.")

    if tipo not in {"Entrega", "Retirada"}:
        return render_inicio("Selecione entrega ou retirada.")

    if tipo == "Entrega" and not bairro:
        return render_inicio("Selecione o bairro para calcular a entrega.")

    if tipo == "Entrega" and not endereco:
        return render_inicio("Informe o endereço para entrega.")

    taxa_entrega = TAXAS_ENTREGA.get(bairro, 0.0) if tipo == "Entrega" else 0.0
    total_geral = subtotal + taxa_entrega

    mensagem = [
        "*Pedido - Nós que faz*",
        "",
        f"*Cliente:* {nome}",
        f"*Data:* {data}",
        f"*Horário:* {horario}",
        f"*Tipo:* {tipo}",
        f"*Pagamento:* {pagamento}",
    ]

    if pagamento.lower() == "dinheiro":
        mensagem.append(f"*Troco para:* R$ {troco_para or 'Não informado'}")

    if tipo == "Entrega":
        mensagem.append(f"*Bairro:* {bairro}")
        mensagem.append(f"*Endereço:* {endereco}")
        mensagem.append(f"*Taxa de entrega:* R$ {formato_brl(taxa_entrega)}")

    if observacao:
        mensagem.append(f"*Observação:* {observacao}")

    mensagem.extend(
        [
            "",
            "*Itens:*",
            *itens,
            "",
            f"*Subtotal:* R$ {formato_brl(subtotal)}",
            f"*Total final (itens + entrega):* R$ {formato_brl(total_geral)}",
        ]
    )

    texto = urllib.parse.quote("\n".join(mensagem))
    link = f"https://wa.me/{WHATSAPP_NUMERO}?text={texto}"
    return redirect(link)


@app.route("/", methods=["GET"])
def raiz():
    return redirect(LINK_ENTRADA)


@app.route("/nosquefaz", methods=["GET", "POST"])
@app.route("/entrada", methods=["GET", "POST"])
@app.route("/pedido", methods=["GET", "POST"])
def entrada():
    # Keep old routes working, but use /nosquefaz as the canonical entry link.
    if request.method == "GET" and request.path in {"/entrada", "/pedido"}:
        return redirect(LINK_ENTRADA)

    if request.method == "GET":
        return render_inicio()
    return processar_pedido()


if __name__ == "__main__":
    app.run(debug=True)
