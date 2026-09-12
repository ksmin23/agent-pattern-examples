"""Sandbox selection and cleanup checks without remote resources."""
import ast
import json
import importlib.util
import os
import types
import unittest
from pathlib import Path
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, Mock, patch

NOTEBOOK = Path(__file__).resolve().parents[1] / 'patterns/sandboxed_agent/examples/workspace_inspection/notebooks/sandboxed_agent-ko.ipynb'


def backends():
    for cell in json.loads(NOTEBOOK.read_text())['cells']:
        if cell['cell_type'] != 'code':
            continue
        tree = ast.parse(''.join(cell['source']))
        nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in {'sandbox_backend', 'load_modal_credentials', 'sandbox_session'}]
        if nodes:
            ns = {'os': os, 'asynccontextmanager': asynccontextmanager, 'DEFAULT_PYTHON_SANDBOX_IMAGE': 'test-image'}
            exec(compile(ast.Module(body=nodes, type_ignores=[]), '<backend>', 'exec'), ns)
            yield ns


class SandboxBackendTests(unittest.IsolatedAsyncioTestCase):
    async def test_docker_cleanup_after_body_start_and_delete_errors(self):
        for ns in backends():
            for failure in ('body', 'start', 'delete', 'create', 'ping'):
                with self.subTest(failure=failure):
                    api = Mock()
                    session = AsyncMock()
                    client = Mock(create=AsyncMock(return_value=session), delete=AsyncMock())
                    if failure == 'start': session.start.side_effect = RuntimeError('start')
                    if failure == 'delete': client.delete.side_effect = RuntimeError('delete')
                    if failure == 'create': client.create.side_effect = RuntimeError('create')
                    if failure == 'ping': api.ping.side_effect = RuntimeError('ping')
                    with patch.dict(os.environ, {'SANDBOX_BACKEND': 'docker'}), patch('docker.from_env', return_value=api), patch('agents.sandbox.sandboxes.docker.DockerSandboxClient', return_value=client):
                        with self.assertRaises(RuntimeError):
                            async with ns['sandbox_session'](object()):
                                if failure == 'body': raise RuntimeError('body')
                    api.close.assert_called_once()
                    if failure not in ('create', 'ping'):
                        client.delete.assert_awaited_once_with(session)

    @unittest.skipUnless(importlib.util.find_spec("modal"), "Install openai-agents[modal] for the Modal adapter check")
    async def test_modal_backend_and_cleanup(self):
        # Use installed SDK option types; replace only the external client.
        for ns in backends():
            session = AsyncMock()
            client = Mock(create=AsyncMock(return_value=session), delete=AsyncMock())
            ns['load_modal_credentials'] = Mock()
            with patch.dict(os.environ, {'SANDBOX_BACKEND': 'modal'}), patch('agents.extensions.sandbox.ModalSandboxClient', return_value=client), patch('docker.from_env') as docker:
                async with ns['sandbox_session'](object()) as actual:
                    self.assertIs(actual, session)
            client.delete.assert_awaited_once_with(session)
            self.assertEqual(client.create.call_args.kwargs['options'].timeout, 300)
            ns['load_modal_credentials'].assert_called_once()
            docker.assert_not_called()

    def test_colab_default_and_modal_secret_loading(self):
        google = types.ModuleType('google')
        colab = types.ModuleType('google.colab')
        google.colab = colab
        userdata = types.SimpleNamespace(get=Mock(side_effect=lambda name: 'test-' + name))
        colab.userdata = userdata
        with patch.dict(os.environ, {}, clear=True), patch.dict('sys.modules', {'google': google, 'google.colab': colab}):
            for ns in backends():
                self.assertEqual(ns['sandbox_backend'](), 'modal')
                ns['load_modal_credentials']()
                self.assertTrue(os.environ['MODAL_TOKEN_ID'])
                self.assertTrue(os.environ['MODAL_TOKEN_SECRET'])
            self.assertEqual(userdata.get.call_count, 2)

    def test_local_default_and_invalid_override(self):
        with patch.dict(os.environ, {}, clear=True), patch.dict('sys.modules', {'google.colab': None}):
            for ns in backends():
                self.assertEqual(ns['sandbox_backend'](), 'docker')
                with patch.dict(os.environ, {'SANDBOX_BACKEND': 'invalid'}):
                    with self.assertRaises(ValueError): ns['sandbox_backend']()


if __name__ == '__main__':
    unittest.main()
