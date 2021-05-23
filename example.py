from yahooquery import Ticker
import zz


t = Ticker('AAPL')
hist = t.history(period='1y')
for (i_h, p_h),(i_l, p_l) in zz.zigzag(hist['high'], hist['low']):
    print(f'PEAK Index: {i_h}, price: {p_h}, VALLEY Index: {i_l}, price: {p_l}')

