from datetime import datetime
import backtrader as bt

class Strategy(bt.Strategy):
    # a simple Strategy class
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(dt.isoformat(), txt)
    
    def __init__(self) -> None:
        self.dataclose = self.datas[0].close
    
    def next(self):
        self.log("Close, {0}".format(self.dataclose[0]))

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Strategy)
    
    cerebro.broker.setcash(110000.0) # set cache
    print(cerebro.broker.getvalue())
    
    # load CSV data for testing
    data = bt.feeds.GenericCSVData(
        dataname='./data/000568.XSHE.csv',
        nullvalue=0.0,
        dtformat=('%Y-%m-%d'),
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1
    )
    
    cerebro.adddata(data)
    cerebro.run()
    
    print(cerebro.broker.getvalue())