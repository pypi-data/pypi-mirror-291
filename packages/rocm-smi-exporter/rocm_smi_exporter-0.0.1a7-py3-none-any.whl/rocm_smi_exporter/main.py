from dataclasses import dataclass
import time

from prometheus_client import start_http_server, Gauge

import logging
from pyrsmi import rocml

logger = logging.getLogger(__name__)


import platform
HOSTNAME = platform.node()

LABEL_UID = "gpuUid"
LABEL_GPU = "gpu"
LABEL_MODEL_NAME = "modelName"
LABEL_HOSTNAME = "Hostname"
LABEL_RSMI_VERSION = "rsmiVersion"
LABEL_ROCM_KERNEL_VERSION = "rocmKernelVersion"
LABELS = [LABEL_UID, LABEL_GPU, LABEL_MODEL_NAME, LABEL_HOSTNAME, LABEL_RSMI_VERSION, LABEL_ROCM_KERNEL_VERSION]

def _get_common_labels(uid: str, gpu: str, model_name: str):
    """
    Returns a dict of the common labels for metric
    """
    res = {}
    res[LABEL_UID] = uid
    res[LABEL_GPU] = gpu
    res[LABEL_MODEL_NAME] = model_name
    res[LABEL_HOSTNAME] = HOSTNAME
    res[LABEL_RSMI_VERSION] = rocml.smi_get_version()
    res[LABEL_ROCM_KERNEL_VERSION] = rocml.smi_get_kernel_version()
    return res

# These names are mimicing dcgm-exporter DCGM_FI_DEV_GPU_UTIL and DCGM_FI_DEV_MEM_COPY_UTIL
METRIC_GPU_UTIL = "ROCM_SMI_DEV_GPU_UTIL"
METRIC_GPU_MEM_TOTAL = "ROCM_SMI_DEV_GPU_MEM_TOTAL"
METRIC_GPU_MEM_USED = "ROCM_SMI_DEV_GPU_MEM_USED"
METRIC_GPU_MEM_UTIL = "ROCM_SMI_DEV_MEM_UTIL"
METRIC_GPU_POWER = "ROCM_SMI_DEV_POWER"
METRIC_GPU_CU_OCCUPANCY = "ROCM_SMI_DEV_CU_OCCUPANCY"

class GPUMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """
    @dataclass
    class Config:
        port: int
        polling_interval_seconds: int

    def __init__(self, config: Config):
        self.config = config

        rocml.smi_initialize()
        ngpus = rocml.smi_get_device_count()
        self.dev_list = list(range(ngpus))

        # Define Prometheus metrics to collect
        self.gpu_util = Gauge(METRIC_GPU_UTIL, "GPU utilization (in %).", LABELS)
        self.gpu_mem_used = Gauge(METRIC_GPU_MEM_USED, "GPU memory used (in Byte).", LABELS)
        self.gpu_mem_total = Gauge(METRIC_GPU_MEM_TOTAL, "GPU memory total (in Byte).", LABELS)
        self.gpu_mem_util = Gauge(METRIC_GPU_MEM_UTIL, "GPU memory utilization (in %).", LABELS)
        self.gpu_cu_occupancy = Gauge(METRIC_GPU_CU_OCCUPANCY, "GPU CU occupancy (in %).", LABELS)

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        logger.info(f"Starting expoerter on :{self.config.port}")
        start_http_server(self.config.port)
        while True:
            logger.info(f"Fetching metrics ...")
            self.fetch()
            time.sleep(self.config.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics.
        """
        for _, dev in enumerate(self.dev_list):
            uid = rocml.smi_get_device_unique_id(dev)
            dev_model_name = rocml.smi_get_device_name(dev)
            labels = _get_common_labels(uid, dev, dev_model_name)

            util = rocml.smi_get_device_utilization(dev)
            self.gpu_util.labels(**labels).set(util)
            
            mem_used = rocml.smi_get_device_memory_used(dev)
            self.gpu_mem_used.labels(**labels).set(mem_used)

            mem_total = rocml.smi_get_device_memory_total(dev)
            self.gpu_mem_total.labels(**labels).set(mem_total)

            mem_ratio = mem_used / mem_total
            self.gpu_mem_util.labels(**labels).set(mem_ratio)

            cu_occupancy = smi_get_device_cu_occupancy(dev)
            self.gpu_cu_occupancy.labels(**labels).set(cu_occupancy)


def smi_get_device_cu_occupancy(dev):
    """returns list of process ids running compute on the device dev"""
    num_procs = rocml.c_uint32()
    ret = rocml.rocm_lib.rsmi_compute_process_info_get(None, rocml.byref(num_procs))
    if rocml.rsmi_ret_ok(ret):
        buff_sz = num_procs.value + 10
        proc_info = (rocml.rsmi_process_info_t * buff_sz)()
        ret2 = rocml.rocm_lib.rsmi_compute_process_info_get(rocml.byref(proc_info), rocml.byref(num_procs))
        
        return sum(proc_info[i].cu_occupancy for i in range(num_procs.value)) if rocml.rsmi_ret_ok(ret2) else 0
    else:
        return 0

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parse command line arguments for port and polling interval.')

    parser.add_argument('--port', type=int, default=9001, help='Port number to use.')
    parser.add_argument('--polling-interval-seconds', type=int, default=5, help='Polling interval in seconds.')

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    app_metrics = GPUMetrics(
        GPUMetrics.Config(
            port=args.port,
            polling_interval_seconds=args.polling_interval_seconds
        )
    )
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
