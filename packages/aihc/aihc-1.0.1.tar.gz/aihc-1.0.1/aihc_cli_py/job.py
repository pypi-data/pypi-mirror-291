from .aihc_argumentparser import config_file
from .utils import send_request
from .configure import get_ak_sk, get_username_password
from .resourcepool import get_pool_id_by_name
from .create_job_request import *
import pandas as pd
import json
from datetime import datetime

###########################################################################################################
#                                                任务相关接口
###########################################################################################################

# 创建任务
def create_job(args):
    global image_config
    if args.username is not None and args.password is not None:
        image_config = ImageConfig(
            username=args.username,
            password=args.password
        )
    else:
        username, password = get_username_password(config_file)
        if username is not None and password is not None:
            image_config = ImageConfig(
                username=username,
                password=password,
            )
    # =========================================== 处理 queue ==========================================
    queue = "default"
    if args.queue is not None:
        queue = args.queue

    # =========================================== 处理 jobFramework ==========================================
    job_framework = JobFramework.PY_TORCH_JOB
    if args.framework == "mpi":
        job_framework = JobFramework.MPI_JOB

    # =========================================== 封装JobSpec ==========================================
    resources = []
    if args.gpu is not None and args.gpu > 0:
        resource = Resource(
            name="baidu.com/a800_80g_cgpu",
            quantity=args.gpu
        )
        resources.append(resource)

    if args.cpu is not None and args.cpu > 0:
        resource = Resource(
            name="cpu",
            quantity=args.cpu
        )
        resources.append(resource)

    if args.memory is not None:
        resource = Resource(
            name="memory",
            quantity=str(args.memory) + "GB"
        )
        resources.append(resource)
    
    if args.rdma == True:
        resource = Resource(
            name="rdma/hca",
            quantity="1"
        )
        resources.append(resource)

    envs = []
    if args.envs is not None:
        for env in args.envs:
            s = env.split('=')
            e = Env(
                name=s[0],
                value=s[1]
            )
            envs.append(e)

    command = ""
    if args.command is not None:
        command = args.command
    elif args.script is not None:
        with open(args.script, 'r', encoding='utf-8') as f:
            command = f.read()

    job_spec = JobSpec(
        command=command,
        enable_rdma=args.rdma,
        envs=envs,
        image=args.image,
        image_config=image_config,
        replicas=args.replicas,
        resources=resources,
        host_network=args.hostnetwork,
    )

    # =========================================== 处理标签 ==========================================
    labels = []

    if args.labels is not None:
        for label in args.labels:
            s = label.split('=')
            l = Label(
                key=s[0],
                value=s[1]
            )
            labels.append(l)

    # =========================================== 处理优先级 ==========================================
    priority = Priority.NORMAL
    if args.priority is not None:
        if args.priority == "high":
            priority = Priority.HIGH
        elif args.priority == "low":
            priority = Priority.LOW
        else:
            priority = Priority.NORMAL

    # =========================================== 配置数据源 ==========================================
    datasource = Datasource(
        mount_path=args.mount_path,
        name=args.pfs_id,
        type=TypeEnum.PFS
    )
    datasources = [datasource]

    # =========================================== 配置故障容忍策略 ==========================================
    fault_tolerance_config = FaultToleranceConfig("", "", "")
    if args.hangdetection is not None:
        fault_tolerance_config.enabled_hang_detection=args.hangdetection
    if args.faulttolerancelimit is not None:
        fault_tolerance_config.fault_tolerance_limit=args.faulttolerancelimit
    if args.hangtimeout is not None:
        fault_tolerance_config.hang_detection_timeout_minutes=args.hangtimeout,

    # 最终实例化 Request 类
    request = Request(
        datasources=datasources,
        fault_tolerance=args.faulttolerance,
        fault_tolerance_config=fault_tolerance_config,
        job_framework=job_framework,
        job_spec=job_spec,
        labels=labels,
        name=args.name,
        priority=priority,
        queue=queue,
    )

    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(args.pool_name)
    create_job_url = f'http://{host}/api/v1/aijobs?resourcePoolId={resource_pool_id}'
    data = send_request(create_job_url, "post", ak, sk, json=request.to_dict())
    return "Job {}/{} created successfully".format(data["result"]["jobName"], data["result"]["jobId"])

