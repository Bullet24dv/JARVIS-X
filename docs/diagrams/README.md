# Diagramas de Arquitectura JARVIS-X

Los diagramas de arquitectura se generan bajo demanda. Para visualizar la estructura, consulte:

- Diagrama de componentes: [architecture.md](../architecture.md)
- Flujo de datos: flujo secuencial descrito en el README principal

Puede generar diagramas con herramientas como Mermaid o Draw.io usando la siguiente descripción:

```mermaid
graph TD
    A[Usuario] --> B[Wake Word / STT]
    B --> C[LLM Router]
    C --> D[Agente Orquestador]
    D --> E1[Programador]
    D --> E2[Investigador]
    D --> E3[Analista]
    E1 --> F[MCP Tools]
    F --> G[Acciones]
    G --> H[TTS]
    H --> A