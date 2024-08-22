from typing import Any, Optional

from braket.ahs.analog_hamiltonian_simulation import AnalogHamiltonianSimulation
from planqk.aws.planqk_quantum_task import PlanqkBaseAwsQuantumTask
from planqk.client.backend_dtos import BackendDto, STATUS, PROVIDER
from planqk.client.client import _PlanqkClient
from planqk.qiskit import PlanqkQiskitJob


class PlanqkQueraAquilaBackend:

    def __init__(self, planqk_client: _PlanqkClient, **kwargs):
        self._planqk_client = planqk_client
        self._backend_info: BackendDto = kwargs.get('backend_info')
        self.name = self._backend_info.name

    @property
    def status(self) -> str:
        planqk_status: STATUS = self._planqk_client.get_backend(self._backend_info.id).status
        return "ONLINE" if planqk_status == STATUS.PAUSED else planqk_status.name

    @property
    def is_available(self) -> bool:
        planqk_status: STATUS = self._planqk_client.get_backend(self._backend_info.id).status
        return True if planqk_status == STATUS.ONLINE else False

    @property
    def backend_provider(self) -> str:
        return PROVIDER.AWS.name

    @property
    def version(self) -> int:
        return 1

    def run(self, task_specification: AnalogHamiltonianSimulation, shots: Optional[int] = None, *args: Any, **kwargs: Any) -> PlanqkQiskitJob:
        #job_details = self._planqk_client.submit_job(None)
        #job_details = self._planqk_client.submit_job(None)

        return PlanqkBaseAwsQuantumTask(backend=self, job_id=None, job_details={}, planqk_client=self._planqk_client)

