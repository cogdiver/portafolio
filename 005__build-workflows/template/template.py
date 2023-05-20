import apache_beam as beam

def count_words(data):
    return (data
            | beam.FlatMap(lambda x: x.split(' '))
            | beam.Map(lambda x: (x, 1))
            | beam.CombinePerKey(sum)
            | beam.Map(print)
            )

def run_pipeline():
    with beam.Pipeline() as pipeline:
        lines = pipeline | "ReadInputData" >> beam.io.ReadFromText('gs://<bucket>/input.txt')
        count_words(lines)

if __name__ == '__main__':
    run_pipeline()
