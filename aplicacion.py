from errores import ErrorSistema
from errores import ErrorServicioNoDisponible
from errores import ErrorValidacion
from servicios import Servicio
from servicios import ServicioReservaSala
from servicios import ServicioAsesoria
from servicios import ServicioAlquilerEquipo
from cliente import Cliente
from textos_aplicacion import RecursosTexto


"""
este archivo tiene la clase para hacer reservas, la aplicación por consola y un método que permite escribir logs de error
en el archivo "logs.txt"
"""


def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{mensaje}\n")




class Reserva:
    """
    maneja la reserva de un servicio a un cliente
    cliente: el cliente que va a realizar la reserva
    servicio: el servicio reservado
    estado: estado de la reserva. puede ser 'pendiente' (por defecto), 'confirmada' (cuando se procesa), 'cancelada' (cuando se procesa y luego se cancela) o 'fallida' (cuando se intentó procesar pero ocurrió un error)
    costo: cuando se procesa se calcula el precio de la reserva. en realidad el precio ya se podría saber pero lo hago para simular que el procesamiento calcula el precio
    """
    def __init__(self,cliente:Cliente,servicio:Servicio):
        self._cliente = cliente
        self._servicio = servicio
        self._estado = "pendiente"
        self._costo = 0


    def procesar(self, *argumentos,**argumentos_nombrados):
        """
        procesa la reserva. llama al método calcular_costo() de la implementación especifica del Servicio
        argumentos: lista de argumentos.
        argumentos_nombrados: diccionario de argumentos, son los que hay que poner el nombre del argumento y el valor
        nota: yo controlo la pasa de parámetros según la instancia de Servicio y los argumentos que pide su método calcular_costo()
        """
        try:
            self._costo = self._servicio.calcular_costo(*argumentos,**argumentos_nombrados)

        #registrar log en casa de error y cambiar estado de reserva
        except ErrorSistema as error:
            self._estado = "fallido"
            registrar_log(f"ERROR:{error}")
            raise

        else:
            self._estado = "confirmada"
            registrar_log(
                f"Reserva confirmada para {self._cliente.obtener_nombre()} - "
                f"{self._servicio.describir_servicio()} - Costo: {self._costo}"
            )


        finally:
            registrar_log("Intento de procesamiento de reserva finalizado\n")



    def cancelar(self):
        """
        cancelo la reserva. solo se pueden cancelar reservas previamente procesadas, de otro modo de lanza una excepción.
        """
        try:
            if self._estado != "confirmada":
                raise ErrorValidacion("No se puede cancelar una reserva no confirmada")

            self._estado = "cancelada"

        except ErrorSistema as e:
            registrar_log(f"ERROR al cancelar: {e}")
            raise

        else:
            registrar_log(
                f"Reserva cancelada para {self._cliente.obtener_nombre()}"
            )




    def mostrar(self):
        """
        usado cuando se quieren listar las reservas por consola
        """
        if self._estado != "confirmada":
            self._costo = "debe procesar la reserva para calcular el precio"


        return (
            f"Cliente: {self._cliente.descripcion()} | \n"
            f"Servicio: {self._servicio.describir_servicio()} | \n"
            f"Estado: {self._estado} | \n"
            f"Costo: {self._costo} \n"
        )



    """
    obtener datos de la reserva
    """

    def obtener_servicio(self):
        return self._servicio


    def obetener_costo(self):
        self._costo