def list_job_by_id(resource_pool_id):
    """
    根据资源池ID列出作业。
    
    Args:
        resource_pool_id (int): 资源池的ID。
    
    Returns:
        List[Dict]: 包含作业信息的字典列表，包括作业ID、名称、状态等。
    
    Raises:
        无。
    """
    ak, sk, host = get_ak_sk(config_file)
    list_job_url = f'http://{host}/api/v1/aijobs?resourcePoolId={resource_pool_id}&pageSize=20'
    
    all_data = []
    page = 1
    has_more = True

    while has_more:
        response = send_request(list_job_url + "&pageNo=" + str(page), "get", ak, sk)
        for job in response["result"]["jobs"]:
            all_data.append(job)
        has_more = True if 10 * page <= int(response["result"]["total"]) else False
        page += 1

    return all_data

# 获取任务列表
def list_job(resource_pool_name, queue_name=None):
    """
    列出指定资源池中的所有作业，可选择按队列过滤。
    
    Args:
        resource_pool_name (str): 资源池名称。
        queue_name (str, optional): 队列名称，默认为None，表示不进行队列过滤。
    
    Returns:
        List[dict]: 包含所有作业信息的列表，每个元素是一个字典，包含作业的相关信息，格式如下：{"id": xxx, "name": yyy, ...}。
        其中"id"是作业ID，"name"是作业名称等。
    
    Raises:
        None
    """
    ak, sk, host = get_ak_sk(config_file)

    resource_pool_id = get_pool_id_by_name(resource_pool_name)
    list_job_url = f'http://{host}/api/v1/aijobs?resourcePoolId={resource_pool_id}&pageSize=20' 

    all_data = []
    page = 1
    has_more = True 

    if queue_name is not None:
        list_job_url += f'&Queue={queue_name}'

    while has_more:
        response = send_request(list_job_url + "&pageNo=" + str(page), "get", ak, sk)
        for job in response["result"]["jobs"]:
            all_data.append(job)
        has_more = True if 10 * page <= int(response["result"]["total"]) else False
        page += 1

    return all_data
    

def list_job_pd(resource_pool_name, queue_name=None, fm=None):
    all_data = list_job(resource_pool_name, queue_name)
    if not all_data:
        column_names = [
            "NAME", "ID", "RESOURCE_POOL_ID", "QUEUE", "FRAMEWORK", 
            "STATUS", "WORKERS (READY/TOTAL)", "GPU", "CREATOR", "CREATEDTIME"
        ]
        empty_df = pd.DataFrame(columns=column_names)
        return empty_df.to_string(index=False)

    datadict = {}
    name = []
    ids = []
    resourcepool = []
    queue = []
    framework = []
    status = []
    workers = []
    gpu = []
    creator = []
    create_time = []

    for job in all_data:
        if fm is not None and job["jobFramework"] != fm:
            continue
        framework.append(job["jobFramework"])
        name.append(job["name"])
        ids.append(job["jobId"])
        resourcepool.append(job["resourcePoolId"])
        queue.append(job["queue"])
        status.append(job["status"])
        datetime_obj = datetime.strptime(job["createdAt"], "%Y-%m-%dT%H:%M:%Sz")
        create_time.append(datetime_obj.strftime("%Y-%m-%d %H:%M:%S"))
        creator.append(get_creator(job))
        gpu_str = ""
        for r in job["resources"]:
            if "a800_80g" in r["name"] or "h800_80g" in r["name"]:
                gpu_str += r["name"] + ":" + str(r["quantity"])
        gpu.append(gpu_str)
        d = get_job(job["jobId"], job["resourcePoolId"])
        cnt = 0
        for pod in d["result"]["podList"]["pods"]:
            if pod["podStatus"]["status"] == "READY":
                cnt += 1
        workers.append(str(cnt) + '/' + str(d["result"]["podList"]["listMeta"]["totalItems"]))

    datadict["NAME"] = name
    datadict["ID"] = ids
    datadict["RESOURCE_POOL_ID"] = resourcepool
    datadict["QUEUE"] = queue
    datadict["FRAMEWORK"] = framework
    datadict["STATUS"] = status
    datadict["WORKERS (READY/TOTAL)"] = workers
    datadict["GPU"] = gpu
    datadict["CREATOR"] = creator
    datadict["CREATEDTIME"] = create_time

    return pd.DataFrame(datadict).to_string(index=False)

