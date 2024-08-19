from enum import Enum
class AdjustFlag(Enum):
    PostAdjust = "1"
    PreAdjust = "2"
    NoAdjust = "3"

class RequestFrequency(Enum):
    FiveMinutsK = '5'
    FifteenMinutsK = '15'
    ThirtyMinutsK = '30'
    HourK = '60'
    DayK = 'd'
    WeekK = 'w'
    MonthK = 'm'