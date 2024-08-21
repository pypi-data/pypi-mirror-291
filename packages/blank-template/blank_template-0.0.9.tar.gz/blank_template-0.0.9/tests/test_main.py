from blank_template import app
from typer.testing import CliRunner


def test_main() -> None:
    runner = CliRunner()
    result = runner.invoke(app)
    assert "Hello" in result.stdout
