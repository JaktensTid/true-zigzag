from math import floor


def _calc_dev(base_price, price):
    return 100 * (price - base_price) / base_price


def zigzag(highs, lows, depth=10, dev_threshold=5):
    def pivots(src_raw, length, isHigh):
        src = list(reversed(src_raw))
        bar_index = list(range(len(src)))
        for start in range(0, len(src)):
            if start + 2 * length + 1 > len(src) - 1:
                return
            p = 0
            if length < len(src) - start:
                p = src[start + length]
            if length == 0:
                yield 0, p
            else:
                isFound = True
                for i in range(start, start + length):
                    if isHigh and src[i] > p:
                        isFound = False
                    if not isHigh and src[i] < p:
                        isFound = False
                for i in range(start + length + 1, start + 2 * length + 1):
                    if isHigh and src[i] >= p:
                        isFound = False
                    c = not isHigh and src[i] <= p
                    if c:
                        isFound = False
                if isFound:
                    yield (bar_index[start + length], p)
                else:
                    yield None, None

    data_highs = [x for x in pivots(highs, floor(depth / 2), True) if x[0]]
    data_lows = [x for x in pivots(lows, floor(depth / 2), False) if x[0]]

    result = []
    prev_data = None

    for i, (ind, p) in enumerate(data_highs):
        if i == 0:
            prev_data = (ind, p)
            result.append(
                ((ind, p),
                 (data_lows[0][0], data_lows[0][1]))
            )
            continue

        lows_d = sorted([(ind_l, p_l) for ind_l, p_l in data_lows if ind > ind_l > prev_data[0]], key=lambda x: x[1])
        if lows_d:
            lows = lows_d[0]

            if abs(_calc_dev(lows[1], p)) >= dev_threshold:
                result.append(
                    ((ind, p),
                     (lows[0], lows[1]))
                )
        else:
            if p > prev_data[-1]:
                last_item = result[-1]
                result = result[:-1]
                result.append(((ind, p),
                     last_item[-1]))
        prev_data = (ind, p)

    return result
