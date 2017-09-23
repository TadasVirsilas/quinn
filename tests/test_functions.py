import pytest

from quinn.spark import *
import quinn.functions as QF
from quinn.extensions import *

from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, IntegerType, ArrayType

class TestFunctions(object):

    def test_exists(self):
        source_df = spark.createDataFrame(
            [
                ("jose", [1, 2, 3]),
                ("li", [4, 5, 6]),
                ("luisa", [10, 11, 12]),
            ],
            StructType([
                StructField("name", StringType(), True),
                StructField("nums", ArrayType(IntegerType(), True), True),
            ])
        )

        actual_df = source_df.withColumn(
            "any_num_greater_than_5",
            QF.exists(lambda n: n > 5)(col("nums"))
        )

        expected_df = spark.createDataFrame(
            [
                ("jose", [1, 2, 3], False),
                ("li", [4, 5, 6], True),
                ("luisa", [10, 11, 12], True)
            ],
            StructType([
                StructField("name", StringType(), True),
                StructField("nums", ArrayType(IntegerType(), True), True),
                StructField("any_num_greater_than_5", BooleanType(), True)
            ])
        )

        assert(expected_df.collect() == actual_df.collect())

    def test_forall(self):
        source_df = spark.createDataFrame(
            [
                ("jose", [1, 2, 3]),
                ("li", [4, 5, 6]),
                ("luisa", [10, 11, 12]),
            ],
            StructType([
                StructField("name", StringType(), True),
                StructField("nums", ArrayType(IntegerType(), True), True),
            ])
        )

        actual_df = source_df.withColumn(
            "all_nums_greater_than_3",
            QF.forall(lambda n: n > 3)(col("nums"))
        )

        expected_df = spark.createDataFrame(
            [
                ("jose", [1, 2, 3], False),
                ("li", [4, 5, 6], True),
                ("luisa", [10, 11, 12], True)
            ],
            StructType([
                StructField("name", StringType(), True),
                StructField("nums", ArrayType(IntegerType(), True), True),
                StructField("all_nums_greater_than_3", BooleanType(), True)
            ])
        )

        assert(expected_df.collect() == actual_df.collect())

    def test_multi_equals(self):
        source_df = spark.createDF(
            [
                ("cat", "cat"),
                ("cat", "dog"),
                ("pig", "pig"),
                ("", ""),
                (None, None)
            ],
            [
                ("s1", StringType(), True),
                ("s2", StringType(), True)
            ]
        )

        actual_df = source_df.withColumn(
            "are_s1_and_s2_cat",
            QF.multi_equals("cat")(col("s1"), col("s2"))
        )

        expected_df = spark.createDF(
            [
                ("cat", "cat", True),
                ("cat", "dog", False),
                ("pig", "pig", False),
                ("", "", False),
                (None, None, False),
            ],
            [
                ("s1", StringType(), True),
                ("s2", StringType(), True),
                ("are_s1_and_s2_cat", BooleanType(), True),
            ]
        )

        assert(expected_df.collect() == actual_df.collect())
