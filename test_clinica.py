import unittest
from datetime import datetime
from clinica import (
    clinica, paciente, medico, turno, receta, historiaclinica, 
    pacienteNoexisteError, medicoNoexisteError, turnoDuplicadoError
)

def test_agregar_pacientes_correctamente():
    """Test: Agregar pacientes correctamente"""
    print("Test: Agregar pacientes correctamente")
    clinica = clinica()
    paciente = paciente("123456789", "Marcos Arce", "15/03/2000")
    
    clinica.agregar_paciente(paciente)
    
    assert len(clinica.pacientes) == 1
    assert "123456789" in clinica.pacientes
    assert "123456789" in clinica.historias_clinicas
    print("✓ PASÓ")


def test_agregar_medicos_correctamente():
    """Test: Agregar médicos correctamente"""
    print("Test: Agregar médicos correctamente")
    clinica = clinica()
    medico = medico("MP001", "Dr. Augusto Salomón", "Kinesiologia")
    
    clinica.agregar_medico(medico)
    
    assert len(clinica.medicos) == 1
    assert "MP001" in clinica.medicos
    print("✓ PASÓ")


def test_agendar_turnos_validos():
    """Test: Agendar turnos válidos"""
    print("Test: Agendar turnos válidos")
    clinica = clinica()
    paciente = paciente("123456789", "Marcos Arce", "15/03/2000")
    medico = medico("MP001", "Dr. Augusto Salomón", "Kinesiologia")
    
    clinica.agregar_paciente(paciente)
    clinica.agregar_medico(medico)
    
    fecha_futura = datetime(2025, 12, 15, 10, 30)
    clinica.agendar_turno("123456789", "MP001", fecha_futura)
    
    assert len(clinica.turnos) == 1
    historia = clinica.obtener_historia_clinica("123456789")
    assert len(historia.obtener_turnos()) == 1
    print("✓ PASÓ")


def test_turnos_duplicados():
    """Test: Evitar turnos duplicados"""
    print("Test: Evitar turnos duplicados")
    clinica = clinica()
    paciente1 = paciente("123456789", "Marcos Arce", "15/03/2000")
    paciente2 = paciente("987654321", "Ana Quispe", "22/07/1985")  
    medico = medico("MP001", "Dr. Augusto Salomón", "Kinesiología")
    
    clinica.agregar_paciente(paciente1)
    clinica.agregar_paciente(paciente2)
    clinica.agregar_medico(medico)
    
    fecha_futura = datetime(2025, 12, 15, 10, 30)
    
    # Primer turno
    clinica.agendar_turno("123456789", "MP001", fecha_futura)
    
    # Segundo turno con mismo médico y hora (debe fallar)
    try:
        clinica.agendar_turno("87654321", "MP001", fecha_futura)
        assert False, "Debería haber lanzado TurnoDuplicadoError"
    except turnoDuplicadoError:
        print("✓ PASÓ")


def test_excepciones_paciente_no_existe():
    """Test: PacienteNoExisteError"""
    print("Test: PacienteNoExisteError")
    clinica = clinica()
    medico = medico("MP001", "Dr. Augusto Salomón", "Kinesiología")
    clinica.agregar_medico(medico)
    
    fecha_futura = datetime(2025, 12, 15, 10, 30)
    
    try:
        clinica.agendar_turno("99999999", "MP001", fecha_futura)
        assert False, "Debería haber lanzado PacienteNoExisteError"
    except pacienteNoexisteError:
        print("✓ PASÓ")


def test_excepciones_medico_no_existe():
    """Test: MedicoNoExisteError"""
    print("Test: MedicoNoExisteError")
    clinica = clinica()
    paciente = paciente("123456789", "Marcos Arce", "15/03/2000")
    clinica.agregar_paciente(paciente)
    
    fecha_futura = datetime(2025, 12, 15, 10, 30)
    
    try:
        clinica.agendar_turno("12345678", "MP999", fecha_futura)
        assert False, "Debería haber lanzado MedicoNoExisteError"
    except medicoNoexisteError:
        print("✓ PASÓ")


