from .configure import get_ak_sk
from .aihc_argumentparser import config_file
from .utils import send_request
import pandas as pd
from datetime import datetime
import json

###############################################################################################################################################
#                                                           资源池相关接口
###############################################################################################################################################

# 打印资源池列表
def list_resource_pool_pd():
    all_data = list_resource_pool()

    if not all_data:
        column_names = [
            "ID", "NAME", "STATUS", "REGION", "NODES(READY/TOTAL)",
            "GPUS(ALLOCATED/TOTAL)", "CREATEDTIME"
        ]
        empty_df = pd.DataFrame(columns=column_names)
        return empty_df.to_string(index=False)

    data_rows = [
        {
            "ID": pool["metadata"]["id"],
            "NAME": pool["metadata"]["name"],
            "STATUS": pool["status"]["phase"],
            "REGION": pool["spec"]["region"],
            "NODES(READY/TOTAL)": f"{pool['status']['nodeCount']['used']}/{pool['status']['nodeCount']['total']}",
            "GPUS(ALLOCATED/TOTAL)": f"{pool['status']['gpuCount']['used']}/{pool['status']['gpuCount']['total']}",
            "CREATEDTIME": datetime.strptime(pool["metadata"]["createdAt"], "%Y-%m-%dT%H:%M:%Sz").strftime("%Y-%m-%d %H:%M:%S")
        }
        for pool in all_data
    ]

    return pd.DataFrame(data_rows).to_string(index=False)

# 获取资源池列表
def list_resource_pool():
    ak, sk, host = get_ak_sk(config_file)
    list_pool_url = f'http://{host}/api/v1/resourcepools?pageSize=20'

    all_data = []
    page = 1
    has_more = True 

    while has_more:
        response = send_request(list_pool_url + "&pageNo=" + str(page), "get", ak, sk)
        for pool in response["result"]["resourcePools"]:
            all_data.append(pool)
        has_more = True if 20 * page <= int(response["result"]["total"]) else False
        page += 1

    return all_data


# 获取资源池详情
def get_resource_pool(resource_pool_name):
    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(resource_pool_name)

    get_resource_pool_url = f'http://{host}/api/v1/resourcepools/{resource_pool_id}?resourcePoolId={resource_pool_id}'
    data = send_request(get_resource_pool_url, "get", ak, sk)
    resource_pool = data["result"]["resourcePool"]
    datadict = {
        "ID": resource_pool["metadata"]["id"],
        "NAME": resource_pool["metadata"]["name"],
        "STATUS": resource_pool["status"]["phase"],
        "REGION": resource_pool["spec"]["region"],
        "NODES(READY/TOTAL)": f"{resource_pool['status']['nodeCount']['used']}/{resource_pool['status']['nodeCount']['total']}",
        "GPU(ALLOCATED/TOTAL)": f"{resource_pool['status']['gpuCount']['used']}/{resource_pool['status']['gpuCount']['total']}",
        "CREATEDTIME": datetime.strptime(resource_pool["metadata"]["createdAt"], "%Y-%m-%dT%H:%M:%Sz").strftime("%Y-%m-%d %H:%M:%S"),
        "PFS_ID": resource_pool["spec"]["associatedPfsId"],
        "CPROM_ID": resource_pool["spec"]["associatedCpromIds"]
    }
    return pd.DataFrame([datadict]).to_string(index=False)


def get_pool_id_by_name(pool_name):
    data = list_resource_pool() 
    for pool in data:
        if pool_name == pool["metadata"]["name"]:
            return pool["metadata"]["id"]  
    return None