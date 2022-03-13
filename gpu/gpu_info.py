from ansi2html import converter
from black import out
import gpustat
import ansi2html
import pynvml


class redirect:
    def __init__(self) -> None:
        self.content = ""

    def write(self, str):
        self.content += str

    def flush(self):
        pass
        # self.content = ""


converter = ansi2html.Ansi2HTMLConverter(    
    dark_bg=False,
    font_size="large",
)


def get_gpu_info():
    r = redirect()
    gpu_stats = gpustat.GPUStatCollection.new_query()
    gpu_stats.print_formatted(fp=r,force_color=True,show_power=True)
    output = converter.convert(r.content)
    output = output.replace("NVIDIA GeForce RTX 3090", "RTX3090")
    output = output.replace(
        '<span class="ansi1 ansi30">root</span>(<span class="ansi33">4M</span>)', ""
    )
    output=output.replace('gdm(4M)','')
    output=output.replace('root(4M)','')
    output = output.replace(".body_background { background-color: #AAAAAA; }", "")
    return output


def get_gpu_simple_info(number=-1):
    pynvml.nvmlInit()
    info = []
    if number != -1:
        handle = pynvml.nvmlDeviceGetHandleByIndex(number)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        used = int(meminfo.used / 1024 / 1024)
        total = int(meminfo.total / 1024 / 1024)
        return {
            "num": number,
            "used": used,
            "total": total,
            "text": f"G{number}: {used:>5d} MB / {total:>5d} MB".replace(" ", "&nbsp"),
        }
    else:
        return [get_gpu_simple_info(i) for i in range(pynvml.nvmlDeviceGetCount())]
