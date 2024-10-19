from .runner import Runner


class RunnerPool:
    def __init__(self) -> None:
        self.runners: list[Runner] = []

    def register(self, runner: Runner) -> None:
        self.runners.append(runner)
