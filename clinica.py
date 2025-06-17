from datetime import datetime 

#excepciones personalizadas
class pacienteNoexisteError(Exception):
    pass

class medicoNoexisteError(Exception):
    pass

class turnoDuplicadoError(Exception):
    pass


#Clases

#Paciente
class paciente:
    def __int__ (self, dni: str, nombre: str, fecha_nacimiento: str):
        self.dni = dni
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento

        def obtener_dni(self) -> str:
            return self.dni
        
        def __str__(self) -> str:
            return f"paciente: {self.nombre} (dni: {self._dni}) - nacimiento: {self.fecha_nacimiento}"

#Médico
class medico:
    def __init__ (self, matricula: str, nombre: str, especialidad: str):
        self.matricula = matricula
        self.nombre = nombre
        self.especialidad = especialidad

    def obtener_matricula(self) -> str:
        return self.matricula
    
    def __str__(self) -> str:
        return f"dr/a. {self.nombre} - matrícula: {self.matricula} - especialidad: {self.especialidad}"
    
#Turno
class turno:
    def __init__(self, paciente: paciente, medico: medico, fecha_hora: datetime):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora

    def obtener_fecha_hora(self) -> datetime:
        return self.fecha_hora
    
    def __str__(self) -> str:
        fecha_str = self.fecha_hora.strftime("%d/%m/%Y %H:%M")
        return f"Turno: {self.paciente.nombre} con {self.medico.nombre} el {fecha_str}"
    
#Receta
class receta:
    def __int__(self, paciente: paciente, medico: medico, medicamentos: list[str]):
        self.paciente = paciente
        self.medico = medico
        self.medicamentos = medicamentos
        self._fecha = datetime.now()
    
    def __str__(self) -> str:
        fecha_str = self._fecha.strftime("%d/%m/%Y")
        medicamentos_str = ", ".join(self.medicamentos)
        return f"Receta del {fecha_str} - Dr/a. {self.medico.nombre} para {self.paciente.nombre}: {medicamentos_str}"
    
#Historia clinica
class historiaclinica:
    def __int__(self, paciente: paciente):
        self.paciente = paciente
        self.turnos = []
        self.recetas = []

    def agregar_turno(self, turn: turno):
        self.turnos.append(turno)

    def agregar_receta(self, receta: receta):
        self.recetas.append(receta)

    def obtener_turnos(self) -> list[turno]:
        return self.turnos
    
    def obtener_recetas(self) -> list[receta]:
        return self.recetas
    
    def __str__(self) -> str:
        resultado = [f"Historia Clínica de {self.paciente.nombre} (DNI: {self.paciente.obtener_dni()})"]
        resultado.append("=" * 50)
        
        resultado.append("\nTURNOS:")
        if self.turnos:
            for turno in self.turnos:
                resultado.append(f"  - {turno}")
        else:
            resultado.append("  No hay turnos registrados.")
        
        resultado.append("\nRECETAS:")
        if self.recetas:
            for receta in self.recetas:
                resultado.append(f"  - {receta}")
        else:
            resultado.append("  No hay recetas registradas.")
        
        return "\n".join(resultado)
    
#Clinica
class clinica:
    def __int__(self):
        self.pacientes = {}
        self.medicos = {}
        self.turnos = []
        self.historias_clinicas = {}

    #agregar paciente
    def agregar_paciente(self, paciente: paciente):
        dni = paciente.obtener_dni()
        self.paciente[dni] = paciente
        self.historias_clinicas[dni] = historiaclinica(paciente)
    #agregar medico
    def agregar_medico(self, medico: medico):
        matricula = medico.obtener_matricula()
        self.medicos[matricula] = medico

    #crear turno
    def agendar_turno(self, dni:str, matricula: str, fecha_hora: datetime): 
        if dni not in self.paciente:
            raise pacienteNoexisteError (f"No existe un paciente con dni {dni}")
        
        if matricula not in self.medicos:
            raise medicoNoexisteError(f"No existe un médico con matrícula {matricula}")
        
        for turno in self.turnos:
            if (turno.medico.obtener_matricula() == matricula and 
                turno.obtener_fecha_hora() == fecha_hora):
                raise turnoDuplicadoError(f"Ya existe un turno con el médico {matricula} en {fecha_hora.strftime('%d/%m/%Y %H:%M')}")
        
        #no agendar turnos en el pasado    
        if fecha_hora < datetime.now():
            raise ValueError("No se pueden agendar turnos en el pasado")
        
    
        paciente = self.pacientes[dni]
        medico = self.medicos[matricula]
        turno = turno(paciente, medico, fecha_hora)

        self.turnos.append(turno)
        self.historias_clinicas[dni].agregar_turno(turno)

    #crear recetas
    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        if dni not in self.pacientes:
            raise pacienteNoexisteError(f"No existe un paciente con DNI {dni}")
        
        if matricula not in self.medicos:
            raise medicoNoexisteError(f"No existe un médico con matrícula {matricula}")
        
        paciente = self.pacientes[dni]
        medico = self.medicos[matricula]
        receta = receta(paciente, medico, medicamentos)
        
        # agregar la receta a la historia clínica
        self.historias_clinicas[dni].agregar_receta(receta)
    
    def obtener_historia_clinica(self, dni: str) -> historiaclinica:
        if dni not in self.historias_clinicas:
            raise pacienteNoexisteError(f"No existe un paciente con DNI {dni}")
        
        return self.historias_clinicas[dni]
    
    def obtener_turnos(self) -> list[turno]:
        return self.turnos


