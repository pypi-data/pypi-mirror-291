from typing import List, Optional, Tuple, TypeVar, Union

from gpuhunt._internal.models import (
    AcceleratorVendor,
    AMDGPUInfo,
    CatalogItem,
    NvidiaGPUInfo,
    QueryFilter,
    TPUInfo,
)

# v5litepod = v5e
_TPU_VERSIONS = ["v2", "v3", "v4", "v5p", "v5litepod"]


def _is_tpu(name: str) -> bool:
    parts = name.split("-")
    if len(parts) == 2:
        version, cores = parts
        if version in _TPU_VERSIONS and cores.isdigit():
            return True
    return False


Comparable = TypeVar("Comparable", bound=Union[int, float, Tuple[int, int]])


def is_between(value: Comparable, left: Optional[Comparable], right: Optional[Comparable]) -> bool:
    if is_below(value, left) or is_above(value, right):
        return False
    return True


def is_below(value: Comparable, limit: Optional[Comparable]) -> bool:
    if limit is not None and value < limit:
        return True
    return False


def is_above(value: Comparable, limit: Optional[Comparable]) -> bool:
    if limit is not None and value > limit:
        return True
    return False


def matches(i: CatalogItem, q: QueryFilter) -> bool:
    """
    Check if the catalog item matches the filters

    Args:
        i: catalog item
        q: filters

    Returns:
        whether the catalog item matches the filters
    """
    # Common checks
    if q.provider is not None and i.provider.lower() not in map(str.lower, q.provider):
        return False
    if not is_between(i.price, q.min_price, q.max_price):
        return False
    if q.spot is not None and i.spot != q.spot:
        return False

    # TPU specific checks
    if i.gpu_vendor == AcceleratorVendor.GOOGLE and i.gpu_name and _is_tpu(i.gpu_name.lower()):
        if q.gpu_vendor is not None and q.gpu_vendor != AcceleratorVendor.GOOGLE:
            return False
        if q.gpu_name is not None:
            if i.gpu_name.lower() not in map(str.lower, q.gpu_name):
                return False
        return True

    # GPU & CPU checks
    if not is_between(i.cpu, q.min_cpu, q.max_cpu):
        return False
    if not is_between(i.memory, q.min_memory, q.max_memory):
        return False
    if q.gpu_vendor and q.gpu_vendor != i.gpu_vendor:
        return False
    if not is_between(i.gpu_count, q.min_gpu_count, q.max_gpu_count):
        return False
    if q.gpu_name is not None:
        if i.gpu_name is None:
            return False
        if i.gpu_name.lower() not in map(str.lower, q.gpu_name):
            return False
    if q.min_compute_capability is not None or q.max_compute_capability is not None:
        if i.gpu_vendor != AcceleratorVendor.NVIDIA:
            return False
        if not i.gpu_name:
            return False
        cc = get_compute_capability(i.gpu_name)
        if not cc or not is_between(cc, q.min_compute_capability, q.max_compute_capability):
            return False
    if not is_between(i.gpu_memory if i.gpu_count > 0 else 0, q.min_gpu_memory, q.max_gpu_memory):
        return False
    if not is_between(
        (i.gpu_count * i.gpu_memory) if i.gpu_count > 0 else 0,
        q.min_total_gpu_memory,
        q.max_total_gpu_memory,
    ):
        return False
    if i.disk_size is not None:
        if not is_between(i.disk_size, q.min_disk_size, q.max_disk_size):
            return False
    return True


def get_compute_capability(gpu_name: str) -> Optional[Tuple[int, int]]:
    for gpu in KNOWN_NVIDIA_GPUS:
        if gpu.name.lower() == gpu_name.lower():
            return gpu.compute_capability
    return None


def correct_gpu_memory_gib(gpu_name: str, memory_mib: float) -> int:
    """
    Round to whole number of gibibytes and attempt correcting the reported GPU
    memory size if the actual memory size for that GPU is known and the
    difference between the reported and the known memory is within a heuristic
    threshold.

    This is useful for cases when nvidia-smi or cloud providers report the GPU
    memory imprecisely.
    """

    memory_gib = memory_mib / 1024
    known_memories_gib = {gpu.memory for gpu in KNOWN_ACCELERATORS if gpu.name == gpu_name}
    if known_memories_gib:
        closest_known_memory_gib = min(known_memories_gib, key=lambda x: abs(x - memory_gib))
        difference_gib = abs(closest_known_memory_gib - memory_gib)
        if difference_gib / closest_known_memory_gib < 0.07:
            return closest_known_memory_gib
    return round(memory_gib)


KNOWN_NVIDIA_GPUS: List[NvidiaGPUInfo] = [
    NvidiaGPUInfo(name="A10", memory=24, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="A40", memory=48, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="A100", memory=40, compute_capability=(8, 0)),
    NvidiaGPUInfo(name="A100", memory=80, compute_capability=(8, 0)),
    NvidiaGPUInfo(name="A10G", memory=24, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="A4000", memory=16, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="A4500", memory=20, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="A5000", memory=24, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="A6000", memory=48, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="H100", memory=80, compute_capability=(9, 0)),
    NvidiaGPUInfo(name="H100NVL", memory=94, compute_capability=(9, 0)),
    NvidiaGPUInfo(name="L4", memory=24, compute_capability=(8, 9)),
    NvidiaGPUInfo(name="L40", memory=48, compute_capability=(8, 9)),
    NvidiaGPUInfo(name="L40S", memory=48, compute_capability=(8, 9)),
    NvidiaGPUInfo(name="P100", memory=16, compute_capability=(6, 0)),
    NvidiaGPUInfo(name="RTX3060", memory=8, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="RTX3060", memory=12, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="RTX3060Ti", memory=8, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="RTX3070Ti", memory=8, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="RTX3080", memory=10, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="RTX3080Ti", memory=12, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="RTX3090", memory=24, compute_capability=(8, 6)),
    NvidiaGPUInfo(name="RTX4090", memory=24, compute_capability=(8, 9)),
    NvidiaGPUInfo(name="RTX6000", memory=24, compute_capability=(7, 5)),
    NvidiaGPUInfo(name="RTX2000Ada", memory=16, compute_capability=(8, 9)),
    NvidiaGPUInfo(name="RTX4000Ada", memory=20, compute_capability=(8, 9)),
    NvidiaGPUInfo(name="RTX6000Ada", memory=48, compute_capability=(8, 9)),
    NvidiaGPUInfo(name="T4", memory=16, compute_capability=(7, 5)),
    NvidiaGPUInfo(name="V100", memory=16, compute_capability=(7, 0)),
    NvidiaGPUInfo(name="V100", memory=32, compute_capability=(7, 0)),
]

KNOWN_AMD_GPUS: List[AMDGPUInfo] = [
    AMDGPUInfo(name="MI300X", memory=192),
]

KNOWN_TPUS: List[TPUInfo] = [TPUInfo(name=version, memory=0) for version in _TPU_VERSIONS]

KNOWN_ACCELERATORS: List[Union[NvidiaGPUInfo, AMDGPUInfo, TPUInfo]] = (
    KNOWN_NVIDIA_GPUS + KNOWN_AMD_GPUS + KNOWN_TPUS
)
