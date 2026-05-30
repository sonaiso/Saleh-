from dataclasses import dataclass

from .candidate import CandidateSet
from .kernel import QiyasKernel, QiyasRequest


@dataclass
class QiyasKernelAdapter:
    kernel: QiyasKernel

    def run(self, request: QiyasRequest) -> CandidateSet:
        return self.kernel.apply(request)
