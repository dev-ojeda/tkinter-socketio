class Usuario:
    # Datos de ejemplo para el inicio de sesión
    USUARIO_CORRECTO = "admin"
    CONTRASEÑA_CORRECTA = "1234"

    """docstring for ClassName."""

    def __init__(self):
        pass

    def Usuario(self, usuario, contraseña):
        self.__usuario = usuario
        self.__contraseña = contraseña

    @property
    def _usuario(self):
        return self.__usuario

    @_usuario.setter
    def _usuario(self, value):
        self.__usuario = value

    @property
    def _contraseña(self):
        return self.__contraseña

    @_contraseña.setter
    def _contraseña(self, value):
        self.__contraseña = value

    # Función para verificar el login y cambiar de ventana
    def verificar_login(self) -> bool:
        validar = False
        user = Usuario()
        usuario = self._usuario
        contraseña = self._contraseña

        if usuario == user.USUARIO_CORRECTO and contraseña == user.CONTRASEÑA_CORRECTA:
            validar = True
        else:
            validar = False

        return validar
