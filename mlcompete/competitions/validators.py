import logging
import random

from mlcompete.competitions.models import Phase, Run, Submission
from mlcompete.competitions.runners import default_runner_cls

logger = logging.getLogger(__name__)


class SubmissionValidator:
    """Run and validate a submission."""

    def __init__(self, submission: Submission, phase: Phase):
        self.submission = submission
        self.phase = phase

    def validate(self):
        runner = default_runner_cls()()
        run = Run(submission=self.submission, phase=self.phase, status="PENDING")
        run.save()
        try:
            runner.run(self.submission, self.phase)
        except ValueError:
            run.status = "FAILED"
            run.save()
            return

        # ios = StringIO(result)
        # df = pd.read_csv(ios, header=None)
        # ypred = df[0]
        # with self.phase.labels_file.open('r') as f:
        #     ytrue = pd.read_csv(f, header=None)[0]
        #
        # score = accuracy_score(ytrue, ypred)
        # run.score = score
        run.status = "SUCCESS"
        logger.warning("Not calculating real score. Generating random score.")
        run.score = random.random()
        run.save()
        return run.score
