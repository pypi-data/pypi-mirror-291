from argparse import ArgumentParser
from sshc.tsvloader import ConfigLoader
from sshc.constants import USER_SSH_CFG, SSHC_TSV


class MainExecutor:
    @staticmethod
    def list(loader: ConfigLoader, args, other):
        keyword: str = other[0] if len(other) > 0 else None
        loader.print(keyword=keyword)

    @staticmethod
    def make(loader: ConfigLoader, args, other):
        loader.make(write=True)

    @staticmethod
    def edit(loader: ConfigLoader, args, other):
        target = None
        if args.open_sshc_tsv:
            target = SSHC_TSV
        elif args.open_ssh_config:
            target = USER_SSH_CFG
        if target:
            loader.open_in_editor(target)

    @staticmethod
    def add(loader: ConfigLoader, args, other):
        loader.add_item_interactive()
        loader.make(write=True)

    @staticmethod
    def remove(loader: ConfigLoader, args, other):
        if loader.remove_item(key=args.key):
            loader.make(write=True)

    @staticmethod
    def update(loader: ConfigLoader, args, other):
        if loader.update(key=args.key, col=args.col, val=args.val):
            loader.make(write=True)

    @staticmethod
    def clean(loader: ConfigLoader, args, other):
        loader.clean_all_backups()


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filepath", default=SSHC_TSV, help=f"default: {SSHC_TSV}")
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser("ps", aliases=("ls", "list"), help="打印所有主机信息(支持过滤)")
    subparser.set_defaults(func=MainExecutor.list)

    subparser = subparsers.add_parser("make", help="制作 ~/.ssh/config 文件")
    subparser.set_defaults(func=MainExecutor.make)

    subparser = subparsers.add_parser("edit", help="在默认文本编辑器中打开文件")
    subparser.add_argument("-t", "--sshc-tsv", dest="open_sshc_tsv", action="store_true", help="打开 sshc/sshc.tsv 文件")
    subparser.add_argument("-s", "--ssh-config", dest="open_ssh_config", action="store_true", help="打开 ssh/ssh_config 文件")
    subparser.set_defaults(func=MainExecutor.edit)

    subparser = subparsers.add_parser("add", aliases=("create", "new"), help="添加一个主机")
    subparser.set_defaults(func=MainExecutor.add)

    subparser = subparsers.add_parser("remove", aliases=("rm", "delete", "destroy"), help="删除一个主机")
    subparser.add_argument("key", help="要删除的主机键名")
    subparser.set_defaults(func=MainExecutor.remove)

    subparser = subparsers.add_parser("update", help="更新主机信息")
    subparser.add_argument("key", help="要更新的主机")
    subparser.add_argument("col", help="要更新的列")
    subparser.add_argument("val", help="要更新的值")
    subparser.set_defaults(func=MainExecutor.update)

    subparser = subparsers.add_parser("clean", help="清除所有备份文件")
    subparser.set_defaults(func=MainExecutor.clean)

    args, other = parser.parse_known_args()

    if hasattr(args, "func"):
        loader = ConfigLoader(args.filepath)
        args.func(loader, args, other)
    else:
        parser.print_help()
