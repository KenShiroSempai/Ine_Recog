from pydantic import BaseModel
from dataclasses import dataclass
from typing import List


class logEnramada(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    building: str
    floor: str
    conjunto: str
    idCArd: str
    face: str
    autorizo: str
    car: str
    origen: str
    guard: str


class deleteLog(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    building: str
    floor: str
    conjunto: str
    date: str
    time: str
    origen: str
    name: str
    motivo: str
    autorizo: str
    guardia: str


class logCarless(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """
    building: str
    floor: str
    conjunto: str
    idCArd: str
    face: str
    autorizo: str
    origen: str
    guard: str
    reason: str


class tagRange(BaseModel):
    """Rango de Tags

    Inicio y fin del loop
    """
    ini: int
    fin: int


@dataclass
class kibanaLog():
    """Estructura a usar en los log
    """
    origen: str
    conjunto: str
    building: str
    floor: str
    timestamp: str
    name: str
    autorizo: str
    idPath: str
    facePath: str
    plate: str
    make: str
    model: str
    color: str
    guardia: str
    tag: str
    preauth: str


class oneCar(BaseModel):
    plate: str
    place: str
    time: str
    img: str


class carList(BaseModel):
    data: List[oneCar]


class persona(BaseModel):
    persona: str
