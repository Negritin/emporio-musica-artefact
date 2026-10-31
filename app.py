"""Chat local. O histórico vive somente na sessão do navegador."""

import streamlit as st

from emporio.agent import Agent
from emporio.config import Settings
from emporio.models import Turn

st.set_page_config(page_title="Empório da Música", page_icon="🎶", layout="centered")
st.markdown(
    """<style>
h1 {font-family: Georgia, serif; letter-spacing: -.04em; font-weight: 500;}
[data-testid="stChatMessage"] {border-radius: 12px;}
.stCaption {line-height: 1.6;}
</style>""",
    unsafe_allow_html=True,
)
st.caption("CAMPO GRANDE · INSTRUMENTOS MUSICAIS")
st.title("Sua música começa aqui.")
st.write("Encontre um instrumento ou tire suas dúvidas sobre as políticas da loja.")
st.caption(
    "Protótipo local com o catálogo fornecido no desafio. Consultas individuais de "
    "clientes e pedidos exigem autenticação e não estão disponíveis nesta versão."
)

settings = Settings.load()
try:
    settings.validate()
except ValueError as exc:
    st.error(str(exc))
    st.info("Prepare o ambiente seguindo o README e execute `emporio prepare` antes do chat.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.turns = []

with st.sidebar:
    st.header("Atendimento")
    st.write("Posso ajudar com catálogo, pagamentos, entregas e trocas.")
    st.caption(
        "Exemplos: “Violões até R$ 1.000”, “Qual o endereço?” ou “Posso devolver "
        "uma compra online?”."
    )
    if st.button("Começar nova conversa", width="stretch"):
        st.session_state.history = []
        st.session_state.turns = []
        st.rerun()
    known = [t.known_cost_usd for t in st.session_state.turns if t.known_cost_usd is not None]
    st.caption(f"Conversas nesta sessão: {len(st.session_state.turns)} turnos")
    st.caption(f"Custo informado: US$ {sum(known):.6f}" if known else "Custo não informado")
    st.caption(
        "Somatório dos valores recebidos do provedor. Pode ser parcial quando "
        "alguma chamada não informa o custo. O histórico é descartado ao iniciar "
        "nova conversa ou encerrar a sessão."
    )


def details(turn: Turn):
    with st.expander("Como cheguei à resposta"):
        st.write(" → ".join(e.name for e in turn.events))
        st.dataframe(
            [
                {
                    "Etapa": e.name,
                    "Estado": e.status,
                    "Duração (ms)": e.duration_ms,
                    "Modelo": e.model or "—",
                    "Tokens de entrada": e.input_tokens,
                    "Tokens de saída": e.output_tokens,
                    "Custo informado (USD)": e.cost_usd,
                }
                for e in turn.events
            ],
            hide_index=True,
            width="stretch",
        )
        if turn.sources:
            pages = sorted({s["page"] for s in turn.sources})
            st.caption(
                "Fontes recuperadas: políticas_da_loja.pdf, páginas "
                + ", ".join(map(str, pages))
                + "."
            )
            for source in turn.sources:
                st.markdown(f"**Página {source['page']} · {source['section']}**")
                st.write(source["content"])
        st.caption("Exibo somente etapas executadas. Valores ausentes não foram informados.")


for turn in st.session_state.turns:
    with st.chat_message("user"):
        st.write(turn.question)
    with st.chat_message("assistant"):
        st.markdown(turn.answer)
        details(turn)

limit = len(st.session_state.turns) >= settings.max_session_turns
if limit:
    st.info("Esta sessão atingiu o limite de turnos. Você pode começar uma nova conversa.")
question = st.chat_input("Como posso ajudar?", max_chars=settings.max_message_chars, disabled=limit)
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Consultando as informações da loja…"):
            try:
                turn = Agent(settings).ask(question, st.session_state.history)
            except Exception:
                st.error("Não consegui iniciar o atendimento. Confira a configuração no README.")
                st.stop()
        st.markdown(turn.answer)
        details(turn)
    st.session_state.turns.append(turn)
    if turn.success:
        st.session_state.history.extend(
            [{"role": "user", "content": question}, {"role": "assistant", "content": turn.answer}]
        )
    st.rerun()