def get_job(job_id, resource_pool_id):
    """
    根据任务ID和资源池ID获取作业信息。
    
    Args:
        job_id (str): 任务ID，可以是字符串或整数类型。
        resource_pool_id (int): 资源池ID，必须为正整数。
    
    Returns:
        dict, None: 返回一个字典对象，包含作业的相关信息；如果请求失败，则返回None。
    
    Raises:
        无。
    """
    ak, sk, host = get_ak_sk(config_file)
    joblist_url = f'http://{host}/api/v1/aijobs/{job_id}?resourcePoolId={resource_pool_id}'
    return send_request(joblist_url, "get", ak, sk)

# 获取任务详情
def get_job_pd(resource_pool_name, job_name, pods=None):
    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(resource_pool_name)
    job_id = get_job_id_by_name(resource_pool_id, job_name)

    get_job_url = f'http://{host}/api/v1/aijobs/{job_id}?resourcePoolId={resource_pool_id}'
    data = send_request(get_job_url, "get", ak, sk)

    if pods is None:
        return data

    datadict = {}
    if pods == False:
        datadict["NAME"] = data["result"]["name"]
        datadict["RESOURCE_POOL_ID"] = data["result"]["resourcePoolId"]
        datadict["QUEUE"] = data["result"]["queue"]
        datadict["FRAMEWORK"] = data["result"]["jobFramework"]
        datadict["STATUS"] = data["result"]["status"]
        ready_count = sum(pod["podStatus"]["status"] == "READY" for pod in data["result"]["podList"]["pods"])
        total_pods = data["result"]["podList"]["listMeta"]["totalItems"]
        datadict["WORKERS (READY/TOTAL)"] = f"{ready_count}/{total_pods}"
        datadict["GPU"] = get_gpu(data)
        datadict["CREATOR"] = get_creator(data["result"])
        datetime_obj = datetime.strptime(data["result"]["createdAt"], "%Y-%m-%dT%H:%M:%Sz")
        datadict["CREATEDTIME"] = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        return pd.DataFrame([datadict]).to_string(index=False)
    else:
        pods = data["result"]["podList"]["pods"]
        data_rows = [
            {
                "PODNAME": pod["objectMeta"]["name"],
                "WORKERTYPE": pod["replicaType"],
                "IP": pod["PodIP"],
                "STATUS": pod["podStatus"]["status"],
                "GPU": get_gpu(data["result"]["resources"]),
                "STARTTIME": pod["objectMeta"]["creationTimestamp"],
                "FINISHTIME": pod["finishedAt"],
            }
            for pod in pods
        ]
        return pd.DataFrame(data_rows).to_string(index=False)


# 停止任务
def stop_job(job_id, resource_pool_name):
    """
    停止指定的作业，该作业必须在指定的资源池中。
    
    Args:
        job_id (str): 需要停止的作业ID。
        resource_pool_name (str): 作业所在的资源池名称。
    
    Returns:
        str: 返回一个字符串，包含了被停止的作业名称和资源池名称。格式为："{作业名称} in {资源池名称} was stoped"。
    
    Raises:
        无。
    """
    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(resource_pool_name)

    stop_job_url = f'http://{host}/api/v1/aijobs/{job_id}/stop?resourcePoolId={resource_pool_id}'
    data = send_request(stop_job_url, "post", ak, sk)
    return "{} in {} was stoped".format(data["result"]["jobName"], resource_pool_name)


# 删除任务
def delete_job(job_id ,resource_pool_name):
    """
    删除指定任务ID和资源池名称的作业。
    
    Args:
        job_id (str): 需要删除的作业ID。
        resource_pool_name (str): 需要删除作业所在的资源池名称。
    
    Returns:
        str: 返回一个字符串，包含已经删除的作业名称和资源池名称。
    
    Raises:
        无。
    """
    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(resource_pool_name)

    delete_job_url = f'http://{host}/api/v1/aijobs/{job_id}?resourcePoolId={resource_pool_id}'
    data = send_request(delete_job_url, "delete", ak, sk)
    return "{} in {} was deleted".format(data["result"]["jobName"], resource_pool_name)


