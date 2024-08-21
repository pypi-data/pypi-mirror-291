from collections import defaultdict
from dataclasses import dataclass
from itertools import zip_longest
from typing import Dict, Sequence, Union


@dataclass
class Block:
    name: str
    input_queue_names: Sequence[str]
    output_queue_names: Sequence[str]
    input_queues: Dict[str, Union[str, Sequence[str]]]
    output_queues: Dict[str, Union[str, Sequence[str]]]


class IndentationManager:
    def __init__(self, blocks: Sequence[Block]) -> None:
        # Identify input queues
        input_queues = {}
        self.queue_degree = defaultdict(lambda: 0)
        for block in blocks:
            for queue in block.input_queues.values():
                input_queues[queue] = None
                self.queue_degree[queue] += 1

        for block in blocks:
            for queue in block.output_queues.values():
                if queue in input_queues:
                    input_queues.pop(queue)

        # Populate initial queues
        self.queues = []
        self.queue_to_index = {}
        for queue in input_queues:
            self.queues.append(queue)
            self.queue_to_index[queue] = len(self.queues) - 1

    def connect(self, queue: str) -> str:
        index = self.queue_to_index[queue]
        indent = str(self)

        self.queue_degree[queue] -= 1
        if self.queue_degree[queue] == 0:
            self.queue_to_index.pop(queue)
            self.queues[index] = None
            char = "└"
        else:
            char = "├"

        return f"{indent[:index * 2]}{char}{'─' * (len(indent) - index * 2 - 1)}"

    def bind(self, queue: str) -> str:
        indent = str(self)

        try:
            index = self.queues.index(None)
        except ValueError:
            index = len(self.queues)
            self.queues.append(queue)
            self.queue_to_index[queue] = index
        else:
            self.queues[index] = queue
            self.queue_to_index[queue] = index

        return f"{indent[:index * 2]}┌{'─' * (len(indent) - index * 2)}"

    def __str__(self) -> str:
        return "".join(["  " if q is None else "│ " for q in self.queues])


corners = {
    "┌": "╭",
    "┐": "╮",
    "┘": "╯",
    "└": "╰",
}
def repr(blocks: Sequence[Block], rounded_corners: bool = True):
    # Run topological sort
    ...

    # Initialize indentation manager
    indent = IndentationManager(blocks)

    # Go
    lines = []
    for block in blocks:
        # text_width = len(block.name)
        # for in_q, out_q in zip_longest(
        #     block.input_queue_names, block.output_queue_names
        # ):
        #     if in_q is None:
        #         in_q = ""
        #     if out_q is None:
        #         out_q = ""
        #     text_width = max(text_width, len(in_q) + len(out_q) + 3)

        max_input_len = max([len(q) for q in block.input_queue_names], default=0)
        max_output_len = max([len(q) for q in block.output_queue_names], default=0)
        text_width = max(len(block.name), max_input_len + max_output_len + 2)
        # max

        if len(block.name) % 2 != text_width % 2:
            text_width += 1

        lines.append(f"{indent}┌──{'─' * text_width}──┐")
        padding = " " * ((text_width - len(block.name)) // 2)
        lines.append(f"{indent}│  {padding}{block.name}{padding}  │")
        lines.append(f"{indent}├──{'─' * text_width}──┤")
        outputs = []
        for in_q, out_q in zip_longest(
            block.input_queue_names, block.output_queue_names
        ):
            if in_q is None:
                in_q = ""
            if out_q is None:
                out_q = ""
            gap = " " * (text_width - len(in_q) - len(out_q))

            line_indent = indent
            if in_q:
                if in_q in block.input_queues:
                    line_indent = indent.connect(block.input_queues[in_q])
                    in_q = f"┼→ {in_q}"
                else:
                    in_q = f"│─ {in_q}"
            else:
                in_q = f"│  {in_q}"

            if out_q:
                if out_q in block.output_queues:
                    if indent.queue_degree[block.output_queues[out_q]] > 0:
                        spacing = "─" * (len(outputs) * 2 + 1)
                        outputs.append(out_q)
                        out_q = f"{out_q} ─┼{spacing}┐"
                    else:
                        spacing = "─" * (len(outputs) * 2)
                        out_q = f"{out_q} ─┼{spacing}→"
                else:
                    spacing = " │" * len(outputs)
                    out_q = f"{out_q} ─│{spacing}"
            else:
                spacing = " │" * len(outputs)
                out_q = f"{out_q}  │{spacing}"

            lines.append(f"{line_indent}{in_q}{gap}{out_q}")

        spacing = "│ " * len(outputs)
        lines.append(f"{indent}└──{'─' * text_width}──┘ {spacing}")

        for i, out_q in enumerate(outputs):
            line_indent = indent.bind(block.output_queues[out_q])
            # prefix = "│ " * i
            middle = "─" * (text_width + 6)
            suffix = " │" * (len(outputs) - i - 1)
            lines.append(f"{line_indent}{middle}┘{suffix}")

    output = "\n".join(lines)

    if rounded_corners:
        output = "".join([corners.get(c, c) for c in output])
    return output


"""
──┼──    
 ├─┬─┴─

│
┤
│
├
│
│

  ───┐   ┌───  
  ─┘  └──     



a
    b
    c

    d
"""

blocks = [
    Block(
        "CoblHDF5Reader",
        [],
        ["q_frame"],
        {},
        {
            "q_frame": "frame",
        },
    ),
    Block(
        "CoblCenterNet",
        ["q_frame"],
        ["q_decl", "q_img_tensor"],
        {"q_frame": "frame"},
        {
            "q_decl": "cnet_decl",
        },
    ),
    Block(
        "CoblResNet",
        ["q_frame", "q_decl", "q_oops"],
        ["q_decl"],
        {"q_frame": "frame", "q_decl": "cnet_decl"},
        {"q_decl": "resnet_decl"},
    ),
]


blocks = [
    Block(
        "CoblHDF5Reader",
        [],
        ["q_frame"],
        {},
        {
            "q_frame": "frame",
        },
    ),
    Block(
        "CoblCenterNet",
        ["q_frame"],
        ["q_decl", "q_img_tensor"],
        {"q_frame": "frame"},
        {
            "q_decl": "cnet_decl",
        },
    ),
    Block(
        "CoblDeepMTI",
        ["q_frame"],
        ["q_decl"],
        {"q_frame": "frame"},
        {
            "q_decl": "mti_decl",
        },
    ),
    Block(
        "CoblDeclFusion",
        ["q_decl1", "q_decl2"],
        ["q_fused_decl"],
        {"q_decl1": "cnet_decl", "q_decl2": "mti_decl"},
        {
            "q_fused_decl": "fused_decl",
        },
    ),
    Block(
        "CoblResNet",
        ["q_frame", "q_decl", "q_oops"],
        ["q_decl"],
        {"q_frame": "frame", "q_decl": "fused_decl"},
        {"q_decl": "resnet_decl"},
    ),
]

o = repr(blocks)
print(o)

