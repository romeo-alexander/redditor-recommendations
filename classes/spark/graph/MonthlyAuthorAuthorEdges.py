from AuthorAuthorEdges import AuthorAuthorEdges
from MonthlyClock import MonthlyClock

class MonthlyAuthorAuthorEdges(AuthorAuthorEdges):
 
    def __init__(self, cfg, context):
        self.context = context
        self.inBucket = cfg['s3']['cleanComments']
        self.outBucket = cfg['s3']['dailyEdges']
        self.truncation = cfg['tuning']['truncation']
        self.partitions = cfg['tuning']['edgePartitions']
        self.clock = MonthlyClock()
