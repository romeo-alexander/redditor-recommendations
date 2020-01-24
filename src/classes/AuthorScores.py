import os
from pyspark.sql import functions as F

class AuthorScores:
 
    def loadComments(self, context, comments, calendar):
        self.df = comments.dataFrame(context, calendar) 
        return self

    def addScores(self):
        self.df = self.df.groupBy("author") \
                         .agg( {"score" : "sum"} ) \
        return self

    def write(self):
        self.df.show(10)
        self.df.write. \
            .option("header", "false") \
            .csv('authorScores')