#CLI (Interfaz por Consola)
class CLI:
    def __init__(self):
        self.clinica = clinica()
    
    def mostrar_menu(self):
        print("\n" + "="*50)
        print("MENÚ CLÍNICA:")
        print("1. Agregar paciente")
        print("2. Agregar médico")
        print("3. Agendar turno")
        print("4. Emitir receta")
        print("5. Ver historia clínica")
        print("6. Ver todos los turnos")
        print("7. Ver todos los pacientes")
        print("8. Ver todos los médicos")
        print("9. Salir")
        print("="*50)
    
    def agregar_paciente(self):
        print("\n--- AGREGAR PACIENTE ---")
        dni = input("DNI: ")
        nombre = input("Nombre completo: ")
        fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
        
        paciente = paciente(dni, nombre, fecha_nacimiento)
        self.clinica.agregar_paciente(paciente)
        print(f"Paciente {nombre} agregado exitosamente.")
    
    def agregar_medico(self):
        print("\n--- AGREGAR MÉDICO ---")
        matricula = input("Matrícula: ")
        nombre = input("Nombre completo: ")
        especialidad = input("Especialidad: ")
        
        medico = medico(matricula, nombre, especialidad)
        self.clinica.agregar_medico(medico)
        print(f"Médico {nombre} agregado exitosamente.")
    
    def agendar_turno(self):
        print("\n--- AGENDAR TURNO ---")
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            fecha_str = input("Fecha y hora (dd/mm/aaaa HH:MM): ")
            
            fecha_hora = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            
            self.clinica.agendar_turno(dni, matricula, fecha_hora)
            print("Turno agendado exitosamente.")
            
        except (pacienteNoexisteError, medicoNoexisteError, turnoDuplicadoError) as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def emitir_receta(self):
        print("\n--- EMITIR RECETA ---")
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            medicamentos_str = input("Medicamentos (separados por coma): ")
            
            medicamentos = [med.strip() for med in medicamentos_str.split(",")]
            
            self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("Receta emitida exitosamente.")
            
        except (pacienteNoexisteError, medicoNoexisteError) as e:
            print(f"Error: {e}")
    
    def ver_historia_clinica(self):
        print("\n--- VER HISTORIA CLÍNICA ---")
        try:
            dni = input("DNI del paciente: ")
            historia = self.clinica.obtener_historia_clinica(dni)
            print(f"\n{historia}")
        except pacienteNoexisteError as e:
            print(f"Error: {e}")
    
    def ver_todos_turnos(self):
        print("\n--- TODOS LOS TURNOS ---")
        turnos = self.clinica.obtener_turnos()
        if not turnos:
            print("No hay turnos agendados.")
        else:
            for turno in turnos:
                print(turno)
    
    def ver_todos_pacientes(self):
        print("\n--- TODOS LOS PACIENTES ---")
        if not self.clinica.pacientes:
            print("No hay pacientes registrados.")
        else:
            for paciente in self.clinica.pacientes.values():
                print(paciente)
    
    def ver_todos_medicos(self):
        print("\n--- TODOS LOS MÉDICOS ---")
        if not self.clinica.medicos:
            print("No hay médicos registrados.")
        else:
            for medico in self.clinica.medicos.values():
                print(medico)
    
    def ejecutar(self):
        while True:
            try:
                self.mostrar_menu()
                opcion = input("\nSeleccione una opción (1-9): ")
                
                if opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.emitir_receta()
                elif opcion == "5":
                    self.ver_historia_clinica()
                elif opcion == "6":
                    self.ver_todos_turnos()
                elif opcion == "7":
                    self.ver_todos_pacientes()
                elif opcion == "8":
                    self.ver_todos_medicos()
                elif opcion == "9":
                    print("¡Hasta luego!")
                    break
                else:
                    print("Opción inválida. Elija una opción del 1 al 9.")
                
                input("\nPresione Enter para continuar...")
                
            except Exception as e:
                print(f"Error: {e}")


#Función principal
def main():
    cli = CLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()  