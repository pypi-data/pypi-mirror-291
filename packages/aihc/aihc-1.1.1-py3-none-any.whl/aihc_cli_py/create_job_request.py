""""""
from enum import Enum
from typing import Optional, List, Dict


class SerializableEnum(Enum):
    """"""
    @classmethod
    def _missing_(cls, value):
        """
            如果找不到指定值，则返回一个新的成员。
        如果没有找到指定值，则引发ValueError异常。
        
        Args:
            value (Any): 要查找的值。
        
        Returns:
            Member (EnumMember): 与指定值相对应的EnumMember实例。
            如果未找到任何匹配项，则为None。
        
        Raises:
            ValueError: 如果value不是有效的EnumMember。
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    def to_dict(self):
        """
            将对象转换为字典格式，返回一个包含所有属性的字典。
        如果属性是一个对象或者列表，则会递归调用该方法进行转换。
        
        Returns:
            dict (dict): 包含所有属性的字典，其中每个属性都是一个值。
        """
        return self.value


class TypeEnum(SerializableEnum):
    """数据源类型，数据源类型，当前支持pfs"""
    PFS = "pfs"


class Datasource:
    """挂载点，容器内挂载点"""
    mount_path: str
    """数据源名称，数据源名称，如果type类型为pfs时，此处为必填，填pfs实例id"""
    name: str
    """数据源类型，数据源类型，当前支持pfs"""
    type: TypeEnum

    def __init__(self, mount_path: str, name: str, type: TypeEnum) -> None:
        """
            初始化类实例，用于存储挂载路径、名称和类型信息。
        
        Args:
            mount_path (str): 挂载路径，字符串格式。
            name (str): 名称，字符串格式。
            type (TypeEnum): 类型，TypeEnum 枚举值之一。
        
        Returns:
            None: 无返回值，实例已初始化完成。
        """
        self.mount_path = mount_path
        self.name = name
        self.type = type

    def to_dict(self):
        """
            将对象转换为字典，包含名称、类型和挂载路径等信息。
        
        Returns:
            dict - 一个包含以下键值对的字典：
                mountPath (str) - 挂载路径；
                name (str) - 名称；
                type (dict) - 类型，格式为{name: str, version: str}。
        """
        return {
            'mountPath': self.mount_path,
            'name': self.name,
            'type': self.type.to_dict()
        }


class FaultToleranceConfig:
    """开启 hang 检测，开启 hang 检测，需要 aibox 版本大于 1.6.22"""
    enabled_hang_detection: Optional[bool]
    """最大容错次数，最大容错次数，需要 aibox 版本大于 1.6.22"""
    fault_tolerance_limit: Optional[int]
    """hang 超时时间，当所有的 worker 超过这个时间没有输出日志，就认定当前任务出现 hang"""
    hang_detection_timeout_minutes: Optional[int]

    def __init__(self, enabled_hang_detection: Optional[bool], fault_tolerance_limit: Optional[int], 
                hang_detection_timeout_minutes: Optional[int]) -> None:
        """
            Initializes the instance with the given parameters.
        
        Args:
            enabled_hang_detection (Optional[bool]): Whether hang detection is enabled or not. Defaults to None.
            fault_tolerance_limit (Optional[int]): The fault tolerance limit for the job. Defaults to None.
            hang_detection_timeout_minutes (Optional[int]): The timeout in minutes for hang detection. Defaults to None.
        
        Returns:
            None: This method does not return anything.
        """
        self.enabled_hang_detection = enabled_hang_detection
        self.fault_tolerance_limit = fault_tolerance_limit
        self.hang_detection_timeout_minutes = hang_detection_timeout_minutes

    def to_dict(self) -> dict:
        """
            将对象转换为字典。
        
        Args:
            None
        
        Returns:
            dict (dict): 包含以下键值对的字典：
                - 'enabledHangDetection' (bool): 是否启用了挂起检测；
                - 'faultToleranceLimit' (int): 故障容错限制；
                - 'hangDetectionTimeoutMinutes' (int): 挂起检测超时时间（分钟）。
        
        Raises:
            None
        """
        return {
            'enabledHangDetection': self.enabled_hang_detection,
            'faultToleranceLimit': self.fault_tolerance_limit,
            'hangDetectionTimeoutMinutes': self.hang_detection_timeout_minutes
        }


class JobFramework(SerializableEnum):
    """分布式框架，分布式框架，本期只支持PyTorchJob"""
    MPI_JOB = "MPIJob"
    PY_TORCH_JOB = "PyTorchJob"


class Env:
    """环境变量，环境变量，包含名称和值"""
    name: Optional[str]
    value: Optional[str]

    def __init__(self, name: Optional[str], value: Optional[str]) -> None:
        """
            初始化Header对象。
        
        Args:
            name (Optional[str], optional): Header的名称，默认为None。可选参数。Defaults to None.
            value (Optional[str], optional): Header的值，默认为None。可选参数。Defaults to None.
        
        Returns:
            None: 无返回值，直接初始化Header对象。
        """
        self.name = name
        self.value = value


class ImageConfig:
    """镜像配置，配置镜像仓库及访问凭证，仅当私有仓库时需要配置"""
    """密码，镜像仓库密码"""
    password: str
    """用户名，镜像仓库用户名"""
    username: str

    def __init__(self, password: str, username: str) -> None:
        """
            初始化类实例，保存密码和用户名。
        
        Args:
            password (str): 登录密码。
            username (str): 用户名。
        
        Returns:
            None: 无返回值，只是初始化类实例。
        """
        self.password = password
        self.username = username

    def to_dict(self) -> dict:
        """
            将对象转换为字典，包含两个键值：'password'和'username'。
        返回值类型为dict，其中key是字符串，value是对应的属性值。
        
        Args:
            None
        
        Returns:
            dict (dict): 一个包含两个键值的字典，分别是'password'和'username'。
        """
        return {
            'password': self.password,
            'username': self.username
        }


class Resource:
    """资源名称，资源名称示例，支持设置GPU/CPU以及内存，枚举值：
    baidu.com/a800_80g_cgpu：gpu型号，需要根据型号按照百度的资源描述符填入，上述示例为A800的型号 cpu：cpu配额，单位核:
    memory：内存配额，单位GB
    """
    name: str
    """资源量，资源量"""
    quantity: float

    def __init__(self, name: str, quantity: float) -> None:
        """
            初始化一个 Ingredient 对象，用于表示食材的名称和数量。
        
        Args:
            name (str): 食材的名称。
            quantity (float): 食材的数量，单位为克（g）。
        
        Returns:
            None: 无返回值，创建了一个 Ingredient 对象。
        """
        self.name = name
        self.quantity = quantity


class JobSpec:
    """作业配置，作业配置"""
    """启动命令，启动命令"""
    command: str
    """开启RDMA，是否开启RDMA，默认false，开启后将自动添加NCCL_IB_DISABLE=0的环境变量，添加rdma/hca资源，并配置10GB共享内存到训练节点的容器中"""
    enable_rdma: Optional[bool]
    """环境变量，worker环境变量，默认注入:
    * AIHC_JOB_NAME ，值为name字段的值
    * NCCL_IB_DISABLE，开启rdma后默认注入，值为0
    * NCCL_DEBUG，nccl日志的级别，值为INFO
    """
    envs: Optional[List[Env]]
    """开启宿主机网络，是否使用宿主机网络，开启后作业worker将使用宿主机网络，"""
    host_network: Optional[str]
    """镜像，镜像包含tag"""
    image: str
    """镜像配置，配置镜像仓库及访问凭证，仅当私有仓库时需要配置"""
    image_config: ImageConfig
    """副本数，worker副本数"""
    replicas: int
    """资源，资源"""
    resources: Optional[List[Resource]]

    def __init__(self, command: str, enable_rdma: Optional[bool], envs: Optional[List[Env]], 
                host_network: Optional[str], image: str, image_config: Optional[ImageConfig], 
                replicas: int, resources: Optional[List[Resource]]) -> None:
        """
            初始化函数，用于设置参数。
        
        Args:
            command (str): 容器的命令行，默认为空字符串。
            enable_rdma (Optional[bool], optional): 是否启用RDMA，默认为None，表示不指定该值。
            envs (Optional[List[Env]], optional): 环境变量列表，默认为None，表示不指定该值。
            host_network (Optional[str], optional): 是否使用主机网络，默认为None，表示不指定该值。
            image (str): 镜像名称。
            image_config (Optional[ImageConfig], optional): 镜像配置，默认为None，表示不指定该值。
            replicas (int): 副本数量。
            resources (Optional[List[Resource]], optional): 资源列表，默认为None，表示不指定该值。
        
        Returns:
            None: 无返回值，所有参数都被保存在对象中。
        """
        self.command = command
        self.enable_rdma = enable_rdma
        self.envs = envs
        self.host_network = host_network
        self.image = image
        self.image_config = image_config
        self.replicas = replicas
        self.resources = resources


class Label:
    """标签名，标签名称"""
    key: str
    """标签值，标签值"""
    value: str

    def __init__(self, key: str, value: str) -> None:
        """
            初始化一个Header对象，用于存储HTTP请求或响应的头部信息。
        
        Args:
            key (str): 头部字段名称。
            value (str): 头部字段值。
        
        Returns:
            None: 不返回任何值，直接初始化一个Header对象。
        """
        self.key = key
        self.value = value
    
    def to_dict(self):
        """
            将对象转换为字典，包含键和值两个元素。
        返回值 (dict)：一个包含键和值两个元素的字典。
            - key (str)：键。
            - value (Any)：值，可以是任何类型。
        """
        return {'key': self.key, 'value': self.value}


class Priority(SerializableEnum):
    """优先级，调度优先级，支持高（high）、中（normal）、低（low）"""
    HIGH = "high"
    LOW = "low"
    NORMAL = "normal"


class Request:
    """数据源配置，配置数据源配置"""
    datasources: Optional[List[Datasource]]
    """容错，是否开启容错，需要安装 npd、nr、且 aibox 版本大于 1.6.10"""
    fault_tolerance: Optional[bool]
    fault_tolerance_config: Optional[FaultToleranceConfig]
    """分布式框架，分布式框架，本期只支持PyTorchJob"""
    job_framework: Optional[JobFramework]
    """作业配置，作业配置"""
    job_spec: JobSpec
    """标签，作业标签，默认包含：
    aijob.cce.baidubce.com/create-from-aihcp-api: "true"
    aijob.cce.baidubce.com/ai-user-id: {accoutId}
    aijob.cce.baidubce.com/ai-user-name: {userName}
    """
    labels: Optional[List[Label]]
    """作业名称，作业名称"""
    name: str
    """优先级，调度优先级，支持高（high）、中（normal）、低（low）"""
    priority: Optional[Priority]
    """作业队列，作业所属队列，默认为default"""
    queue: Optional[str]

    def __init__(self, datasources: Optional[List[Datasource]], fault_tolerance: Optional[bool], 
                fault_tolerance_config: Optional[FaultToleranceConfig], job_framework: Optional[JobFramework], 
                job_spec: JobSpec, labels: Optional[List[Label]], name: str, priority: Optional[Priority], 
                queue: Optional[str]) -> None:
        self.datasources = datasources
        self.fault_tolerance = fault_tolerance
        self.fault_tolerance_config = fault_tolerance_config
        self.job_framework = job_framework
        self.job_spec = job_spec
        self.labels = labels
        self.name = name
        self.priority = priority
        self.queue = queue

    def to_dict(self):
        """
            将对象转换为字典，包含所有属性和值。
        返回值 (dict)：一个包含所有属性和值的字典。如果属性是列表或对象，则会递归调用该方法。
        """
        return {
            'datasources': [ds.to_dict() for ds in self.datasources] if self.datasources else None,
            'faultTolerance': self.fault_tolerance,
            # 'faultToleranceConfig': self.fault_tolerance_config.to_dict() if self.fault_tolerance_config else None,
            'jobFramework': self.job_framework.to_dict() if self.job_framework else None,
            'jobSpec': {
                'command': self.job_spec.command,
                'enableRDMA': self.job_spec.enable_rdma,
                'envs': [env.__dict__ for env in self.job_spec.envs] if self.job_spec.envs else None,
                'hostNetwork': self.job_spec.host_network,
                'image': self.job_spec.image,
                'imageConfig': self.job_spec.image_config.to_dict() if self.job_spec.image_config else None,
                'replicas': self.job_spec.replicas,
                'resources': [resource.__dict__ for resource in self.job_spec.resources] 
                            if self.job_spec.resources else None,
            },
            'labels': [label.__dict__ for label in self.labels] if self.labels else None,
            'name': self.name,
            'priority': self.priority.to_dict() if self.priority else None,
            'queue': self.queue
        }
