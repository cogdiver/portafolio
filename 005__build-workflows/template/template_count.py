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
        counts = count_words(lines)
        print(counts)

if __name__ == '__main__':
    print(sys.argv)
    run_pipeline('gs://005__build-workflows/template/input.txt')
