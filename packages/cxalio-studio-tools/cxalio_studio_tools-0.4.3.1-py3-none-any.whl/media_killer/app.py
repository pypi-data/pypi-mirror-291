from cx_core.app import AbstractApp, LogLevel
from cx_core.misc import DataPackage
from argparse import ArgumentParser

from rich.markdown import Markdown
from rich.panel import Panel
from rich_argparse import RichHelpFormatter
from pathlib import Path
from .env import env

from .profile_loader import ProfileLoader
from .source_detector import SourceDetector

from .exceptions import *
import pkgutil
from cx_core.filesystem.path_utils import *
from .mission_maker import MissionMaker
from .script_writer import ScriptWriter
from .transcoder import Transcoder
from cx_core.tui import JobCounter
from ffmpeg import FFmpegError

class MediaKillerApp(AbstractApp):
    APP_VERSION = "0.4.3"
    APP_NAME = "mediakiller"

    def __init__(self):
        super(MediaKillerApp, self).__init__()

        _parser = ArgumentParser(
            prog=MediaKillerApp.APP_NAME,
            formatter_class=RichHelpFormatter,
            description="批量转码工具",
            epilog=f"Version {MediaKillerApp.APP_VERSION} Designed by xiii_1991",
        )

        _parser.add_argument(
            "sources",
            help="指定需要处理的文件，其中必须包含至少一个配置文件",
            default=None,
            metavar="需要处理的路径",
            nargs="*",
        )
        _parser.add_argument(
            "-g",
            "--generate",
            action="store_true",
            dest="generate_example",
            help="生成范例配置文件",
        )
        _parser.add_argument(
            "-s",
            "--make-script",
            dest="script_output",
            metavar="脚本文件路径",
            help="生成对应的脚本文件",
        )
        _parser.add_argument(
            "-o",
            "--output",
            dest="output_dir",
            metavar="输出位置",
            help="指定输出目录",
            default=".",
        )
        _parser.add_argument(
            '-c',
            '--continue',
            dest='continue_mode',
            action='store_true',
            help='继续未完成的任务'
        )
        _parser.add_argument(
            "--pretend",
            "-p",
            dest="pretend_mode",
            action="store_true",
            help="空转模式，模拟执行",
        )
        _parser.add_argument(
            "-d", "--debug", action="store_true", dest="debug", help="显示调试信息"
        )
        _parser.add_argument(
            "--full-help", help="显示详细的说明", dest="full_help", action="store_true"
        )
        _parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=MediaKillerApp.APP_VERSION,
            help="显示软件版本信息",
        )

        self.parser = _parser
        self.profile = None
        self.args = None
        self.global_task = None

    def __enter__(self):
        env.start()
        env.print(
            f"[yellow]{MediaKillerApp.APP_NAME}[/yellow] [blue]{MediaKillerApp.APP_VERSION}[/blue]"
        )

        _args = self.parser.parse_args()
        self.args = DataPackage(**vars(_args))
        env.log_level = LogLevel.DEBUG if self.args.debug else LogLevel.WARNING
        env.debug("解析命令行参数：", self.args)

        self.global_task = env.progress.add_task("全局进度", start=False, visible=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.stop_task(self.global_task)
        env.progress.remove_task(self.global_task)
        self.global_task = None

        result = False
        if exc_type is None:
            pass
        elif issubclass(exc_type, CxException):
            env.error(exc_val)
            result = True

        env.stop()
        return result

    @staticmethod
    def copy_example_profile(to):
        to = normalize_path(to)
        to = force_suffix(to, ".toml")
        data = pkgutil.get_data("media_killer", "example_project.toml")
        try:
            with open(to, "xb") as file:
                file.write(data)
            env.print(f"配置文件{to.name}已初始化，[red]请在修改后运行[/red]")
        except FileExistsError:
            env.error(
                f"文件 [yellow]{to.name}[/yellow] 已存在，请手动删除或指定其它目标文件"
            )

    @staticmethod
    def show_full_help():
        data = pkgutil.get_data("media_killer", "help.md").decode("utf_8")
        panel = Panel(Markdown(data), width=80)
        env.console.print(panel)

    def run(self):
        if self.args.full_help:
            env.info("检测到full_help，打印帮助文件并输出")
            MediaKillerApp.show_full_help()
            return

        if not self.args.sources:
            env.info("指定的路径为空")
            raise NoSourcesError("未指定任何文件，你想做什么？")

        if self.args.generate_example:
            MediaKillerApp.copy_example_profile(self.args.sources[0])
            return

        env.progress.update(self.global_task, visible=True, total=None)

        env.progress.update(self.global_task, description="正在检测配置文件…")
        profiles = []
        pro_files = list(filter(lambda x: Path(x).suffix == ".toml", self.args.sources))
        env.print(f"发现[cyan]{len(pro_files)}[/cyan]个配置文件")
        for a in pro_files:
            with ProfileLoader(a, self.args) as loader:
                profiles.append(loader.load())
        if len(profiles) == 0:
            raise NoProfileError("没有指定配置文件，无法执行任务")

        env.progress.update(self.global_task, description="正在探测源文件…")
        sources = set(filter(lambda x: Path(x).suffix != ".toml", self.args.sources))
        env.print(f"开始探测[cyan]{len(sources)}[/cyan]个来源路径")
        with SourceDetector(self.args) as source_detector:
            for s in sources:
                source_detector.detect(s)
            total_sources = source_detector.arrange_tasks()

        env.debug("解析的文件列表：", total_sources)

        env.progress.update(self.global_task, description="正在制定计划…")
        missions = []
        env.progress.update(
            self.global_task, completed=0, total=len(total_sources) * len(profiles)
        )
        for profile in profiles:
            for source in total_sources:
                maker = MissionMaker(source, profile)
                mission = maker.make()
                missions.append(mission)
                env.progress.advance(self.global_task)

        env.progress.update(self.global_task, description="正在为任务列表排序…")
        missions = sorted(missions, key=lambda x: x.source)

        mission_count = len(missions)
        env.print(
            f"为 [blue]{len(profiles)}[/blue] 个配置文件生成了 [blue]{mission_count}[/blue] 个任务"
        )
        env.progress.start_task(self.global_task)
        env.progress.update(self.global_task,completed=0,total=mission_count)

        if self.args.pretend_mode:
            env.print("启用了干转模式，将会假装执行")
            for m in missions:
                cmd = ScriptWriter.compile_cmd(m)
                env.debug(f"[grey]假装执行：[/grey] {cmd}")
                env.print(f'[grey]假装生成了：[blue]{' '.join([str(x.filename) for x in m.outputs])}[/blue][/grey]')
                env.progress.advance(self.global_task)
            return

        if self.args.script_output:
            env.progress.update(self.global_task, description="正在输出脚本文件…")
            script_target = Path(self.args.script_output)
            env.print(
                f"指定了脚本目标[cyan]{script_target.name}[/cyan]，将会生成脚本文件"
            )
            with ScriptWriter(script_target) as writer:
                writer.write_all(missions)
        else:
            if self.args.continue_mode:
                env.progress.update(self.global_task,description='检查以跳过已完成的任务…')
                missions = [m for m in missions if not all([x.exists() for x in m.iter_output_filenames()])]
                env.print(f'已跳过[red]{mission_count - len(missions)}[/red]项已完成的任务')
                mission_count = len(missions)

            job_counter = JobCounter(mission_count)
            env.progress.update(
                self.global_task,
                description="总体进度",
            )

            for m in missions:
                if env.wanna_quit:
                    env.print("取消未完成的任务…")
                    raise UserCanceledError("用户取消了执行")
                skipped = False
                try:
                    with Transcoder(m) as coder:
                        coder.run()
                except FFmpegError as e:
                    env.error(f'FFMPEG运行出错 ：[red]{e.message}[/red]')
                    skipped = True

                job_counter.advance()
                env.progress.update(
                    self.global_task,
                    completed=job_counter.current,
                    total=job_counter.total,
                )
                if skipped:
                    env.print(
                        f"[yellow]{job_counter}[/yellow] [red]{mission.source.name}[/red] 未正确执行"
                    )
                else:
                    env.print(
                        f"[yellow]{job_counter}[/yellow] [cyan]{mission.source.name}[/cyan] 执行完毕"
                    )


def run():
    with MediaKillerApp() as media_killer:
        media_killer.run()
