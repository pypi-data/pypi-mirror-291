from attrs import field, frozen
from typing import Any
from abc import ABC
import numpy as np


@frozen
class IEntity(ABC):
    name: str


@frozen
class Circuit:
    entities: list[IEntity] = field()

    @entities.validator
    def check(self, attribute: Any, value: list[IEntity]):

        if len(value) == 0:
            raise ValueError("Need entities")


@frozen
class VoltageSource(IEntity):
    pos: str
    neg: str
    voltage: float


@frozen
class Resistor(IEntity):
    pos: str
    neg: str
    resistance: float


@frozen
class DCSweep:
    name: str
    source: str
    start: float
    stop: float
    step: float


@frozen
class ParameterSweep:
    pass


class DCSim:

    def __init__(self, dc: DCSweep, circuit: Circuit) -> None:
        self._sweep: DCSweep = dc
        self._entities: list[IEntity] = circuit.entities
        self._source: VoltageSource
        self._resistors: list[Resistor]
        self._totalResistance: float = 0

    def Run(self):
        self.Setup()

        for i in np.arange(self._sweep.start, self._sweep.stop, self._sweep.step):
            print(f"At {i}v:")
            current = self.CalcCurrent(i, self._totalResistance)
            print(f"  Current: {current}A")
            print(f"  Resistance: {self._totalResistance}")
            print(f"  Power: {round(self.CalcPower(i, current), 2)}W")
            voltageDrop = self.CalcVoltage(current, self._totalResistance)
            print(f"  Voltage drop: {voltageDrop}v\n")
        pass

    def CalcVoltage(self, current: float, resistance: float) -> float:
        return current * resistance

    def CalcCurrent(self, sourceVoltage: float, resistance: float) -> float:
        return sourceVoltage / resistance

    def CalcPower(self, sourceVoltage: float, current: float) -> float:
        return sourceVoltage * current

    def Setup(self):
        source = [x for x in self._entities if isinstance(x, VoltageSource)]

        if len(source) != 1:
            raise ValueError("")

        resistors = [x for x in self._entities if isinstance(x, Resistor)]

        if len(resistors) < 1:
            raise ValueError("")

        for resistor in resistors:
            self._totalResistance += resistor.resistance


r1 = Resistor("R1", "in", "out", 100)
voltageSource = VoltageSource("Input", "in", "out", 0)

circuit = Circuit([voltageSource, r1])
dc = DCSweep("dc", "Input", -5, 5, 1)

dcSim = DCSim(dc, circuit)
dcSim.Run()
