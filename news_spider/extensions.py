from scrapy.extensions.corestats import CoreStats
from datetime import datetime, timedelta
import pytz


class TestCoreStats(CoreStats):
    """
    此扩展类的作用是修改日期为本地时区日期，特别注意，这些时间均依赖于当前系统时间，即需要当前系统时间准确。
    日志中显示的时间也是依赖于当前系统时间。
    """

    def spider_opened(self, spider):
        self.start_time = datetime.utcnow()  # utc时间
        self.start_time_now = datetime.now()  # 当前系统时间
        self.start_time_zone = datetime.now(tz=pytz.timezone('Asia/Shanghai'))  # 选择指定时区时间
        self.start_time_delta = self.start_time + timedelta(hours=8)  # 根据时区对utc对时间计算，比如北京时间是东八区，即为utc时间加8小时
        self.stats.set_value('start_time', self.start_time, spider=spider)
        self.stats.set_value('start_time_now', self.start_time_now, spider=spider)
        self.stats.set_value('start_time_zone', self.start_time_zone, spider=spider)
        self.stats.set_value('start_time_delta', self.start_time_delta, spider=spider)

    def spider_closed(self, spider, reason):
        finish_time = datetime.utcnow()  # utc时间
        finish_time_now = datetime.now()  # 当前系统时间
        finish_time_zone = datetime.now(tz=pytz.timezone('Asia/Shanghai'))  # 选择指定时区时间
        finish_time_delta = finish_time + timedelta(hours=8)  # 根据时区对utc对时间计算，比如北京时间是东八区，即为utc时间加8小时
        elapsed_time = finish_time - self.start_time
        elapsed_time_seconds = elapsed_time.total_seconds()
        self.stats.set_value('elapsed_time_seconds', elapsed_time_seconds, spider=spider)
        self.stats.set_value('finish_time', finish_time, spider=spider)
        self.stats.set_value('finish_time_now', finish_time_now, spider=spider)
        self.stats.set_value('finish_time_zone', finish_time_zone, spider=spider)
        self.stats.set_value('finish_time_delta', finish_time_delta, spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)