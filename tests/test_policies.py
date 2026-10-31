from emporio.policies import ambiguity_reply


def test_exact_shipping_boundary_is_not_inferred():
    sources = [{"page": 4, "content": "Frete grátis acima de 500; abaixo taxa de 35."}]
    answer = ambiguity_reply("Frete para compra de exatamente R$500?", sources)
    assert "não informa" in answer.lower() and "não consigo confirmar" in answer
    assert ambiguity_reply("Frete para R$600?", sources) is None


def test_contact_conflict_needs_both_retrieved_pages():
    sources = [
        {"page": 2, "content": "Telefone WhatsApp 3341-4444"},
        {"page": 6, "content": "WhatsApp 3321-4500"},
    ]
    answer = ambiguity_reply("Qual é o WhatsApp?", sources)
    assert "3341-4444" in answer and "3321-4500" in answer
    assert "Não consigo confirmar" in answer
    assert ambiguity_reply("Qual é o WhatsApp?", []) is None


def test_installment_conflict_is_not_silently_resolved():
    sources = [{"page": 3, "content": "Tabela 100,00; seção específica 80,00"}]
    answer = ambiguity_reply("Posso pagar em 6 vezes?", sources)
    assert "100,00" in answer and "80,00" in answer and "confirmar" in answer


def test_warranty_uses_distinct_purchase_and_receipt_dates():
    sources = [
        {"page": 4, "content": "30 dias compra"},
        {"page": 7, "content": "90 dias recebimento"},
    ]
    answer = ambiguity_reply("Defeito depois de 45 dias?", sources)
    assert "após a compra" in answer and "recebimento" in answer
    assert "não concluo" in answer


def test_return_policy_does_not_confirm_facts_the_customer_did_not_supply():
    sources = [{"page": 4, "content": "Arrependimento em 7 (sete) dias"}]
    answer = ambiguity_reply("Quero devolver, tenho embalagem e manuais.", sources)
    assert "Confira" in answer and "acessórios" in answer
    assert "você confirmou" not in answer and "online" in answer
