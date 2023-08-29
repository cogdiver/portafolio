import sys
import apache_beam as beam

def count_words(data):
    return (data
            | beam.FlatMap(lambda x: x.split(' '))
            | beam.Map(lambda x: (x, 1))
            | beam.CombinePerKey(sum)
            | beam.Map(print)
            )

def run_pipeline(input_file):
    with beam.Pipeline() as pipeline:
        lines = pipeline | "ReadInputData" >> beam.io.ReadFromText(input_file)
        count_words(lines)
        # counts = count_words(lines)
        # print(counts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Se requiere especificar el nombre del archivo de entrada.")
        sys.exit(1)

    input_file = sys.argv[1]
    run_pipeline(input_file)
# run_pipeline('gs://005__build-workflows/template/input.txt')
