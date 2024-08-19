from astropy import time, coordinates
from typing_extensions import Annotated
import queue
import numpy as np
from typing import Union

from .dataclasses import autoconverted, Field

TimeType = autoconverted(time.Time)
TimeDeltaType = autoconverted(time.TimeDelta)
PortType = Annotated[int, Field(ge=0, lt=65535)]
QOSType = Annotated[int, Field(ge=0, le=2)]
EarthLocationType = autoconverted(coordinates.EarthLocation)
SkyCoordType = autoconverted(coordinates.SkyCoord)
QueueType = autoconverted(queue.Queue)

try:
    from typing import TypeAlias
except:
    TypeAlias = type

Vector: TypeAlias = Union[list[float], np.ndarray]
VectorOrScalar: TypeAlias = Union[float, list[float], np.ndarray]
