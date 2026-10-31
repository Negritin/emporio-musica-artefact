"""Preservo conflitos conhecidos do manual antes de redigir uma resposta livre."""

import re

from emporio.store import normalize


def ambiguity_reply(question: str, sources: list[dict]) -> str | None:
    q = normalize(question)
    text = " ".join(s["content"] for s in sources)
    pages = {s["page"] for s in sources}
    if (
        re.search(r"whats|telefone|contato", q)
        and {2, 6} <= pages
        and "3341" in text
        and "3321" in text
    ):
        return (
            "Encontrei dois contatos diferentes no manual: a página 2 apresenta "
            "(67) 3341-4444 como telefone/WhatsApp, e a página 6 apresenta "
            "(67) 3321-4500 como canal principal de WhatsApp. Não consigo confirmar "
            "qual deve prevalecer; recomendo confirmar com a loja. [Manual, p. 2 e 6]"
        )
    if (
        "frete" in q
        and re.search(r"\b500(?:[,.]00)?\b", q)
        and "exat" in q
        and 4 in pages
        and "acima" in text
        and "abaixo" in text
    ):
        return (
            "Para a região metropolitana de Campo Grande, o manual prevê frete grátis "
            "acima de R$ 500,00 e taxa de R$ 35,00 abaixo desse valor. Não informa a "
            "condição para exatamente R$ 500,00. Por isso, não consigo confirmar frete "
            "grátis nesse limite; é preciso confirmar com a loja. [Manual, p. 4]"
        )
    if (
        re.search(r"parcel|\bvezes\b|\b[4-6]x\b", q)
        and 3 in pages
        and "80,00" in text
        and "100,00" in text
    ):
        return (
            "O manual apresenta uma diferença nas condições: a tabela geral informa "
            "parcelamento em até 12x sem juros com parcela mínima de R$ 100,00. A seção "
            "3.1 especifica até 3x sem valor mínimo (com ressalva abaixo de R$ 50), "
            "de 4x a 6x com mínimo de R$ 80,00 e de 7x a 12x com mínimo de R$ 100,00. "
            "Para confirmar qual condição se aplica à sua compra, consulte a loja; "
            "não vou escolher uma interpretação sem essa confirmação. [Manual, p. 3]"
        )
    if re.search(r"garantia|defeito", q) and {4, 7} <= pages and "30" in text and "90" in text:
        return (
            "O manual traz duas referências: a seção 4.2 prevê troca por defeito em até "
            "30 dias corridos após a compra e, depois, acionamento do fabricante, com "
            "possibilidade de intermediação da loja. Já a seção 8.1 descreve garantia "
            "legal de 90 dias a partir do recebimento. São contagens e procedimentos "
            "diferentes; não concluo que a garantia legal acabou aos 30 dias. Confirme "
            "com a loja como aplicar as duas regras ao caso, informando as datas de "
            "compra e recebimento. [Manual, p. 4 e 7]"
        )
    if re.search(r"devol|arrepend", q) and 4 in pages and "7 (sete) dias" in text:
        return (
            "Para compras online, você pode solicitar devolução por arrependimento em até "
            "7 dias corridos após receber o produto. O manual pede embalagem original, "
            "ausência de sinais de uso e todos os acessórios e manuais. Confira se todos "
            "esses itens estão presentes antes de solicitar. O reembolso ocorre na mesma "
            "forma de pagamento em até 10 dias úteis, e o frete de devolução fica por conta "
            "da loja. Entre em contato com o atendimento para iniciar o procedimento; "
            "não abro solicitações ou faço estornos nesta demonstração. [Manual, p. 4]"
        )
    if re.search(r"\bcabos?\b|\bpalhetas?\b|\bpedais\b|\bamplificadores?\b", q) and 6 in pages:
        return (
            "A Empório da Música trabalha com instrumentos musicais e não comercializa "
            "acessórios como cabos, palhetas, pedais e amplificadores. Posso ajudar a "
            "encontrar um instrumento no catálogo. [Manual, p. 6]"
        )
    return None