def test_emitir_recetas_validas():
    """Test: Emitir recetas válidas"""
    print("Test: Emitir recetas válidas")
    clinica = clinica()
    paciente = paciente("123456789", "Marcos Arce", "15/03/2000")
    medico = medico("MP001", "Dr. Augusto Salomón", "Kinesiología")
    
    clinica.agregar_paciente(paciente)
    clinica.agregar_medico(medico)
    
    medicamentos = ["Paracetamol", "Ibuprofeno"]
    clinica.emitir_receta("12345678", "MP001", medicamentos)
    
    historia = clinica.obtener_historia_clinica("12345678")
    assert len(historia.obtener_recetas()) == 1
    print("✓ PASÓ")


def test_emitir_receta_paciente_no_existe():
    """Test: Error al emitir receta - paciente no existe"""
    print("Test: Error al emitir receta - paciente no existe")
    clinica = clinica()
    medico = medico("MP001", "Dr. Carlos López", "Cardiología")
    clinica.agregar_medico(medico)
    
    medicamentos = ["Paracetamol"]
    
    try:
        clinica.emitir_receta("99999999", "MP001", medicamentos)
        assert False, "Debería haber lanzado PacienteNoExisteError"
    except pacienteNoexisteError:
        print("✓ PASÓ")


def test_emitir_receta_medico_no_existe():
    """Test: Error al emitir receta - médico no existe"""
    print("Test: Error al emitir receta - médico no existe")
    clinica = clinica()
    paciente = paciente("123456789", "Marcos Arce", "15/03/2000")
    clinica.agregar_paciente(paciente)
    
    medicamentos = ["Paracetamol"]
    
    try:
        clinica.emitir_receta("123456789", "MP999", medicamentos)
        assert False, "Debería haber lanzado MedicoNoExisteError"
    except medicoNoexisteError:
        print("✓ PASÓ")


def test_historia_clinica_completa():
    """Test: Historia clínica con turnos y recetas"""
    print("Test: Historia clínica con turnos y recetas")
    clinica = clinica()
    paciente = paciente("123456789", "Marcos Arce", "15/03/2000")
    medico = medico("MP001", "Dr. Augusto Salomón", "Kinesiología")
    
    clinica.agregar_paciente(paciente)
    clinica.agregar_medico(medico)
    
    # Agendar turno
    fecha_futura = datetime(2025, 12, 15, 10, 30)
    clinica.agendar_turno("12345678", "MP001", fecha_futura)
    
    # Emitir receta
    medicamentos = ["Paracetamol", "Ibuprofeno"]
    clinica.emitir_receta("123456789", "MP001", medicamentos)
    
    # Verificar historia clínica
    historia = clinica.obtener_historia_clinica("123456789")
    assert len(historia.obtener_turnos()) == 1
    assert len(historia.obtener_recetas()) == 1
    print("✓ PASÓ")


def ejecutar_tests():
    """Ejecutar todos los tests"""
    print("🧪 EJECUTANDO TESTS UNITARIOS")
    print("=" * 50)
    
    tests = [
        test_agregar_pacientes_correctamente,
        test_agregar_medicos_correctamente,
        test_agendar_turnos_validos,
        test_turnos_duplicados,
        test_excepciones_paciente_no_existe,
        test_excepciones_medico_no_existe,
        test_emitir_recetas_validas,
        test_emitir_receta_paciente_no_existe,
        test_emitir_receta_medico_no_existe,
        test_historia_clinica_completa
    ]
    
    tests_pasados = 0
    tests_fallidos = 0
    
    for test in tests:
        try:
            test()
            tests_pasados += 1
        except Exception as e:
            print(f"✗ FALLÓ: {e}")
            tests_fallidos += 1
    
    print("=" * 50)
    print(f"Tests ejecutados: {len(tests)}")
    print(f"✓ Pasaron: {tests_pasados}")
    print(f"✗ Fallaron: {tests_fallidos}")
    print("=" * 50)


if __name__ == "__main__":
    ejecutar_tests()


    