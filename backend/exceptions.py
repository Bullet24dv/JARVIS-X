"""
JARVIS-X - Excepciones personalizadas
Sistema de manejo de errores empresarial
"""

from typing import Optional, Any, Dict


class JARVISException(Exception):
    """Excepción base para JARVIS-X"""
    
    def __init__(self, message: str, code: str = "JARVIS_ERROR", details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la excepción a diccionario para respuestas API"""
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details
        }


class ConfigurationError(JARVISException):
    """Error de configuración (variables de entorno faltantes, etc.)"""
    
    def __init__(self, message: str, missing_key: Optional[str] = None):
        super().__init__(
            message=message,
            code="CONFIG_ERROR",
            details={"missing_key": missing_key} if missing_key else {}
        )


class LLMProviderError(JARVISException):
    """Error en proveedor de LLM (DeepSeek, OpenAI, etc.)"""
    
    def __init__(self, provider: str, original_error: str):
        super().__init__(
            message=f"Error en proveedor {provider}: {original_error}",
            code="LLM_PROVIDER_ERROR",
            details={"provider": provider, "original_error": original_error}
        )


class AllLLMProvidersFailedError(JARVISException):
    """Todos los proveedores de LLM fallaron"""
    
    def __init__(self, errors: Dict[str, str]):
        self.errors = errors
        super().__init__(
            message="Todos los proveedores de LLM fallaron",
            code="ALL_LLM_FAILED",
            details={"errors": errors}
        )


class VoiceProcessingError(JARVISException):
    """Error en procesamiento de voz (STT/TTS)"""
    
    def __init__(self, component: str, reason: str):
        super().__init__(
            message=f"Error en {component}: {reason}",
            code="VOICE_ERROR",
            details={"component": component, "reason": reason}
        )


class WakeWordDetectionError(JARVISException):
    """Error en detección de palabra de activación"""
    
    def __init__(self, reason: str):
        super().__init__(
            message=f"Error detectando palabra de activación: {reason}",
            code="WAKE_WORD_ERROR",
            details={"reason": reason}
        )


class VisionProcessingError(JARVISException):
    """Error en procesamiento de visión (OCR, detección, etc.)"""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            message=f"Error en operación de visión '{operation}': {reason}",
            code="VISION_ERROR",
            details={"operation": operation, "reason": reason}
        )


class ScreenCaptureError(JARVISException):
    """Error capturando pantalla"""
    
    def __init__(self, reason: str):
        super().__init__(
            message=f"Error capturando pantalla: {reason}",
            code="SCREEN_CAPTURE_ERROR",
            details={"reason": reason}
        )


class ComputerControlError(JARVISException):
    """Error controlando el ordenador"""
    
    def __init__(self, action: str, reason: str):
        super().__init__(
            message=f"Error ejecutando '{action}': {reason}",
            code="COMPUTER_CONTROL_ERROR",
            details={"action": action, "reason": reason}
        )


class MCPServiceError(JARVISException):
    """Error en servicio MCP (Model Context Protocol)"""
    
    def __init__(self, connector: str, operation: str, reason: str):
        super().__init__(
            message=f"Error en MCP connector '{connector}.{operation}': {reason}",
            code="MCP_ERROR",
            details={"connector": connector, "operation": operation, "reason": reason}
        )


class MCPConnectorNotFoundError(JARVISException):
    """Conector MCP no encontrado"""
    
    def __init__(self, connector_name: str):
        super().__init__(
            message=f"Conector MCP '{connector_name}' no encontrado",
            code="MCP_CONNECTOR_NOT_FOUND",
            details={"connector": connector_name}
        )


class AgentError(JARVISException):
    """Error en ejecución de agente"""
    
    def __init__(self, agent_name: str, action: str, reason: str):
        super().__init__(
            message=f"Error en agente '{agent_name}' acción '{action}': {reason}",
            code="AGENT_ERROR",
            details={"agent": agent_name, "action": action, "reason": reason}
        )


class AgentNotFoundError(JARVISException):
    """Agente no encontrado"""
    
    def __init__(self, agent_name: str):
        super().__init__(
            message=f"Agente '{agent_name}' no encontrado",
            code="AGENT_NOT_FOUND",
            details={"agent": agent_name}
        )


class MemoryError(JARVISException):
    """Error en sistema de memoria"""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            message=f"Error en memoria '{operation}': {reason}",
            code="MEMORY_ERROR",
            details={"operation": operation, "reason": reason}
        )


class DatabaseError(JARVISException):
    """Error en base de datos"""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            message=f"Error en base de datos '{operation}': {reason}",
            code="DATABASE_ERROR",
            details={"operation": operation, "reason": reason}
        )


class SecurityError(JARVISException):
    """Error de seguridad (autenticación, permisos, etc.)"""
    
    def __init__(self, reason: str, required_permission: Optional[str] = None):
        details = {"reason": reason}
        if required_permission:
            details["required_permission"] = required_permission
        super().__init__(
            message=f"Error de seguridad: {reason}",
            code="SECURITY_ERROR",
            details=details
        )


class AuthenticationError(SecurityError):
    """Error de autenticación (token inválido, usuario no encontrado)"""
    
    def __init__(self, reason: str = "Credenciales inválidas"):
        super().__init__(reason)
        self.code = "AUTH_ERROR"


class PermissionDeniedError(SecurityError):
    """Permiso denegado"""
    
    def __init__(self, action: str, role: str):
        super().__init__(
            reason=f"Rol '{role}' no tiene permiso para '{action}'",
            required_permission=action
        )
        self.code = "PERMISSION_DENIED"


class AutomationError(JARVISException):
    """Error en automatización (Playwright, Selenium, etc.)"""
    
    def __init__(self, tool: str, action: str, reason: str):
        super().__init__(
            message=f"Error en automatización '{tool}.{action}': {reason}",
            code="AUTOMATION_ERROR",
            details={"tool": tool, "action": action, "reason": reason}
        )


class BrowserError(AutomationError):
    """Error específico del navegador"""
    
    def __init__(self, browser: str, reason: str):
        super().__init__(tool=browser, action="browser_control", reason=reason)
        self.code = "BROWSER_ERROR"


class WebScrapingError(AutomationError):
    """Error en web scraping"""
    
    def __init__(self, url: str, reason: str):
        super().__init__(tool="scraper", action=f"scrape {url}", reason=reason)
        self.code = "WEB_SCRAPING_ERROR"


class StarCarsError(JARVISException):
    """Error específico del módulo StarCars (automotriz)"""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            message=f"Error en StarCars '{operation}': {reason}",
            code="STARCARS_ERROR",
            details={"operation": operation, "reason": reason}
        )


class VehicleDetectionError(StarCarsError):
    """Error detectando marca/modelo de vehículo"""
    
    def __init__(self, image_path: str, reason: str):
        super().__init__(
            operation="vehicle_detection",
            reason=f"No se pudo detectar vehículo en {image_path}: {reason}"
        )
        self.code = "VEHICLE_DETECTION_ERROR"


class PublicationError(StarCarsError):
    """Error publicando vehículo"""
    
    def __init__(self, platform: str, vehicle_id: str, reason: str):
        super().__init__(
            operation="publication",
            reason=f"Error publicando vehículo {vehicle_id} en {platform}: {reason}"
        )
        self.code = "PUBLICATION_ERROR"


class WebSocketError(JARVISException):
    """Error en WebSocket"""
    
    def __init__(self, reason: str):
        super().__init__(
            message=f"Error en WebSocket: {reason}",
            code="WEBSOCKET_ERROR",
            details={"reason": reason}
        )


class ResourceNotFoundError(JARVISException):
    """Recurso no encontrado"""
    
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} con ID '{resource_id}' no encontrado",
            code="NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": resource_id}
        )


class RateLimitError(JARVISException):
    """Límite de tasa excedido"""
    
    def __init__(self, provider: str, retry_after: int):
        super().__init__(
            message=f"Límite de tasa excedido para {provider}. Reintentar en {retry_after}s",
            code="RATE_LIMIT_ERROR",
            details={"provider": provider, "retry_after": retry_after}
        )


class TimeoutError(JARVISException):
    """Timeout en operación"""
    
    def __init__(self, operation: str, timeout_seconds: int):
        super().__init__(
            message=f"Timeout después de {timeout_seconds}s en operación '{operation}'",
            code="TIMEOUT_ERROR",
            details={"operation": operation, "timeout": timeout_seconds}
        )


class InvalidInputError(JARVISException):
    """Entrada inválida del usuario"""
    
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Campo '{field}' inválido: {reason}",
            code="INVALID_INPUT",
            details={"field": field, "reason": reason}
        )


class FileOperationError(JARVISException):
    """Error en operación de archivos"""
    
    def __init__(self, operation: str, path: str, reason: str):
        super().__init__(
            message=f"Error en '{operation}' en '{path}': {reason}",
            code="FILE_ERROR",
            details={"operation": operation, "path": path, "reason": reason}
        )


class ModelNotFoundError(JARVISException):
    """Modelo de IA no encontrado"""
    
    def __init__(self, model_name: str, model_type: str):
        super().__init__(
            message=f"Modelo '{model_name}' de tipo '{model_type}' no encontrado",
            code="MODEL_NOT_FOUND",
            details={"model": model_name, "type": model_type}
        )


class ModelLoadError(JARVISException):
    """Error cargando modelo de IA"""
    
    def __init__(self, model_name: str, reason: str):
        super().__init__(
            message=f"Error cargando modelo '{model_name}': {reason}",
            code="MODEL_LOAD_ERROR",
            details={"model": model_name, "reason": reason}
        )


class QueueError(JARVISException):
    """Error en sistema de colas (RabbitMQ)"""
    
    def __init__(self, queue_name: str, operation: str, reason: str):
        super().__init__(
            message=f"Error en cola '{queue_name}' operación '{operation}': {reason}",
            code="QUEUE_ERROR",
            details={"queue": queue_name, "operation": operation, "reason": reason}
        )


class CacheError(JARVISException):
    """Error en caché (Redis)"""
    
    def __init__(self, operation: str, key: str, reason: str):
        super().__init__(
            message=f"Error en caché '{operation}' para clave '{key}': {reason}",
            code="CACHE_ERROR",
            details={"operation": operation, "key": key, "reason": reason}
        )


# Función helper para manejar excepciones en endpoints
def handle_exception(e: Exception) -> Dict[str, Any]:
    """Convierte cualquier excepción en respuesta JSON para API"""
    if isinstance(e, JARVISException):
        return e.to_dict()
    return {
        "error": "INTERNAL_SERVER_ERROR",
        "message": str(e),
        "details": {}
    }