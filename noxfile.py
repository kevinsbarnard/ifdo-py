import nox


nox.options.default_venv_backend = "uv"

@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def tests(session):
    session.install("pytest", "jsonschema", ".")
    session.run("pytest")
