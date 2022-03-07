from datetime import datetime
from re import S
import backtrader as bt
import datetime

from simplejson import OrderedDict

class Strategy(bt.Strategy):
    params = (
        ('exitbars', 5),
        ('maperiod', 15),
    )
    
    # a simple Strategy class
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(dt.isoformat(), txt)
    
    def __init__(self) -> None:
        self.dataclose = self.datas[0].close
        
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, price {0:.2f}, Cost {1:.2f}, Comm {2:.2f}'.format(
                    order.executed.price, 
                    order.executed.value,
                    order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, price {0:.2f}, Cost {1:.2f}, Comm {2:.2f}'.format(
                    order.executed.price, 
                    order.executed.value,
                    order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS {0:.2f}, NET {1:.2f}'.format(trade.pnl, trade.pnlcomm))

    def next(self):
        # self.log("Close {0}, previous Close {1}".format(self.dataclose[0], self.dataclose[-1]))
        
        if self.order:
            return
        
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                # current close price less than previous close price
                self.log('BUY CREATE, {0:.2f}'.format(self.dataclose[0]))
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, {0:.2f}'.format(self.dataclose[0]))
                self.order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Strategy)
    
    cerebro.broker.setcash(100000.0) # set cache
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print(cerebro.broker.getvalue())
    
    # load CSV data for testing
    data = bt.feeds.GenericCSVData(
        dataname='./data/000568.XSHE.csv',
        nullvalue=0.0,
        dtformat=('%Y-%m-%d'),
        fromdate=datetime.datetime(2017, 1, 1),
        todate=datetime.datetime(2017, 12, 31),
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        reverse=False
    )
    
    cerebro.adddata(data)
    cerebro.run()
    
    print(cerebro.broker.getvalue())
    cerebro.plot()