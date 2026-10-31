"""Grafo curto: validar, interpretar, consultar evidências e responder."""

import re
import time
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from emporio.config import Settings
from emporio.models import Event, Plan, Turn
from emporio.provider import Embeddings, OpenRouterModel
from emporio.store import Store

PRIVATE_REQUEST = re.compile(
    r"\b(?:meu|minha)\s+(?:pedido|cadastro|rastreamento)|"
    r"\b(?:pedido|cliente)\s*(?:n[ºo°.]?\s*)?[#:]?\s*\d+|"
    r"\b(?:cpf|telefones?|e-?mails?|endereços?)\s+(?:dos?|das?)\s+clientes?",
    re.IGNORECASE,
)
CREDENTIAL_REQUEST = re.compile(
    r"(?:senha|chave|token).{0,50}(?:postgres|openrouter|api|banco)|"
    r"(?:postgres|openrouter|api|banco).{0,50}(?:senha|chave|token)",
    re.IGNORECASE,
)
POLICY_TERMS = re.compile(r"\bpix\b|parcel|\bvezes\b|promoç|desconto|\bfrete\b", re.IGNORECASE)
PRIVATE_REPLY = (
    "Para proteger os dados do cliente, não consulto cadastros, status nem rastreamento "
    "de pedidos sem autenticação e autorização. Esta demonstração não tem essa etapa. "
    "Procure o atendimento da loja; posso explicar as políticas gerais de entrega, "
    "troca e devolução por aqui."
)


class State(TypedDict, total=False):
    question: str
    history: list[dict]
    plan: Plan
    events: list[Event]
    products: list[dict]
    sources: list[dict]
    answer: str
    success: bool


class Agent:
    def __init__(self, settings: Settings, *, model=None, store=None, embeddings=None):
        self.settings = settings
        self.model = model or OpenRouterModel(settings)
        self.store = store or Store(settings)
        self.embeddings = embeddings or Embeddings(settings)
        graph = StateGraph(State)
        for name, action in (
            ("validar", self.guard),
            ("interpretar", self.interpret),
            ("catalogo", self.catalog),
            ("politicas", self.policies),
            ("responder", self.respond),
        ):
            graph.add_node(name, action)
        graph.add_edge(START, "validar")
        graph.add_conditional_edges("validar", lambda s: END if s.get("answer") else "interpretar")
        graph.add_conditional_edges("interpretar", self.after_plan)
        graph.add_conditional_edges(
            "catalogo",
            lambda s: (
                END
                if not s["success"]
                else ("politicas" if s["plan"].route == "hybrid" else "responder")
            ),
        )
        graph.add_conditional_edges("politicas", lambda s: "responder" if s["success"] else END)
        graph.add_edge("responder", END)
        self.graph = graph.compile()

    def ask(self, question: str, history: list[dict] | None = None) -> Turn:
        recent = (history or [])[-self.settings.history_turns * 2 :]
        recent = [
            {"role": h["role"], "content": str(h["content"])[:2000]}
            for h in recent
            if h.get("role") in ("user", "assistant")
        ]
        state = self.graph.invoke(
            {
                "question": question.strip(),
                "history": recent,
                "events": [],
                "products": [],
                "sources": [],
                "success": True,
            },
            {"recursion_limit": 12},
        )
        return Turn(
            question=question,
            answer=state["answer"],
            events=state["events"],
            sources=state["sources"],
            products=state["products"],
            success=state["success"],
            route=state["plan"].route if "plan" in state else "guard",
        )

    def guard(self, state: State) -> dict:
        start = time.perf_counter()
        question = state["question"]
        reply, status = "", "ok"
        if not question or len(question) > self.settings.max_message_chars:
            reply = f"Envie uma pergunta com até {self.settings.max_message_chars} caracteres."
            status = "bloqueado"
        elif CREDENTIAL_REQUEST.search(question):
            reply = (
                "Não compartilho credenciais ou detalhes de acesso aos serviços. "
                "Posso ajudar com instrumentos e políticas da loja."
            )
            status = "bloqueado"
        elif PRIVATE_REQUEST.search(question):
            reply, status = PRIVATE_REPLY, "bloqueado"
        event = Event(
            name="validar",
            status=status,
            duration_ms=round((time.perf_counter() - start) * 1000, 2),
        )
        return {"events": [event], **({"answer": reply} if reply else {})}

    def interpret(self, state: State) -> dict:
        start = time.perf_counter()
        try:
            plan, event = self.model.plan(state["question"], state["history"])
            if plan.route == "catalog" and POLICY_TERMS.search(state["question"]):
                plan = plan.model_copy(
                    update={"route": "hybrid", "policy_query": state["question"]}
                )
            return {"plan": plan, "events": state["events"] + [event]}
        except Exception:
            return self.failure(state, "interpretar", start)

    @staticmethod
    def after_plan(state: State):
        if not state["success"]:
            return END
        route = state["plan"].route
        return (
            "catalogo"
            if route in ("catalog", "hybrid")
            else ("politicas" if route == "policies" else "responder")
        )

    def catalog(self, state: State) -> dict:
        start = time.perf_counter()
        try:
            products = self.store.products(state["plan"])
            event = Event(
                name="catalogo", duration_ms=round((time.perf_counter() - start) * 1000, 2)
            )
            return {"products": products, "events": state["events"] + [event]}
        except Exception:
            return self.failure(state, "catalogo", start)

    def policies(self, state: State) -> dict:
        start = time.perf_counter()
        events = list(state["events"])
        try:
            query = state["plan"].policy_query or state["question"]
            vectors, embedding_event = self.embeddings.embed([query])
            events.append(embedding_event)
            search_start = time.perf_counter()
            sources = self.store.policies(vectors[0], query)
            event = Event(
                name="politicas", duration_ms=round((time.perf_counter() - search_start) * 1000, 2)
            )
            return {"sources": sources, "events": events + [event]}
        except Exception:
            return self.failure({**state, "events": events}, "politicas", start)

    def respond(self, state: State) -> dict:
        start = time.perf_counter()
        route = state["plan"].route
        if route in ("private", "outside", "clarify"):
            answer = {
                "private": PRIVATE_REPLY,
                "outside": "Posso ajudar com instrumentos, produtos e políticas da Empório da "
                "Música. Sobre qual desses assuntos você quer conversar?",
                "clarify": state["plan"].clarification
                or "Oi! Como posso ajudar? Você procura um instrumento ou tem uma "
                "dúvida sobre as políticas da loja?",
            }[route]
            event = Event(
                name="responder", duration_ms=round((time.perf_counter() - start) * 1000, 2)
            )
            return {"answer": answer, "events": state["events"] + [event]}
        try:
            answer, event = self.model.answer(
                {
                    "question": state["question"],
                    "history": state["history"],
                    "products": state["products"],
                    "policy_sources": state["sources"],
                    "route": route,
                }
            )
            return {"answer": answer, "events": state["events"] + [event]}
        except Exception:
            return self.failure(state, "responder", start)

    @staticmethod
    def failure(state: State, name: str, start: float) -> dict:
        # Mensagens do banco/provedor podem conter detalhes operacionais: não as exponho.
        event = Event(
            name=name,
            status="erro",
            error="serviço_indisponível",
            duration_ms=round((time.perf_counter() - start) * 1000, 2),
        )
        return {
            "success": False,
            "answer": "Não consegui consultar as informações agora. "
            "Tente novamente em instantes; não vou confirmar valores ou regras sem verificar.",
            "events": state["events"] + [event],
        }
