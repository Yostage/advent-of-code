import functools
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


@dataclass
# SerializedModule=Tuple[str, str, List[str]]
class SerializedModule:
    type: str
    name: str
    outputs: List[str]
    state: Dict[str, int] = field(default_factory=dict)
    inputs: List[str] = field(default_factory=list)


@dataclass
class SerializedPulse:
    source: str
    signal: int
    dest: str


# SerializedPulse = Tuple[str, int, str]


def parse_lines(lines: List[str]) -> Dict[str, SerializedModule]:
    ret: List[SerializedModule] = []
    for line in lines:
        (left, right) = line.split(" -> ")
        if left == "broadcaster":
            type = "broadcaster"
            name = "broadcaster"
        else:
            type = left[0]
            name = left[1:]
        outputs = right.split(", ")
        ret.append(SerializedModule(type=type, name=name, outputs=outputs))
    return {module.name: module for module in ret}


#     example = """broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a"""


def handle_pulse(
    pulse: SerializedPulse,
    modules: Dict[str, SerializedModule],
    pulse_queue: deque[SerializedPulse],
) -> None:
    module = modules[pulse.dest]

    if module.type == "button":
        for output in module.outputs:
            pulse_queue.append(SerializedPulse(module.name, 0, output))
    elif module.type == "broadcaster":
        for output in module.outputs:
            pulse_queue.append(SerializedPulse(module.name, 0, output))
    # flip-flop
    elif module.type == "%":
        # ignore high pulse
        if pulse.signal == 1:
            return
        current_state = module.state.get("state", 0)
        out_signal = 1 if current_state == 0 else 0
        new_state = 1 if current_state == 0 else 0
        module.state["state"] = new_state
        for output in module.outputs:
            pulse_queue.append(SerializedPulse(module.name, out_signal, output))
    # conjunction
    elif module.type == "&":
        # write memory
        module.state["memory_" + pulse.source] = pulse.signal
        # check memory
        source_memory = [
            module.state.get("memory_" + input, 0) for input in module.inputs
        ]
        out_signal = 0 if all(x == 1 for x in source_memory) else 1
        for output in module.outputs:
            pulse_queue.append(SerializedPulse(module.name, out_signal, output))
    elif module.type == "dummy":
        return
    else:
        raise ValueError(module.type)


def part_one(lines) -> int:
    def link_inputs():
        for module in list(modules.values()):
            for output in module.outputs:
                if output not in modules.keys():
                    modules[output] = SerializedModule(
                        type="dummy", name=output, outputs=[]
                    )
                modules[output].inputs.append(module.name)

    modules = parse_lines(lines)
    modules["button"] = SerializedModule(
        type="button", name="button", outputs=["broadcaster"]
    )

    # reverse link all the edges so conjunctions can know their state
    link_inputs()

    pulse_queue: deque[SerializedPulse] = deque()

    pulses = [0, 0]

    def pump_pulses():
        # the button has been pushed
        pulse_queue.append(SerializedPulse("button", 0, "broadcaster"))
        while len(pulse_queue) > 0:
            pulse = pulse_queue.popleft()
            # print(
            #     f"{pulse.source} -{'low' if pulse.signal == 0 else 'high'}--> {pulse.dest}"
            # )
            pulses[pulse.signal] += 1
            handle_pulse(pulse, modules, pulse_queue)

    for x in range(1000):
        pump_pulses()
    # print(f"After 1 push: {pulses}")
    # pump_pulses()
    print(f"After 1000 push: {pulses}")
    return pulses[0] * pulses[1]


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day20_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
