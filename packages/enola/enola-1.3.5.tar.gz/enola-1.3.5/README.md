# Enola-AI: Plataforma de Validación y Observabilidad GenAI

Enola-AI es una plataforma avanzada de GenAI diseñada para validar y monitorear la robustez de los modelos de inteligencia artificial en industrias altamente reguladas como finanzas, salud y educación. Nuestra solución asegura que las implementaciones de IA cumplan con los estrictos estándares regulatorios mediante evaluaciones continuas, integraciones fluidas y monitoreo en tiempo real.

## Características Principales

- **Evaluación Multinivel:** Recopilación de feedback de usuarios, evaluaciones automatizadas y revisiones de expertos internos.
- **Monitoreo en Tiempo Real:** Capacidades de monitoreo continuo para detectar desviaciones en el comportamiento de los modelos de IA.
- **Integración Fluida:** Compatible con infraestructuras existentes como sistemas ERP, CRM y plataformas de análisis de datos.
- **Configuración Personalizada:** Adaptación de la metodología de evaluación según las necesidades específicas del cliente.
- **Seguridad y Cumplimiento:** Medidas avanzadas de seguridad y cumplimiento con normativas de protección de datos.

## Requisitos

- Python 3.7+
- Dependencias especificadas en `requirements.txt`


## Uso

1. Configura las variables de entorno necesarias:

    ```bash
    export token='tu_api_key'
    ```

2. Importa las librerías e inicializa

    ```python
    from enola import agent
    from enola.base.enola_types import ErrOrWarnKind
    from enola.base.enola_types import DataType
    ```

3. Inicializa el Agente

    ```python
    myAgent = agent.Agent(token=token,
                      name="Ejecución Demo Modelo Fuga",
                      isTest=True,
                      user_id="1",
                      user_name="Tu Nombre",
                      app_id= "GoogleColab",
                      channel_id="Google Colab",
                      session_id="1",
                      message_input="Hola, qué puedes hacer?"
                      )
    ```

4. Registra el paso

    ```python
    step1 = myAgent.new_step("step 1")
    step1.add_extra_info("ValorNumerico", 11)
    step1.add_extra_info("ValorTexto", "valor2")
    ```

5. Registra errores si es que existen

    ```python
    step1.add_error(id="10", message="Error de validación de datos", kind=ErrOrWarnKind.INTERNAL_TOUSER)
    ```

6. envía los datos al Server

    ```python
    data_server = myAgent.finish_agent(True, message_output="Salida generada por tu agente", num_iteratons=15 )
    ```

7. Ejecuta la aplicación:

    ```bash
    python main.py
    ```


## Contribuciones

¡Contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request para cualquier mejora o corrección.

## Licencia

Este proyecto está licenciado bajo la Licencia BSD 3-Clause License . Ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para cualquier consulta o soporte, por favor contacta a [help@huemulsolutions.com](mailto:help@huemulsolutions.com).