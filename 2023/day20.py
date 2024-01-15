import functools
import math
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
    generation: int = 0,
) -> None:
    module = modules[pulse.dest]

    press_key = str(pulse.signal)
    module.state[press_key] = module.state.get(press_key, 0) + 1
    module.state["last_input"] = pulse.signal

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
        module.state["last_output"] = out_signal
        module.state["flips"] = module.state.get("flips", 0) + 1
        module.state["flipflop_change"] = 1
        module.state["output_" + str(out_signal)] = (
            module.state.get("output_" + str(out_signal), 0) + 1
        )
        for output in module.outputs:
            pulse_queue.append(SerializedPulse(module.name, out_signal, output))
    # conjunction
    elif module.type == "&":
        # write memory
        memory_key = "memory_" + pulse.source
        module.state[memory_key] = pulse.signal
        if pulse.signal == 1:
            memory_last = memory_key + "_last"
            if memory_last in module.state:
                module.state[memory_key + "_delta"] = (
                    generation - module.state[memory_last]
                )
            else:
                module.state[memory_key + "_first"] = generation
            module.state[memory_last] = generation

        # check memory
        source_memory = [
            module.state.get("memory_" + input, 0) for input in module.inputs
        ]
        out_signal = 0 if all(x == 1 for x in source_memory) else 1
        module.state["last_output"] = out_signal
        module.state["output_" + str(out_signal)] = (
            module.state.get("output_" + str(out_signal), 0) + 1
        )
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
        # clear everyody's stuff
        for key in ["last_output", "flipflop_change"]:
            for module in modules.values():
                module.state.pop(key, None)

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

    # dump the graph
    # for module in modules.values():
    #     for output in module.outputs:
    #         print(f"{module.name} --> {output}")

    # return

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
            handle_pulse(pulse, modules, pulse_queue, generation=presses + 1)

    presses = 0
    while True:
        pump_pulses()
        presses += 1
        if modules["rx"].state.get("0", 0) > 0:
            return presses

        for module in [
            # this one comes from rx
            "zr",
            # inputs 3 up from zr
            "gc",
            "sz",
            "cm",
            "xf",
            # the other one
            # rh -> ks -> cm
            # "rh",
            # "zz",
            "ks",
            # tc -> mn -> xs -> zr
            # "tc",
            # "mn",
            # "ks",
        ]:
            # if modules[module].state["last_output"] == 0:
            if modules[module].type == "%":
                if (
                    modules[module].state.get("output_1", 0) < 100
                    and modules[module].state.get("last_output") == 1
                    and "flipflop_change" in modules[module].state
                ):
                    print(f"\t{presses} %{module} flips high")
                    print(module + ": " + str(modules[module].state))
            elif modules[module].type == "&":
                if (
                    modules[module].state.get("output_0", 0) < 5
                    and modules[module].state.get("last_output") == 0
                ):
                    print(f"\t{presses} &{module} emits low")
                    print(module + ": " + str(modules[module].state))

        if presses % 10000 == 0:
            print(f"Press {presses}")
            print(f"rx: {modules['rx'].state}")
            print(f"zr: {modules['zr'].state}")
            firsts = [v for k, v in modules["zr"].state.items() if k.endswith("_first")]
            if len(firsts) == 4:
                return math.lcm(*firsts)


def main() -> None:
    with open("day20_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