class Aplicacion:
    """
    es la aplicación por consola que integra las reservas de servicios, los clientes y las reservas
    """


    def __init__(self,datos_iniciales = False):
        """
        datos_iniciales: True para cargar datos de prueba
        """
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas:list[Reserva] = []
        self._recursos_texto = RecursosTexto()
        self._datos_iniciales = datos_iniciales






    def _cargar_datos_iniciales(self):
        """
        carga datos iniciales en la aplicación. solo lo usa para pruebas
        """
        self._clientes.append(Cliente("clienteUno", "cliente1@gmail.com", "1111111111"))
        self._clientes.append(Cliente("clienteDos", "cliente2@gmail.com", "2222222222"))
        self._clientes.append(Cliente("clienteTres", "cliente3@gmail.com", "3333333333"))
        self._clientes.append(Cliente("clienteCuatro", "cliente4@gmail.com", "4444444444"))
        self._clientes.append(Cliente("clienteCinco", "cliente5@gmail.com", "5555555555"))

        servicio1 = ServicioAlquilerEquipo("alquiler de tecnología de última generación","Computador")
        servicio1.calcular_costo(2,10)

        servicio2 = ServicioAsesoria("servicio asesoría de software","crear sitio web")
        servicio2.calcular_costo(2,urgencia=True)

        servicio3 = ServicioReservaSala("reserva de instalaciones de recreación")
        servicio3.calcular_costo(2,descuento=10000)

        self._servicios.append(servicio1)
        self._servicios.append(servicio2)
        self._servicios.append(servicio3)


    def _pedir_opcion(self, mensaje="", opciones_validas=None, mensaje_error="Opción inválida"):
     """
     pedir una opción entre las dadas, si no se elije una de ellas informa por consola y registra el log en "logs.txt"
     mensaje: es el mensaje que sale por consola para pedirte el dato, ej: 'ingrese su edad:'
     opciones_validas: array de strings que contempla las opciones válidas, si pasas el array ['1','2'] y luego por consola escribes una diferente, entonces muestra un mensaje de error y vuelve a pedir el dato
     mensaje_error: mensaje que aparece cuando no se escribe por consola una de las opciones válidas. registra log y muestra en consola
     retorna: la opción elegida
     """

     if opciones_validas is None:
         opciones_validas = []

     while True:
         opcion = input(mensaje).strip()


         # validación
         if opciones_validas and opcion not in opciones_validas:
            print(f"{mensaje_error}\n")
            mensaje_error_log = mensaje_error.strip()
            registrar_log(f"error en {self.__class__.__name__}:{mensaje_error_log}")
            continue

         return opcion






    def _crear_servicio(self,tipo) -> Servicio:
        """
        método para crear un servicio por consola
        tipo: subclase de servicio que representa el servicio que quieres crear. es la clase NO una instancia
        retorna el servicio creado
        """

        servicio = None
        while True:

         try:

             nombre_servicio = input(self._recursos_texto.PEDIR_NOMBRE_SERVICIO)

             """
             tipo ==  ServicioReservaSala
             """
             if tipo == ServicioReservaSala:
                 horas_alquiler = int(input(self._recursos_texto.PEDIR_HORAS_RESERVA_SALA))


                 servicio = ServicioReservaSala(nombre_servicio)

                 mensaje_descuento = self._recursos_texto.obtener_mensaje_descuento_sala(servicio.calcular_costo(horas_alquiler))

                 descuento = int(input(mensaje_descuento))
                 costo = servicio.calcular_costo(horas_alquiler,descuento)

                 if costo < 0:
                     raise ErrorValidacion(f"""error en {self.__class__.__name__}:el valor del descuento no puede ser mayor al precio del servicio""")



                 return servicio




             elif tipo == ServicioAlquilerEquipo:
              """
               tipo == ServicioAlquilerEquipo:
              """
              tipo_equipo = input(self._recursos_texto.PEDIR_NOMBRE_EQUIPO_A_ALQUILAR)

              if not tipo_equipo or not tipo_equipo.strip():
                  raise ErrorValidacion(f"""error en {self.__class__.__name__}:el nombre del equipo a alquilar no pueda estar vacio""")

              servicio = ServicioAlquilerEquipo(nombre_servicio,tipo_equipo)

              cantidad_equipos = int(input(self._recursos_texto.PEDIR_CANTIDAD_EQUIPOS_A_ALQUILAR))

              dias_alquiler = int(input(self._recursos_texto.PEDIR_CANTIDAD_DIAS_ALQUILER))


              costo = servicio.calcular_costo(dias_alquiler,cantidad_equipos)

              impuestos = int(input(self._recursos_texto.PEDIR_PORCENTAJE_IMPUESTOS))


              servicio.calcular_costo(dias_alquiler,cantidad_equipos,impuestos=impuestos)
              return servicio


             elif tipo == ServicioAsesoria:
                 """
                 tipo == ServicioAsesoria
                 """
                 especialidad = input(self._recursos_texto.PEDIR_ESPECIALIDAD_ASESORIA)

                 if not especialidad or not especialidad.strip():
                  raise ErrorValidacion(f"""error en {self.__class__.__name__}:la especialidad del servicio de asesoría no puede estar vacio""")


                 horas = int(input(self._recursos_texto.PEDIR_HORAS_ASESORIA))

                 urgencia = self._pedir_opcion(
                     opciones_validas=["s","n","S","N"],
                     mensaje_error=self._recursos_texto.MENSAJE_ERROR_URGENCIA_SERVICIO_INVALIDA,
                     mensaje=self._recursos_texto.PEDIR_URGENCIA_SERVICIO)

                 urgencia = urgencia.lower() == "s"

                 servicio = ServicioAsesoria(nombre_servicio,especialidad)

                 servicio.calcular_costo(horas,urgencia)
                 return servicio


         except ErrorSistema as error:
             registrar_log(error)
             print(f"{error}")
             continue


         except ValueError as error:
             registrar_log(f"Error en {self.__class__.__name__} al crear servicio : valores como el impuesto, días, cantidad deben ser numéricos.")
             print("""\nError : debe ingresar valores numéricos válidos""")
             continue










    def iniciar(self):
        """
        punto de incio de la aplicación
        """

        if self._datos_iniciales:
            self._cargar_datos_iniciales()


        while (True):
            """
            bucle infinito que pide una opción y hace una tarea según la respuesta
            """

            accion = self._pedir_opcion(
                opciones_validas=["1","2","3","4","5","6","7","8","9","10","11"],
                mensaje_error=self._recursos_texto.MENSAJE_ERROR_OPCION_NO_VALIDA_MENU_INICIAL,
                mensaje= self._recursos_texto.MENSAJE_MENU_INICIAL)

            match accion:


                case "1":
                    """
                    crear cliente
                    """
                    while True:

                     """
                     pide los datos por consola y crea el objeto cliente.
                     al crear un cliente el mismo constructor de encarga de lanzar las excepciones pertinentes
                     """

                     nombre = input(self._recursos_texto.PEDIR_NOMBRE_CLIENTE)

                     telefono = input(self._recursos_texto.PEDIR_TELEFONO_CLIENTE)

                     email = input(self._recursos_texto.PEDIR_EMAIL_CLIENTE)

                     try:
                      cliente = Cliente(nombre,email,telefono)
                     except ErrorSistema as error:
                         registrar_log(error) #registrar log
                         print(f"""\n{error}""")
                         continue

                     else:
                         self._clientes.append(cliente)
                         print(self._recursos_texto.MENSAJE_CLIENTE_REGISTRADO)
                         break






                case "2":
                    """
                    crear servicio
                    """

                    """
                    usa el método que pide un dato hasta que se inserte una de las opciones válidas, en este caso ["1","2","3","4"]
                    """
                    tipo_servicio = self._pedir_opcion(
                        opciones_validas=["1","2","3","4"],
                        mensaje_error= self._recursos_texto.MENSAJE_ERROR_OPCION_SERVICIO_NO_VALIDA,
                        mensaje= self._recursos_texto.MENSAJE_OPCIONES_SERVICIO)

                    servicio = None

                    """"
                    dependiendo el número de teclado, creo un servicio de un tipo.
                    la opción 4 es para volver al menú principal
                    """

                    match tipo_servicio:
                        case "1":
                            servicio = self._crear_servicio(ServicioReservaSala)

                        case "2":
                            servicio = self._crear_servicio(ServicioAlquilerEquipo)


                        case "3":
                            servicio = self._crear_servicio(ServicioAsesoria)

                        case "4":
                            continue

                    #agrego el servicio a la lista
                    self._servicios.append(servicio)

                    print(self._recursos_texto.MENSAJE_SERVICIO_REGISTRADO)




                case "3":
                    """
                    listar los servicios registrados
                    """
                    print(self._recursos_texto.TITULO_LISTADO_SERVICIOS)


                    # si la lista está vacia muestro un mensaje
                    if not self._servicios:
                        print(self._recursos_texto.MENSAJE_LISTADO_SERVICIOS_VACIO)

                    # si hay elementos simplemento recorro la lista y escribo su descripción, quedaría como: 1. descripción
                    else:
                     for s in self._servicios:
                        print(f"""{self._servicios.index(s) + 1}. {s.describir_servicio()}""")




                case "4":
                    """
                    crear reserva
                    """

                    """
                    si no tengo clientes ni servicios inscritos muestro un mensaje avisando. para crear una reserva
                    debe existir al menor un servicio y un cliente que lo reserva
                    """

                    if not self._servicios or not self._clientes:
                        print(self._recursos_texto.MENSAJE_LISTADO_CLIENTES_SERVICIOS_VACIO_CREAR_RESERVA)


                    else:
                        """
                        si hay elementos entonces los listo para que el usuario elija
                        """

                        #indices que representan las opciones válidas al pedir dato por consola
                        indices_permitidos = []

                        print(self._recursos_texto.MENSAJE_SELECCION_CLIENTE)

                        # listo clientes y pido que elija uno para asignarle un servicio
                        for c in self._clientes:
                            indice = self._clientes.index(c) + 1
                            print(f"""{indice}. {c.descripcion()}""")
                            indice_str = str(indice)
                            indices_permitidos.append(indice_str)

                        indice_cliente = self._pedir_opcion(
                            opciones_validas=indices_permitidos,
                            mensaje_error=self._recursos_texto.MENSAJE_ERROR_SELECCIONAR_CLIENTE,
                            mensaje=self._recursos_texto.PEDIR_SELECCION_CLIENTE)






                        indices_permitidos = []


                        print(self._recursos_texto.MENSAJE_SELECCION_SERVICIO)

                        # listo servicios y pido la elección de uno para asignar a la reserva
                        for s in self._servicios:
                            indice = self._servicios.index(s) +1
                            print(f"""{indice}. {s.describir_servicio()}""") # aquí listo una reserva
                            indice_str = str(indice)
                            indices_permitidos.append(indice_str)


                        indice_servicio = self._pedir_opcion(
                            opciones_validas= indices_permitidos,
                            mensaje_error=RecursosTexto.MENSAJE_ERROR_SELECCION_SERVICIO,
                            mensaje=self._recursos_texto.PEDIR_SELECCION_SERVICIO)



                        try:
                          """
                          a este índice le resto 1 porque anteriormente lo sumé para mostrar valores de 1 en adelante
                          """
                          indice_cliente  = int(indice_cliente) - 1
                          indice_servicio= int(indice_servicio) -1

                          reserva = Reserva(cliente=self._clientes[indice_cliente],servicio=self._servicios[indice_servicio])
                          self._reservas.append(reserva)

                          print(self._recursos_texto.MENSAJE_RESERVA_REGISTRADA)

                        except ValueError as e:
                            """
                            este error nunca se lanza porque ya lo tengo previsto en _pedir_opcion(), de todas maneras atrapo la excepción.
                            """
                            registrar_log(f"""error en {self.__class__.__name__}:error al convertir un string a int""")
                            continue



                case "5":
                    """
                    procesar reserva
                    """

                    print(self._recursos_texto.TITULO_PROCESAMIENTO_RESERVA)


                    # muestro mensaje si no hay reservas
                    if not self._reservas:
                        print(self._recursos_texto.MENSAJE_LISTA_RESERVAS_VACIA)

                    # listo las reservas y pido que el usuario elija una opción
                    else:

                     indices_permitidos = []

                     for r in self._reservas:
                         indice = self._reservas.index(r) + 1

                         print(f"""{indice}. {r.mostrar()}""")
                         indice_str = str(indice)
                         indices_permitidos.append(indice_str)


                     indice_reserva = self._pedir_opcion(
                         opciones_validas=indices_permitidos,
                         mensaje_error=self._recursos_texto.MENSAJE_ERROR_SELECCION_RESERVA,
                         mensaje=self._recursos_texto.PEDIR_SELECCION_RESERVA)



                     try:
                         """
                         dependiendo la instancia del servicio de esta reserva, lo proceso
                         """
                         indice_reserva = int(indice_reserva) -1
                         reserva = self._reservas[indice_reserva]

                         servicio = reserva.obtener_servicio()

                         if isinstance(servicio,ServicioReservaSala):
                           reserva.procesar(servicio.obtener_horas_reservas(),descuento=servicio.obtener_valor_descuento())


                         elif isinstance(servicio,ServicioAlquilerEquipo):
                            reserva.procesar(servicio.obtener_dias_alquiler(),servicio.obtener_cantidad(),impuestos=servicio.obtener_impuestos())


                         elif isinstance(servicio,ServicioAsesoria):
                            reserva.procesar(servicio.obtener_horas(), urgencia=servicio.obtener_urgencia())


                         print(self._recursos_texto.MENSAJE_RESERVA_PROCESADA)


                     except ValueError as err:
                         print(self._recursos_texto.MENSAJE_ERROR_PROCESAR_RESERVA)

                     except ErrorSistema as err:
                          """
                          esta excepción es lanzada por el método procesar() de reserva cuando se quiere procesar una reserva que tiene un servicio inhabilitado
                          """
                          registrar_log(err)
                          print(f"""{err}.""")





                case "6":
                    """
                    cancelar reserva
                    """
                    print(self._recursos_texto.TITULO_CANCELACION_RESERVA)



                    if not self._reservas:
                        print(self._recursos_texto.MENSAJE_LISTA_RESERVAS_VACIA)


                    else:

                     indices_permitidos = []

                     for r in self._reservas:
                         indice = self._reservas.index(r) + 1
                         print(f"""{indice}. {r.mostrar()}""")
                         indice_str = str(indice)
                         indices_permitidos.append(indice_str)


                     indice_reserva = self._pedir_opcion(
                         opciones_validas=indices_permitidos,
                         mensaje_error=self._recursos_texto.MENSAJE_ERROR_SELECCION_RESERVA,
                         mensaje=self._recursos_texto.PEDIR_SELECCION_RESERVA_A_CANCELAR )


                     try:
                         indice_reserva = int(indice_reserva) -1
                         reserva = self._reservas[indice_reserva]

                         reserva.cancelar() # cancelar la reserva

                         print(self._recursos_texto.MENSAJE_RESERVA_CANCELADA)


                     except ValueError as err:
                         print(self._recursos_texto.MENSAJE_ERROR_CANCELAR_RESERVA)

                     except ErrorSistema as err:
                          registrar_log(err)
                          print(f"""{err}.""")




                case "7":
                    """
                    listar reservas
                    """

                    print(self._recursos_texto.TITULO_LISTADO_RESERVAS)

                    # mensaje en caso de que la lista esté vacia
                    if not self._reservas:
                        print(self._recursos_texto.MENSAJE_LISTA_RESERVAS_VACIA)

                    else:
                    # si tiene elementos la recorro y imprimo las reservas
                     for r in self._reservas:
                         indice = self._reservas.index(r) + 1

                         print(f"""\n{indice}. {r.mostrar()}""")




                case "8":
                    """
                    listar clientes
                    """

                    print(self._recursos_texto.TITULO_LISTADO_CLIENTES)

                    #mensaje en caso de lista vacia
                    if not self._clientes:
                        print(self._recursos_texto.MENSAJE_LISTADO_CLIENTES_VACIO)

                    # listar clientes si la lista tiene elementos
                    else:
                     for c in self._clientes:
                         indice = self._clientes.index(c) + 1

                         print(f"""\n{indice}. {c.descripcion()}""")



                case "9":
                     """
                     habilitar servicio
                     """
                     print(self._recursos_texto.TITULO_HABILITAR_SERVICIO)

                     # si no hay servicios, muestro mensaje
                     if not self._servicios:
                        print(self._recursos_texto.MENSAJE_LISTADO_SERVICIOS_VACIO)


                     else:
                      indices_permitidos = []


                      for s in self._servicios:
                        indice = self._servicios.index(s) +1

                        print(f"""{indice}. {s.describir_servicio()}""")
                        indice_str = str(indice)
                        indices_permitidos.append(indice_str)


                      indice_servicio = self._pedir_opcion(
                            opciones_validas= indices_permitidos,
                            mensaje_error=self._recursos_texto.MENSAJE_ERROR_SELECCION_SERVICIO,
                            mensaje=self._recursos_texto.PEDIR_SERVICIO_A_HABILITAR)



                      try:
                        indice_servicio= int(indice_servicio) -1


                        servicio = self._servicios[indice_servicio]
                        servicio.activar()

                        print(self._recursos_texto.MENSAJE_SERVICIO_HABILITADO)

                      except ValueError as e:
                        registrar_log(f"""error en {self.__class__.__name__}:error al convertir un string a int""")
                        continue






                case "10":
                    """
                    deshabilitar servicio
                    """
                    print(self._recursos_texto.TITULO_DESHABILITAR_SERVICIO)

                    #mensaje en caso de lista vacia
                    if not self._servicios:
                        print(self._recursos_texto.MENSAJE_LISTADO_SERVICIOS_VACIO)



                    else:

                     indices_permitidos = []

                     # si hay elementos en la lista los muestro y pido al usuario que elija
                     for s in self._servicios:
                        indice = self._servicios.index(s) +1

                        print(f"""{indice}. {s.describir_servicio()}""")
                        indice_str = str(indice)
                        indices_permitidos.append(indice_str)


                     indice_servicio = self._pedir_opcion(
                            opciones_validas= indices_permitidos,
                            mensaje_error=self._recursos_texto.MENSAJE_ERROR_SELECCION_SERVICIO,
                            mensaje=self._recursos_texto.PEDIR_SERVICIO_A_DESHABILITAR)



                     try:
                        indice_servicio= int(indice_servicio) -1

                        servicio = self._servicios[indice_servicio]
                        servicio.desactivar()

                        print(self._recursos_texto.MENSAJE_SERVICIO_DESHABILITADO)

                     except ValueError as e:
                        registrar_log(f"""error en {self.__class__.__name__}:error al convertir un string a int""")
                        continue



                case "11":
                    exit()
