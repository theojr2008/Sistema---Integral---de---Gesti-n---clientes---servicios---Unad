from abc import ABC,abstractmethod
from errores import ErrorSistema
from errores import ErrorServicioNoDisponible
from errores import ErrorValidacion




class Servicio(ABC):
    """
    clase abstracta que representa a todos los servicios.
    """
    def __init__(self,nombre:str,precio_base):
        self._validar_nombre_servicio(nombre)
        self._precio_base = precio_base
        self._disponible = True




    def _validar_nombre_servicio(self,nombre):
        """
        decidí validar el nombre aparte porque es un método que todas las subclases usarán.
        no tiene que ser sobrescrito
        """
        if not nombre or not nombre.strip():
            raise ErrorValidacion(f"error en {self.__class__.__name__}:El nombre del servicio no puede estar vacío")

        self._nombre = nombre


    def validar_disponibilidad(self):
        """
        este método se usa antes de realizar cualquier acción en el servicio.  si el servicio no está dispoible lanza una excepción.
        """
        if not self._disponible:
            raise ErrorServicioNoDisponible(f"Error en {self.__class__.__name__}: Servicio no disponible")


    """
    habilitar e inhabilitar servicio. cuando un servicio está inhabilitado y se quiero procesar lanzará una excepción.
    """

    def activar(self):
        self._disponible = True

    def desactivar(self):
        self._disponible = False


    """
    estos últimos 3 métodos son abstractos, las subclases los deben implementar según lógica de cada servicio.
    recibe una cantidad indeterminada de argumentos para de algún modo cumplir con la sobrecarga de métodos.
    No creé un mismo método con diferente número y tipo de argumentos porque no todas las subclases los necesitan
    """
    @abstractmethod
    def calcular_costo(self, *argumentos,**argumentos_nombrados):
        pass


    @abstractmethod
    def validar_parametros(self,*argumentos,**argumentos_nombrados):
        pass


    """
    retorna un string que es la descripción del servicio. se usa cuando se quiere listar servicios en la consola
    """
    @abstractmethod
    def describir_servicio(self):
        pass






"""
las 3 implementaciones de Servicio
"""



class ServicioReservaSala(Servicio):
    """
    servicio para reservar salas para eventos u otras actividades. subclase de Servicio
    """
    def __init__(self, nombre,precio_por_hora = 50000):
        super().__init__(nombre, precio_por_hora)
        self._horas_reserva = 0
        self._descuento = 0





    """
    sobrescribo los 3 métodos de Servicio
    """

    def validar_parametros(self, horas):
        if horas <= 0:
          raise ErrorValidacion(f"Error en {self.__class__.__name__}: Las horas deben ser mayores a 0")

        self._horas_reserva = horas




    def calcular_costo(self, horas,descuento=0):
        """
        horas: horas de reserva de la sala
        descuento: valor del descuento. es un precio, NO porcentaje
        """
        self.validar_disponibilidad()
        self.validar_parametros(horas=horas)

        """
        lanza error si el descuento es negativo
        """
        if descuento < 0:
            raise ErrorValidacion(f"Error en {self.__class__.__name__}: El descuento no puede ser negativo")

        self._descuento = descuento

        costo = horas * self._precio_base
        return costo - self._descuento




    """
    si no se ha procesado el servicio, no mostrar el precio.
    """
    def describir_servicio(self):
        precio = None
        try:
            precio = self.calcular_costo(self._horas_reserva,self._descuento)
        except ErrorSistema:
            precio = "debe asignar el servicio a una reserva y luego procesarla para calcular el precio"

        return f"Servicio de sala: {self._nombre} por el precio de: ${precio}"




    """
    obtener datos del servicio
    """

    def obtener_valor_descuento(self):
        return self._descuento

    def obtener_horas_reservas(self):
        return self._horas_reserva









