from .configure import get_ak_sk
from .aihc_argumentparser import config_file
from .resourcepool import get_pool_id_by_name
from .utils import send_request, gpu_exits
import pandas as pd
from datetime import datetime

gpu_dict = {
    'baidu.com/v100_16g_cgpu': "Tesla V100-SXM2-16GB",
    'baidu.com/v100_32g_cgpu': "Tesla V100-SXM2-32GB",
    'baidu.com/t4_16g_cgpu': "Tesla T4",
    'baidu.com/a100_80g_cgpu': 'NVIDIA A100-SXM4-80GB',
    'baidu.com/a100_40g_cgpu': 'NVIDIA A100-SXM4-40GB',
    'baidu.com/a800_80g_cgpu': 'NVIDIA A800-SXM4-80GB',
    'baidu.com/a30_24g_cgpu': 'NVIDIA A30',
    'baidu.com/a10_24g_cgpu': 'NVIDIA A10',
    'baidu.com/rtx_3090_cgpu': 'NVIDIA GeForce RTX 3090',
    'baidu.com/rtx_3080_cgpu': 'NVIDIA GeForce RTX 3080',
    'baidu.com/rtx_4090_cgpu': 'NVIDIA GeForce RTX 4090',
    'baidu.com/h800_80g_cgpu': 'NVIDIA H800',
    'baidu.com/p40_8_cgpu': 'Tesla P40',
    'baidu.com/l20_cgpu': 'NVIDIA L20',
    'baidu.com/cgpu': '--',
    'nvidia.com/gpu': '--', 
    'huawei.com/Ascend910': 'Huawei Ascend910', 
    'kunlunxin.com/xpu': 'KUNLUNXIN-P800',
}

def list_queue_pd(pool_name):
    """
    列出指定资源池中的队列，并以 pandas DataFrame 格式返回。
    
    Args:
        pool_name (str): 需要查看的资源池名称。
    
    Returns:
        str: 包含所有队列信息的字符串，如果没有队列则返回空字符串。
    """
    all_data = list_resource_pool_queue(pool_name)

    if not all_data:
        column_names = [
            "NAME", "GPU_TYPE", "GPU(ALLOCATED/TOTAL)", "NOTE", "CREATEDTIME"
        ]
        empty_df = pd.DataFrame(columns=column_names)
        return empty_df.to_string(index=False)
    
    data_rows = [
        {
            "NAME": queue["name"],
            "GPU_TYPE": get_gpu_type(queue),
            "GPU(ALLOCATED/TOTAL)": get_gpu_quantity(queue),
            "NOTE": queue["description"] if "description" in queue else "",
            "CREATEDTIME": datetime.strptime(queue["createdTime"], "%Y-%m-%dT%H:%M:%Sz").strftime("%Y-%m-%d %H:%M:%S")
        }
        for queue in all_data
        if queue["name"] != "63a9f0ea7bb98050796b649e85481845"
    ]
    
    return pd.DataFrame(data_rows).to_string(index=False)

# 获取资源池队列列表
def list_resource_pool_queue(resource_pool_name):
    """
    列出指定资源池的队列。
    
    Args:
        resource_pool_name (str) – 资源池名称，类型为str。
    
    Returns:
        List[dict] – 返回一个包含所有队列信息的列表，每个元素是一个字典，包括队列ID、名称等信息。
    
    Raises:
        无。
    """
    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(resource_pool_name)
    list_resource_pool_queue_url = f'http://{host}/api/v1/resourcepools/{resource_pool_id}/queue?pageSize=20'

    all_data = []
    page = 1
    has_more = True 

    while has_more:
        response = send_request(list_resource_pool_queue_url + "&pageNo=" + str(page), "get", ak, sk)
        for queue in response["result"]["queues"]:
            all_data.append(queue)
        has_more = True if 20 * page <= int(response["result"]["total"]) else False
        page += 1

    return all_data

# 获取队列详情
def get_queue(resource_pool_name, queue_name):
    """
    获取指定资源池和队列的信息，返回包含名称、GPU类型、已分配/总量、备注和创建时间等字段的 DataFrame。
    
    Args:
        resource_pool_name (str): 需要查询的资源池名称。
        queue_name (str): 需要查询的队列名称。
    
    Returns:
        str: 包含名称、GPU类型、已分配/总量、备注和创建时间等字段的 DataFrame 的字符串表示形式。
    """
    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(resource_pool_name)

    get_queue_url = f'http://{host}/api/v1/resourcepools/{resource_pool_id}/queue/{queue_name}?resourcePoolId={resource_pool_id}&queueName={queue_name}'
    data = send_request(get_queue_url, "get", ak, sk)

    queue = data["result"]["queue"]
    datadict = {
        "NAME": queue["name"],
        "GPU_TYPE": get_gpu_type(queue),
        "GPU(ALLOCATED/TOTAL)": get_gpu_quantity(queue), 
        "NOTE": queue["description"] if "description" in queue else "",
        "CREATEDTIME": datetime.strptime(queue["createdTime"], "%Y-%m-%dT%H:%M:%Sz").strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return pd.DataFrame([datadict]).to_string(index=False)

def get_gpu_type(queue):
    """
    获取GPU类型，返回一个字符串列表，每个元素为一种GPU类型。如果GPU不存在于指定的队列中，则返回该GPU类型。
    如果队列中没有包含任何GPU类型，则返回一个空列表或者一个'-'。
    
    Args:
        queue (dict): 包含GPU信息的字典，格式为{"deserved": {"gpu1": ..., "gpu2": ...}, "capability": {"gpu3": ...}}。
            其中"deserved"和"capability"是可选项，如果不存在则视为空列表。
            如果"deserved"和"capability"都不存在，则返回一个空列表或者一个'-'。
    
    Returns:
        str or list: 返回一个字符串列表，每个元素为一种GPU类型。如果GPU不存在于指定的队列中，则返回该GPU类型。如果队列中没有包含任何GPU类型，则返回一个空列表或者一个'-'。
    """
    res = []
    if "deserved" in queue:
        for key in queue["deserved"]:
            if "gpu" in key:
                if gpu_exits(gpu_dict, key):
                    res.append(gpu_dict[key])
                else:
                    res.append(key)
    elif "capability" in queue:
        for key in queue["capability"]:
            if "gpu" in key:
                if gpu_exits(gpu_dict, key):
                    res.append(gpu_dict[key])
                else:
                    res.append(key)
    else:
        return "-"
    return "\n".join(res)
    
def get_gpu_quantity(queue):
    """
    获取GPU数量，返回一个字符串格式的结果，包括已分配和总共的GPU数量。
    
    Args:
        queue (dict): 队列信息，包含两种格式：1. "deserved": {"gpu-1": 2, "gpu-2": 3}；2. "capability": {"gpu-1": 4, "gpu-2": 5}。
            其中"deserved"表示已被申请的GPU数量，"capability"表示可用的GPU数量。
    
    Returns:
        str: 返回一个字符串格式的结果，包括已分配和总共的GPU数量，格式为"{已分配}/{总共}"。如果没有任何GPU数量信息，则返回空字符串。
    """
    allocated = 0
    total = 0
    if "deserved" in queue:
        for key, value in queue["deserved"].items():
            if "gpu" in key:
                total += int(value)
    elif "capability" in queue:
        for key, value in queue["capability"].items():
            if "gpu" in key:
                total += int(value)
    
    if "allocated" in queue:
        for key, value in queue["allocated"].items():
            if "gpu" in key:
                allocated += int(value)
    return f'{allocated}/{total}'
