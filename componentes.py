from fasthtml.common import Div, H1, P, Form, Input, Button, Ul, Li, A

def reg_livro():
    formulario = Form(
        Input(type="text", name="tarefa", placeholder="Insira a tarefa a ser adicionada"),
        Button("Enviar"),
        method="post",
        action="/registrar_livro",
        hx_post="/registrar_livro",
        hx_target="registrar-livro",
        hx_swap="outerHTML"
    )
    return formulario