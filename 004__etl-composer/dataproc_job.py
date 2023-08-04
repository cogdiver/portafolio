from pyspark.sql import SparkSession
from datetime import datetime


if __name__ == "__main__":
	
    # create Spark Session and context with necessary configuration
    spark = SparkSession \
        .builder \
        .master('local') \
        .appName('PySpark Letters Count Example') \
        .getOrCreate()

    sc = spark.sparkContext

    # Get bucket files
    file_regex = f"gs://<BUCKET_2>/{datetime.now().strftime('%Y/%m/%d')}/*.txt"
    files = sc.wholeTextFiles(file_regex).keys().collect()

    print('*'*50, 'FILES', '*'*50)
    print(files)
    print('*'*107)

    for path in files:
        # read data from text file and split each line into letters
        letters = sc.textFile(path).flatMap(lambda line: [l for l in line if l not in ',.* '])

        # count the occurrence of each letter
        lettersCounts = letters.map(lambda letter: (letter, 1)) \
            .reduceByKey(lambda a,b: a + b) \
            .map(lambda l: (path, l[0], l[1]))

        # save the counts to output
        lettersCounts.toDF(schema=['path','letters','total']) \
            .write.format('bigquery') \
            .option('table', '<PROJECT_ID>.<DATASET>.test') \
            .option("temporaryGcsBucket", "<BUCKET_2>") \
            .mode('append') \
            .save()
