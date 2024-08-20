import argparse
import pandas as pd
from .configure import save_config
from .aihc_argumentparser import AIHCArgumentParser
from .resourcepool import list_resource_pool_pd, get_resource_pool
from .resourcepool_queue import list_queue_pd, get_queue
from .job import list_job_pd, create_job, stop_job, get_job_pd, get_job_logs, delete_job
from .utils import send_request, command_exists

AIHC_VERSION = '1.0.1'

def get_version():
    """打印版本信息"""
    return "aihc/v{}".format(AIHC_VERSION)


def get_parser():
    """获取命令行参数解析器"""
    # 创建 ArgumentParser 对象
    parser = AIHCArgumentParser()

    # 添加 subparsers 来处理不同的命令
    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommand to run')

    # 定义子命令
    # ======================================================== 通用命令 ==========================================================
    version_parser = subparsers.add_parser('version', help='Print version')
    help_parser = subparsers.add_parser('help', help='Print help')

    configure_parser = subparsers.add_parser('config', help='Configuration management')
    configure_parser.add_argument('--access_id', '--ak', action='store', required=False, help='Access Key ID')
    configure_parser.add_argument('--access_key', '--sk', action='store', required=False, help='Access Key Secret')
    configure_parser.add_argument('--region', action='store', required=False, help='Region ID')
    configure_parser.add_argument('--username', action='store', required=False, help='')
    configure_parser.add_argument('--password', action='store', required=False, help='')
    
    # ========================================================== Pool ==========================================================
    subparser_pool = subparsers.add_parser('pool', help='Pool management')
    pool_parser = subparser_pool.add_subparsers(dest='pool_subcommand')

    parser_pool_list = pool_parser.add_parser('list', help='List pools')
    parser_pool_list = pool_parser.add_parser('ls', help='List pools')

    parser_pool_get = pool_parser.add_parser('get', help='Get pool info')
    parser_pool_get.add_argument('pool_name', action='store', help='')
    
    # ========================================================== Queue ==========================================================
    subparser_queue = subparsers.add_parser('queue', help='Queue management')
    queue_parser = subparser_queue.add_subparsers(dest='queue_subcommand')

    parser_queue_list = queue_parser.add_parser('list', help='List queues')
    parser_queue_list.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')

    parser_queue_ls = queue_parser.add_parser('ls', help='List queues')
    parser_queue_ls.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')

    parser_queue_get = queue_parser.add_parser('get', help='Get queue info')
    parser_queue_get.add_argument('queue_name', action='store', help='')
    parser_queue_get.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')
    parser_queue_get.add_argument('--note', '-n', type=bool, default=False,
                                    required=False, action='store', dest='pool_name', help='')

    # ========================================================== Job ==========================================================
    subparser_job = subparsers.add_parser('job', help='Job management')
    job_parser = subparser_job.add_subparsers(dest='job_subcommand')

    parser_job_submit = job_parser.add_parser('submit', help='Create a job')
    parser_job_submit.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')
    parser_job_submit.add_argument('--queue', '-q', required=False, action='store', dest='queue', help='')
    parser_job_submit.add_argument('--name', '-n', type=str, required=True, action='store', dest='name', help='')
    parser_job_submit.add_argument('--framework', '-F', required=False, action='store', dest='framework', help='')
    parser_job_submit.add_argument('--image', '-i', required=True, action='store', dest='image', help='')
    parser_job_submit.add_argument('--username', required=False, action='store', dest='username', help='')
    parser_job_submit.add_argument('--pwd', required=False, action='store', dest='password', help='')
    parser_job_submit.add_argument('--command', '-c', required=False, action='store', dest='command', help='')
    parser_job_submit.add_argument('--script-file', required=False, action='store', dest='script', help='')
    parser_job_submit.add_argument('--env', '-e', nargs='*', required=False, action='store', dest='envs', help='')
    parser_job_submit.add_argument('--workers', '-w', type=int, required=False,
                                   default=1, action='store', dest='replicas', help='')
    parser_job_submit.add_argument('--gpu', '-g', type=int, required=False, action='store', dest='gpu', help='')
    parser_job_submit.add_argument('--cpu', type=float, required=False, action='store', dest='cpu', help='')
    parser_job_submit.add_argument('--memory', type=float, required=False, action='store', dest='memory', help='')
    parser_job_submit.add_argument('--rdma', '-r', type=bool, required=False,
                                   default=False, action='store', dest='rdma', help='')
    parser_job_submit.add_argument('--hostnetwork', type=bool, required=False,
                                   default=False, action='store', dest='hostnetwork', help='')
    parser_job_submit.add_argument('--data', '-d', required=False, action='store', dest='pfs_id', help='')
    parser_job_submit.add_argument('--data-dir', required=False, action='store',
                                   dest='mount_path', default='/mnt/cluster', help='')
    parser_job_submit.add_argument('--label', nargs='*', required=False, action='store', dest='labels', help='')
    parser_job_submit.add_argument('--priority', required=False, default='normal',
                                   action='store', dest='priority', help='')
    parser_job_submit.add_argument('--faulttolerance', type=bool, required=False,
                                   default=False, action='store', dest='faulttolerance', help='')
    parser_job_submit.add_argument('--hangdetection', type=bool, required=False,
                                   action='store', dest='hangdetection', help='')
    parser_job_submit.add_argument('--hangtimeout', type=int, required=False,
                                   action='store', dest='hangtimeout', help='')
    parser_job_submit.add_argument('--faulttolerancelimit', type=int, required=False,
                                   action='store', dest='faulttolerancelimit', help='')

    parser_job_list = job_parser.add_parser('list', help='List jobs')
    parser_job_list.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')
    parser_job_list.add_argument('--queue', '-q', required=False, action='store', dest='queue_name', help='')
    parser_job_list.add_argument('--framework', '-F', required=False, action='store', dest='framework', help='')

    parser_job_ls = job_parser.add_parser('ls', help='List jobs')
    parser_job_ls.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')
    parser_job_ls.add_argument('--queue', '-q', required=False, action='store', dest='queue_name', help='')
    parser_job_ls.add_argument('--framework', '-F', required=False, action='store', dest='framework', help='')

    parser_job_get = job_parser.add_parser('get', help='Get job info')
    parser_job_get.add_argument('job_name', action='store', help='')
    parser_job_get.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')
    parser_job_get.add_argument('--pods', type=bool, default=False, required=False, 
                                action='store', dest='pods', help='')

    patser_job_stop = job_parser.add_parser('stop', help='Stop job')
    patser_job_stop.add_argument('job_id', action='store', help='')
    patser_job_stop.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')

    parser_job_delete = job_parser.add_parser('delete', help='Delete job')
    parser_job_delete.add_argument('job_id', action='store', help='')
    parser_job_delete.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')

    subparser_logs = subparsers.add_parser('logs', help='Job logs management')
    subparser_logs.add_argument('job_name', action='store', help='')
    subparser_logs.add_argument('--pool', '-p', required=True, action='store', dest='pool_name', help='')
    subparser_logs.add_argument('--tail', '-t', type=int, default=10,
                                required=False, action='store', dest='tail', help='')
    subparser_logs.add_argument('--podname', required=False, action='store', dest='podname', help='')

    return parser


