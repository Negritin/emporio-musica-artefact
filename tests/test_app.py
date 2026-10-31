from dataclasses import replace
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from emporio.config import ROOT, Settings


def test_local_chat_blocks_private_request_and_can_reset():
    settings = replace(Settings(), api_key="test-key", database_url="unused")
    with patch("emporio.config.Settings.load", return_value=settings):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15).run()
        assert not app.exception
        app.chat_input[0].set_value("Qual o status do meu pedido 123?").run()
        assert not app.exception
        assert len(app.chat_message) == 2
        assert any("autenticação" in m.value for m in app.markdown)
        app.sidebar.button[0].click().run()
        assert not app.chat_message and not app.exception
