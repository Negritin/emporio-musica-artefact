"""Comandos de preparação, consulta e conversa local."""

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from emporio.config import ROOT, Settings
from emporio.models import Turn


def show_turn(turn: Turn) -> None:
    console = Console()
    console.print(Markdown(turn.answer))
    table = Table("Etapa", "Estado", "ms", "Modelo", "Tokens entrada/saída", "USD informado")
    for e in turn.events:
        table.add_row(
            e.name,
            e.status,
            f"{e.duration_ms:.0f}",
            e.model or "—",
            f"{e.input_tokens}/{e.output_tokens}" if e.input_tokens is not None else "—",
            f"{e.cost_usd:.6f}" if e.cost_usd is not None else "não informado",
        )
    console.print(table)
    if turn.sources:
        pages = sorted({s["page"] for s in turn.sources})
        console.print(
            "Fontes recuperadas: políticas_da_loja.pdf, páginas", ", ".join(map(str, pages))
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Meu atendimento local — Empório da Música")
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare", help="Valido, carrego e indexo as fontes")
    prepare.add_argument("--data-dir", type=Path, default=ROOT / "Arquivos")
    ask = sub.add_parser("ask", help="Faço uma pergunta sem manter histórico")
    ask.add_argument("question")
    ask.add_argument("--json", action="store_true")
    sub.add_parser("chat", help="Converso no terminal; sair encerra a sessão")
    sub.add_parser("check", help="Verifico a leitura restrita e a indexação")
    args = parser.parse_args()
    try:
        settings = Settings.load(admin=args.command == "prepare")
        settings.validate()
        if args.command == "prepare":
            from emporio.ingest import index_policies, migrate_and_load, provision_reader

            report = migrate_and_load(settings, args.data_dir)
            report["rag"] = index_policies(settings, args.data_dir / "políticas_da_loja.pdf")
            provision_reader(settings)
            (ROOT / "docs").mkdir(exist_ok=True)
            (ROOT / "docs/dados-validacao.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2)
            )
            print("Preparei o schema, a carga e o manual. Relatório: docs/dados-validacao.json")
            return
        from emporio.store import Store

        store = Store(settings)
        if args.command == "check":
            with store.connection() as conn:
                counts = conn.execute("""
                    SELECT (SELECT count(*) FROM artefact.products) AS products,
                           (SELECT count(*) FROM artefact.policy_chunks) AS chunks
                """).fetchone()
                if counts["products"] == 0 or counts["chunks"] == 0:
                    raise ValueError("Execute emporio prepare antes de conversar.")
            print(json.dumps(counts))
            return
        from emporio.agent import Agent

        agent = Agent(settings)
        if args.command == "ask":
            result = agent.ask(args.question)
            print(result.model_dump_json(indent=2)) if args.json else show_turn(result)
            if not result.success:
                sys.exit(1)
            return
        history = []
        print("Empório da Música · catálogo fictício do desafio. Digite sair para encerrar.")
        for _ in range(settings.max_session_turns):
            question = input("Você: ").strip()
            if question.lower() in ("sair", "exit", "quit"):
                return
            turn = agent.ask(question, history)
            show_turn(turn)
            if turn.success:
                history.extend(
                    [
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": turn.answer},
                    ]
                )
        print("Encerrei esta sessão pelo limite de turnos configurado.")
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrei a conversa.")
    except Exception as exc:
        # Evito imprimir exceções de conexão que possam carregar detalhes sensíveis.
        print(
            f"Não consegui executar ({type(exc).__name__}). Confira a configuração no README.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