class ServicioAlquilerEquipo(Servicio):
    """
    servicio de alquiler de equipos, ya sean electrónicos o de cualquier tipo
    """
    def __init__(self, nombre,tipo_equipo,precio_por_dia = 80000):
        super().__init__(nombre, precio_por_dia)
        self._tipo_equipo = tipo_equipo
        self._dias = 0
        self._cantidad = 0
        self._impuestos = 0




    """
    sobrescribo los 3 métodos de Servicio
    """

    def validar_parametros(self, dias,cantidad):
        """
        valido que el número de días sea positivo y la cantidad de objetos esté entre 0 a 101, sin contar los extremos
        """
        if dias <= 0:
            raise ErrorValidacion(f" error en {self.__class__.__name__}:Los días deben ser mayores a 0")

        if cantidad <= 0 or cantidad > 100:
            raise ErrorValidacion(f"error en {self.__class__.__name__}: Cantidad inválida. solo puedes alquilar mínimo 1, máximo 100 el equipo {self._tipo_equipo} ")


        self._dias = dias
        self._cantidad = cantidad



    def calcular_costo(self,dias,cantidad,impuestos=0):
        """
        días: total de días de alquiler del equipo
        cantidad: total de equipos
        impuestos: porcentaje del impuesto
        """
        self.validar_disponibilidad()
        self.validar_parametros(dias=dias,cantidad=cantidad)

        """
        error si el impuesto es negativo. el impuesto es un número que representa el porcentaje.
        """
        if impuestos < 0 or impuestos > 100:
            raise ErrorValidacion(f"error en {self.__class__.__name__}: el porcentaje de impuestos debe estar entre 0 y 100")


        self._impuestos = impuestos

        costo = dias * cantidad * self._precio_base
        costo += costo * (impuestos/100)
        return costo



    def describir_servicio(self):
        precio = None
        try:
            precio = self.calcular_costo(self._dias,self._cantidad,impuestos=self._impuestos)
        except ErrorSistema:
            precio = "debe asignar el servicio a una reserva y luego procesarla para calcular el precio"

        return f"Alquiler de {self._cantidad} {self._tipo_equipo}(s) por {self._dias} días al precio de {precio}"




    """
    obtener datos del servicio
    """
    def obtener_dias_alquiler(self):
        return self._dias


    def obtener_cantidad(self):
        return self._cantidad


    def obtener_impuestos(self):
        return self._impuestos








class ServicioAsesoria(Servicio):
    """
    subclase de Servicio. en un servicio de un profesional que asesora en un campo en concreto
    """
    def __init__(self, nombre,especialidad,tarifa_por_hora = 60000):
        super().__init__(nombre, tarifa_por_hora)
        self._especialidad = especialidad
        self._horas = 0
        self._urgencia = False


    def validar_parametros(self, horas):
        """
        valida que el valor de las horas de asesoria no sea negativo
        """
        if horas <= 0:
            raise ErrorValidacion(f"error en {self.__class__.__name__}:Las horas deben ser mayores a 0")

        self._horas = horas



    def calcular_costo(self, horas, urgencia=False):
        """
        horas: horas de asesoria
        urgencia: True si es un servicio al cual se le tiene que dar prioridad
        """
        self.validar_disponibilidad()
        self.validar_parametros(horas)

        costo = horas * self._precio_base

        """
        simulo que le aumento 20% si es un servicio necesitado con urgencia , ya que tendría que
        asignar más recursos para ello.
        """
        if urgencia:
            costo *= 1.2

        self._urgencia = urgencia

        return costo




    def describir_servicio(self):

        precio = None
        try:
            precio = self.calcular_costo(self._horas,self._urgencia)
        except ErrorSistema:
            precio = "debe asignar el servicio a una reserva y luego procesarla para calcular el precio"

        return f"Asesoría en {self._especialidad} por {self._horas} horas al precio de {precio} "


    """
    obtener datos del servicio
    """

    def obtener_horas(self):
        return self._horas

    def obtener_urgencia(self):
        return self._urgencia