def main():
    """
    主函数，用于解析命令行参数并调用相应的功能。
    
    Args:
        无参数，程序会自动从命令行中读取参数。
    
    Returns:
        str: 如果是版本信息，则返回字符串形式的版本号；否则，不返回任何值。
    """
    parser = get_parser()

    # 解析命令行参数
    args = parser.parse_args()

    if args.subcommand == 'version':
        print(get_version())
    elif args.subcommand == 'config':
        print(save_config(args.access_id, args.access_key, args.region, args.username, args.password))
    elif args.subcommand == 'pool':
        if args.pool_subcommand == 'list' or args.pool_subcommand == 'ls':
            print(list_resource_pool_pd())
        elif args.pool_subcommand == 'get':
            print(get_resource_pool(args.pool_name))
        else:
            parser.print_pool_help()
    elif args.subcommand == 'queue':
        if args.queue_subcommand == 'list' or args.queue_subcommand == 'ls':
            print(list_queue_pd(args.pool_name))
        elif args.queue_subcommand == 'get':
            print(get_queue(args.pool_name, args.queue_name))
        else:
            parser.print_queue_help()
    elif args.subcommand == 'job':
        if args.job_subcommand == 'submit':
            if args.command == None and args.script == None:
                print("Please specify the command or script")
                return
            print(create_job(args))
        elif args.job_subcommand == 'list' or args.job_subcommand == 'ls':
            print(list_job_pd(args.pool_name, args.queue_name, args.framework))
        elif args.job_subcommand == 'get':
            print(get_job_pd(args.pool_name, args.job_name, args.pods))
        elif args.job_subcommand == 'stop':
            print(stop_job(args.job_id, args.pool_name))
        elif args.job_subcommand == 'delete':
            print(delete_job(args.job_id, args.pool_name))
        else:
            parser.print_job_help()
    elif args.subcommand == 'logs':
        print(get_job_logs(args.job_name, args.pool_name, args.tail, args.podname))
    else:
        parser.print_help()