# 查询任务日志
def get_job_logs(job_name, pool_name, tail, podname):
    """
    获取作业的日志，可以指定要查看的具体pod名称。如果不指定pod名称，则会返回所有pod的日志。
    
    Args:
        job_name (str): 作业名称，用于获取作业ID。
        pool_name (str): 资源池名称，用于获取资源池ID。
        tail (int, optional): 最近多少行日志，默认为100。
        podname (str, optional): 要查看的具体pod名称，如果不指定则返回所有pod的日志。默认为None。
    
    Returns:
        str: 作业的日志信息，包括每个pod的日志，格式为："<pod_name>: <log>"。如果出现错误，则返回错误信息。
    """
    ak, sk, host = get_ak_sk(config_file)
    resource_pool_id = get_pool_id_by_name(pool_name)
    job_id = get_job_id_by_name(resource_pool_id, job_name)

    if podname is not None:
        job_logs_url = f'http://{host}/api/v1/aijobs/{job_id}/pods/{podname}/logs?resourcePoolId={resource_pool_id}&maxLines={tail}'
        try:
            data = send_request(job_logs_url, "get", ak, sk)
            return f"{data['result']['podName']}: \n{data['result']['logs']}"
        except Exception as e:
            return f"Failed to get logs for pod {podname}: {e}"
    else:
        try:
            job_info = get_job(job_id, resource_pool_id)
            pod_logs = []
            for pod in job_info["result"]["podList"]["pods"]:
                pod_name = pod["objectMeta"]["name"]
                job_logs_url = f'http://{host}/api/v1/aijobs/{job_id}/pods/{pod_name}/logs?resourcePoolId={resource_pool_id}&maxLines={tail}'
                data = send_request(job_logs_url, "get", ak, sk)
                pod_logs.append(f"{data['result']['podName']}:\n{data['result']['logs']}")
            return "\n".join(pod_logs)
        except Exception as e:
            return f"Failed to get job logs: {str(e)}"

def get_job_id_by_name(resource_pool_id, job_name):
    """
    根据资源池ID和作业名称获取作业ID。
    
    Args:
        resource_pool_id (str): 资源池ID，字符串类型。
        job_name (str): 作业名称，字符串类型。
    
    Returns:
        str: 返回作业ID，如果找不到匹配的作业则返回空字符串("")。
    """
    data = list_job_by_id(resource_pool_id) 
    for job in data:
        if job_name == job["name"]:
            return job["jobId"]  
    return ""

def get_gpu(data):
    """
    获取GPU信息，返回一个字符串，包含所有GPU的名称和数量。如果没有GPU，则返回空字符串。
    
    Args:
        data (dict): 包含结果信息的字典，其中包括"result"字段，该字段是一个字典，包含"resources"字段，该字段是一个列表，每个元素都是一个字典，包含"name"和"quantity"两个键值对。
    
    Returns:
        str: 返回一个字符串，包含所有GPU的名称和数量，每个GPU之间以换行符分隔。如果没有GPU，则返回空字符串。
    """
    gpu_str = ""
    for r in data["result"]["resources"]:
        if "gpu" in r["name"] :
            gpu_str += f"{r['name']}:{r['quantity']}\n"
    return gpu_str

def get_creator(data):
    """
    获取创建者信息，返回一个字符串，包含作业的创建者名称和时间。如果没有创建者信息，则返回空字符串。
    
    Args:
        data (dict): 包含结果信息的字典，其中包括"result"字段，该字段是一个字典，包含"createdBy"字段，该字段是一个字典，包含"name"和"time"两个键值对。
    
    Returns:
        str: 返回一个字符串，包含作业的创建者名称和时间，格式为："{创建者名称} {创建时间}"。如果没有创建者信息，则返回空字符串。
    """
    for label in data["labels"]:
        if label["key"] == "aijob.cce.baidubce.com/ai-user-name":
            return label["value"]