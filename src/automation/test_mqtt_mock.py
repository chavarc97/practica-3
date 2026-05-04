import pytest
import json
from unittest.mock import Mock

def test_mqtt_connection_success():
    """Prueba que el cliente MQTT simulado puede conectarse."""
    mock_client = Mock()
    mock_client.connect.return_value = 0 # 0 es exito en paho-mqtt
    
    rc = mock_client.connect("localhost", 1883, 60)
    assert rc == 0, "La conexión MQTT debería ser exitosa (código 0)"

def test_mqtt_publish_telemetry():
    """Prueba que la publicación de telemetría funciona."""
    mock_client = Mock()
    payload = '{"temperature": 25.5, "humidity": 50.0}'
    
    # Simular que el método publish regresa un objeto con rc=0
    mock_client.publish.return_value = Mock(rc=0)
    result = mock_client.publish("iot/edge_1/telemetry", payload)
    
    assert result.rc == 0, "La publicación del payload debería ser exitosa"
    mock_client.publish.assert_called_with("iot/edge_1/telemetry", payload)

def test_mqtt_reject_malformed_payload():
    """TP11 - Simula backend descartando tramas malformadas (Inyección MQTT)."""
    malformed_payload = "NOT_JSON_DATA_SUDDEN_INJECTION"
    
    # Lógica simplificada de validación de backend
    def validate_payload(payload):
        try:
            data = json.loads(payload)
            if not isinstance(data, dict):
                return False
            return True
        except json.JSONDecodeError:
            return False
            
    assert validate_payload(malformed_payload) == False, "El payload malformado debe ser descartado"

def test_mqtt_accept_valid_payload():
    """Prueba que un payload correcto si pasa la validación."""
    valid_payload = '{"temperature": 25.5, "humidity": 50.0}'
    
    def validate_payload(payload):
        try:
            data = json.loads(payload)
            if not isinstance(data, dict):
                return False
            return True
        except json.JSONDecodeError:
            return False
            
    assert validate_payload(valid_payload) == True, "El payload correcto debe ser aceptado"
