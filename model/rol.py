class Rol:
    """docstring for Rol."""

    def __init__(self, rold_id, rol_nombre):

        self.__rold_id = rold_id
        self.__rol_nombre = rol_nombre

    @property
    def _rold_id(self):
        return self.__rold_id

    @_rold_id.setter
    def _rold_id(self, value):
        self.__rold_id = value

    @property
    def _rol_nombre(self):
        return self.__rol_nombre

    @_rol_nombre.setter
    def _rol_nombre(self, value):
        self.__rol_nombre = value
