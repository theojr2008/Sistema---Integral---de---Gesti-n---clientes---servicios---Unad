from errores import ErrorValidacion


class Cliente:
    """
    representa a cada cliente del sistema
    """
    def __init__(self,nombre,email,telefono):
        self.verificar_nombre(nombre)
        self.verificar_email(email)
        self.verificar_telefono(telefono)


    def verificar_nombre(self,nombre):
        """
        verifica que el nombre sea correcta
        -no vacio y solo letras
        """

        if not nombre or not nombre.strip():
            raise ErrorValidacion(f"error en {self.__class__.__name__}:El nombre no puede estar vacío")

        if not nombre.replace(" ", "").isalpha():
            raise ErrorValidacion(f"error en {self.__class__.__name__}:El nombre solo debe contener letras")

        self._nombre = nombre



    def verificar_email(self,email):
        """
        verifica que el correo sea correcto.
        -solo se verifica que tenga @ y . para no extender el código
        """
        if not email or "@" not in email or "." not in email:
            raise ErrorValidacion(f"error en {self.__class__.__name__}:Email inválido, debe contener al menos un @ y .")
        self._email = email



    def verificar_telefono(self,telefono:str):
        """
        verifica que el número sea correcto
        -dígito de una longitud de 10
        """
        if not telefono.isdigit():
            raise ErrorValidacion(f"error en {self.__class__.__name__}:El teléfono debe contener solo números")

        if not len(telefono) == 10:
            raise ErrorValidacion(f"error en {self.__class__.__name__}:El teléfono debe ser de 10 dígitos")

        self._telefono = telefono



    """
    obtener los datos del cliente
    """
    def obtener_nombre(self):
        return self._nombre

    def obtener_email(self):
        return self._email

    def obtener_telefono(self):
        return self._telefono


    def descripcion(self):
        return f"Nombre:{self._nombre},  email:{self._email},   teléfono:{self._telefono}"
