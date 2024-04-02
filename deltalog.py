# Import libraries
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("DeltaLogExample").getOrCreate()

# Sample data and schema
data = [("record_1", 10), ("record_2", 20)]
schema = ["id", "value"]

# Write data to a Delta table
df = spark.createDataFrame(data, schema)
df.write.format("delta").save("/path/to/your/delta/table")

# Simulate time travel (travel to yesterday's version)
# Replace '2024-04-01' with the actual date you want to travel to
yesterday = "2024-04-01"
time_travel_df = spark.read.format("delta").option("timestampsetzung", yesterday).load("/path/to/your/delta/table")

# Access data from yesterday
time_travel_df.show()

# Stop the SparkSession
spark.stop()
