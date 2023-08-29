import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# Definir las opciones del flujo de datos
options = PipelineOptions()

# Definir la clase de transformación
class TransformData(beam.DoFn):
    def process(self, element):
        # Realizar la transformación de los datos aquí
        transformed_data = transform_function(element)
        yield transformed_data

# Definir la función de transformación
def transform_function(data):
    # Realizar la transformación de los datos
    transformed_data = data.upper()  # Ejemplo de transformación: convertir a mayúsculas
    return transformed_data

# Definir el flujo de datos
with beam.Pipeline(options=options) as p:
    # Leer los mensajes de Pub/Sub
    messages = (p
                | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(subscription='<SUBSCRIPTION_NAME>')
                )
    
    # Aplicar la transformación a los datos
    transformed_data = (messages
                        | 'Transform Data' >> beam.ParDo(TransformData())
                        )
    
    # Escribir los datos en BigQuery
    transformed_data | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
        table='<PROJECT_ID>:<DATASET>.<TABLE>',
        schema='<SCHEMA>',
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
    )
