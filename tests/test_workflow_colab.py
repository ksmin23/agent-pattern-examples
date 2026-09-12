"""Test notebook environment branches without credentials or API calls."""
import ast
import json
import os
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from dotenv import load_dotenv

NOTEBOOK = Path(__file__).resolve().parents[1] / 'patterns/workflow_planning/examples/research_report/notebooks/workflow_planning-ko.ipynb'


def code_cells():
    return [''.join(c['source']) for c in json.loads(NOTEBOOK.read_text())['cells'] if c['cell_type'] == 'code']


def loaders():
    for source in code_cells():
        nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'load_environment']
        if nodes:
            namespace = {'os': os, 'find_dotenv': Mock(return_value=''), 'load_dotenv': load_dotenv}
            exec(compile(ast.Module(body=nodes, type_ignores=[]), '<loader>', 'exec'), namespace)
            yield namespace


class WorkflowEnvironmentTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {}, clear=True)
        env.start()
        self.addCleanup(env.stop)
        self.userdata = types.ModuleType('google.colab.userdata')
        for name in ('SecretNotFoundError', 'NotebookAccessError', 'TimeoutException'):
            setattr(self.userdata, name, type(name, (Exception,), {}))
        self.userdata.get = Mock(return_value='test-only-secret')
        google = types.ModuleType('google')
        colab = types.ModuleType('google.colab')
        google.colab = colab
        colab.userdata = self.userdata
        self.modules = {'google': google, 'google.colab': colab, 'google.colab.userdata': self.userdata}

    def test_offline_needs_no_key_or_secret_access(self):
        with patch.dict('sys.modules', self.modules):
            for ns in loaders():
                self.assertEqual(ns['load_environment'](run_api=False), 'gpt-5.6-luna')
        self.userdata.get.assert_not_called()
        self.assertNotIn('OPENAI_API_KEY', os.environ)

    def test_colab_secret_reused_in_memory(self):
        for ns in loaders():
            os.environ.pop('OPENAI_API_KEY', None)
            with patch.dict('sys.modules', self.modules):
                ns['load_environment'](run_api=True)
            self.assertEqual(os.environ['OPENAI_API_KEY'], 'test-only-secret')
        self.assertEqual(self.userdata.get.call_count, 2)

    def test_local_env_file_and_existing_environment_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = Path(tmp) / '.env.local'
            env.write_text('OPENAI_API_KEY=file-test-value\nAGENT_MODEL=test-model\n')
            for ns in loaders():
                ns['find_dotenv'].return_value = str(env)
                os.environ.pop('OPENAI_API_KEY', None)
                with patch.dict('sys.modules', {'google.colab': None}):
                    self.assertEqual(ns['load_environment'](run_api=True), 'test-model')
                    self.assertEqual(os.environ['OPENAI_API_KEY'], 'file-test-value')
                    os.environ['OPENAI_API_KEY'] = 'existing-test-value'
                    ns['load_environment'](run_api=True)
                    self.assertEqual(os.environ['OPENAI_API_KEY'], 'existing-test-value')

    def test_existing_environment_skips_colab_secrets(self):
        os.environ['OPENAI_API_KEY'] = 'existing-test-value'
        with patch.dict('sys.modules', self.modules):
            for ns in loaders():
                ns['load_environment'](run_api=True)
        self.userdata.get.assert_not_called()

    def test_secret_errors_are_actionable_and_do_not_leak(self):
        for name in ('SecretNotFoundError', 'NotebookAccessError', 'TimeoutException'):
            self.userdata.get.side_effect = getattr(self.userdata, name)('private error detail')
            for ns in loaders():
                with patch.dict('sys.modules', self.modules), self.assertRaises(RuntimeError) as error:
                    ns['load_environment'](run_api=True)
                self.assertIn('Colab Secrets', str(error.exception))
                self.assertNotIn('private error detail', str(error.exception))
                self.assertTrue(error.exception.__suppress_context__)

    def test_missing_local_key_fails_only_in_live_mode(self):
        with patch.dict('sys.modules', {'google.colab': None}):
            for ns in loaders():
                ns['load_environment'](run_api=False)
                with self.assertRaisesRegex(RuntimeError, 'Set OPENAI_API_KEY'):
                    ns['load_environment'](run_api=True)

    def test_installation_only_in_colab(self):
        bootstrap = code_cells()[0].split('from agents import', 1)[0]
        for colab in (False, True):
            modules = self.modules if colab else {'google.colab': None}
            with patch.dict('sys.modules', modules), patch('subprocess.check_call') as install, patch('importlib.metadata.version', return_value='0.0'):
                exec(bootstrap, {})
            self.assertEqual(install.call_count, int(colab))
            if colab:
                self.assertIn('openai-agents==0.22.1', install.call_args.args[0])

    def test_matching_colab_dependencies_skip_installation(self):
        bootstrap = code_cells()[0].split('from agents import', 1)[0]
        with patch.dict('sys.modules', self.modules), patch('subprocess.check_call') as install, patch('importlib.metadata.version', side_effect=['0.22.1', '1.2.3']):
            exec(bootstrap, {})
        install.assert_not_called()


if __name__ == '__main__':
    unittest.main()
