from pydantic import BaseModel


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


class Item(BaseModel):
    """Objeto a recivir en el apartado de QR.

    Se hizo una clase en para que en un futuro, si se quieren aumentar los
    parametros sea mas sencillo.
    """

    url: str    # String del cual se va a generar el QR

class tagRange(BaseModel):
    """
    """
    ini : int
    fin : int
