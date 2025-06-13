from interfaces.cli import main


def test_execute_command(capsys):
    main(["execute-command", "test"])
    captured = capsys.readouterr()
    assert "Executing: test" in captured.out
