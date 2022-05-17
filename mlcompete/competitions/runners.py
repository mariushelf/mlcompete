import os
import subprocess
from tempfile import TemporaryDirectory

from mlcompete.competitions.models import Phase, Submission


class ScriptRunner:
    def run(self, submission: Submission, phase: Phase) -> str:
        """Run script for given phase.

        Returns
        -------
        predictions : str
            predictions made by the script as string, e.g., the contents of a csv file
        """
        raise NotImplementedError


class FakeRunner(ScriptRunner):
    def run(self, submission: Submission, phase: Phase) -> str:
        return "FAKE PREDICTION RUNNER"


class NaivePythonRunner(ScriptRunner):
    def run(self, submission: Submission, phase: Phase) -> str:
        with TemporaryDirectory() as tmpdir:
            self.prepare_directory(phase, submission, tmpdir)
            self.runscript("__main__.py", tmpdir)
            result = self.read_results(tmpdir)
        return result

    def read_results(self, directory):
        with open(directory / "predictions" / "result") as f:
            result = f.read()
        return result

    def runscript(self, scriptfile: str, cwd: str) -> None:
        result = subprocess.run(["python", scriptfile], cwd=cwd)
        if result.returncode != 0:
            raise ValueError("script failed to execute")

    def prepare_directory(self, phase, submission, tmpdir):
        with phase.data_file.open("r") as f:
            data = f.read()
        with open(tmpdir / "data", "w") as f:
            f.write(data)
        with submission.script_file.open("r") as f:
            script = f.read()
        with open(tmpdir / "__main__.py", "w") as f:
            f.write(script)
        os.mkdir(tmpdir / "predictions")


def default_runner_cls():
    return FakeRunner
