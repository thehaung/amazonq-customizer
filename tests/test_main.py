from typer.testing import CliRunner
from amazonq_customizer.main import app

runner = CliRunner()

def test_app_exists():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.stdout