# todo 1. 对于查询的持仓，空的也要推送空的，否则orderplit无法回调.  这对于http请求很容易实现，但是如果是websocket回调，也许空的不会回调？例如ibk

import pandas as pd
from datetime import datetime, timedelta

from tigeropen.common.consts import (Language,        # 语言
                                Market,           # 市场
                                BarPeriod,        # k线周期
                                QuoteRight)       # 复权类型
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.trade.domain.contract import Contract
from tigeropen.trade.domain.position import Position
from tigeropen.trade.domain.prime_account import PortfolioAccount
from tigeropen.trade.domain.prime_account import Segment
from tigeropen.trade.trade_client import TradeClient
from tigeropen.tiger_open_config import get_client_config
from tigeropen.common.consts import SecurityType, Currency, Market, OrderStatus, TradingSession
from tigeropen.common.util.contract_utils import stock_contract, option_contract_by_symbol
from tigeropen.common.util.order_utils import limit_order, market_order
from tigeropen.push.push_client import PushClient
from tigeropen.push.pb.QuoteBBOData_pb2 import QuoteBBOData
from tigeropen.push.pb.QuoteBasicData_pb2 import QuoteBasicData
from tigeropen.push.pb.OrderStatusData_pb2 import OrderStatusData
from tigeropen.push.pb.TradeTickData_pb2 import TradeTickData
from tigeropen.trade.domain.order import Order

from tigeropen.common.consts import (
    OrderStatus, OrderType
)

from typing import Union, Tuple, Optional
import itertools
from ks_trade_api.object import ContractData, MyAccountData, ErrorData, MyPositionData, MyTradeData, MyOrderData, OptionData
from ks_trade_api.constant import (
    Product as ksProduct,
    Currency as KsCurrency,
    Exchange as KsExchange,
    Direction as KsDirection, 
    OrderType as ksOrderType, 
    Direction as KsDirection,
    SubscribeType as KsSubscribeType,
    Offset as KsOffset, 
    TimeInForce as KsTimeInForce,
    TradingHours as KsTradingHours,
    ErrorCode as KsErrorCode,
    Status as KsStatus,
    RetCode,
    RET_OK, 
    RET_ASYNC,
    RET_ERROR, 
    CHINA_TZ,
    Environment
)
from ks_trade_api.base_trade_api import BaseTradeApi, RateLimitChecker
from ks_trade_api.utility import extract_vt_symbol, extract_vt_orderid, get_trading_hours, TradingHours, extract_option_vt_symbol
import sys
from decimal import Decimal
import uuid
from logging import DEBUG, WARNING, ERROR
from ks_utility.numbers import to_decimal

RATES_INTERVAL: int = 30

class OrderSide:
    BUY = 'BUY'
    SELL = 'SELL'

class TimeInForce:
    DAY = 'DAY' # 日内有效
    GTC = 'GTC' # good till cancel
    GTD = 'GTD' # good till date

EXCHANGE_MY2KS = {
    'US': 'SMART',
    'HK': 'SEHK'
}

class Currency:
    USD = 'USD'
    HKD = 'HKD'

CURRENCY_MY2KS = {
    Currency.USD: KsCurrency.USD,
    Currency.HKD: KsCurrency.HKD
}

EXCHANGE_CURRENCY_MAP: dict = {
    KsExchange.SMART: Currency.USD,
    KsExchange.SEHK: Currency.HKD
}

SUBTYPE_KS2MY = {
    KsSubscribeType.USER_ORDER: KsSubscribeType.USER_ORDER,
    KsSubscribeType.USER_TRADE: KsSubscribeType.USER_TRADE,
    KsSubscribeType.USER_POSITION: KsSubscribeType.USER_POSITION,
}

TRADING_HOURS2TRADING_SESSION: dict = {
    TradingHours.PRE_MARKET: TradingSession.PreMarket,
    TradingHours.RTH: TradingSession.Regular,
    TradingHours.AFTER_HOURS: TradingSession.AfterHours,
    TradingHours.OVER_NIGHT: TradingSession.OverNight
}


def extract_my_symbol(contract: Union[Contract, OrderStatusData]):
    exchange = KsExchange(EXCHANGE_MY2KS.get(contract.market))
    sec_type_str: str = contract.secType if isinstance(contract, OrderStatusData) else contract.sec_type
    if SecurityType(sec_type_str) == SecurityType.OPT:
        opion_data: OptionData = OptionData(
            gateway_name=None, underlying_symbol=contract.symbol, exchange=exchange, 
            expiry=contract.expiry[2:], right=contract.right[:1], strike=Decimal(str(contract.strike))
        )
        symbol = opion_data.symbol
    else:
        symbol = contract.symbol
    

    return symbol, exchange

def transform_scale(quantity: int, scale: int) -> Decimal:
    return Decimal(quantity * (10 ** -scale))

MARKET_KS2MY = {
    KsExchange.SEHK: 'HK',
    KsExchange.SMART: 'US'
}

MARKET_MY2KS = { v:k for k,v in MARKET_KS2MY.items() }

def symbol_ks2my(vt_symbol: str):
    if not vt_symbol:
        return ''
    symbol, ks_exchange = extract_vt_symbol(vt_symbol)
    return symbol

ORDERTYPE_MY2KS = {
    OrderType.LMT: ksOrderType.LIMIT,
    OrderType.MKT: ksOrderType.MARKET
}

ORDERTYPE_KS2MY = {v:k for k,v in ORDERTYPE_MY2KS.items()}


STATUS_MY2KS = {
    OrderStatus.PENDING_NEW: KsStatus.NOTTRADED,
    OrderStatus.NEW: KsStatus.NOTTRADED,
    OrderStatus.HELD: KsStatus.NOTTRADED,
    OrderStatus.PARTIALLY_FILLED: KsStatus.PARTTRADED,
    OrderStatus.FILLED: KsStatus.ALLTRADED,
    OrderStatus.CANCELLED:  KsStatus.CANCELLED,
    OrderStatus.PENDING_CANCEL: KsStatus.NOTTRADED,
    OrderStatus.REJECTED: KsStatus.REJECTED,
    OrderStatus.EXPIRED: KsStatus.REJECTED
}

STATUS_KS2MY = { v:k for k,v in STATUS_MY2KS.items() }

SIDE_KS2MY = {
    f'{KsDirection.LONG.value},{KsOffset.OPEN.value}': OrderSide.BUY,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSE.value}': OrderSide.SELL,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSETODAY.value}': OrderSide.SELL,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSEYESTERDAY.value}': OrderSide.SELL,

    f'{KsDirection.SHORT.value},{KsOffset.OPEN.value}': OrderSide.SELL,
    f'{KsDirection.LONG.value},{KsOffset.CLOSE.value}': OrderSide.BUY,
    f'{KsDirection.LONG.value},{KsOffset.CLOSETODAY.value}': OrderSide.BUY,
    f'{KsDirection.LONG.value},{KsOffset.CLOSEYESTERDAY.value}': OrderSide.BUY,
}

def side_ks2my(direction: KsDirection, offset: KsOffset):
    key = f'{direction.value},{offset.value}'
    return SIDE_KS2MY.get(key)

def sides_ks2my(directions: list[KsDirection], offsets: list[KsOffset]):
    sides_map = {}
    combinations = itertools.product(directions, offsets)
    for direction, offset in combinations:
        sides_map[side_ks2my(direction, offset)] = 1
    sides = list(sides_map.keys())
    return sides

def side_my2ks(side: OrderSide):
    # 为啥原来会是对的？
    if side == OrderSide.BUY:
        direction = KsDirection.LONG
        offset = KsOffset.OPEN
    else:
        direction = KsDirection.SHORT
        offset = KsOffset.CLOSE
    return direction, offset


TIF_KS2MY = {
    KsTimeInForce.GTD: TimeInForce.DAY,
    KsTimeInForce.GTC: TimeInForce.GTC
}

class KsTigerTradeApi(BaseTradeApi):
    gateway_name: str = "KS_TIGER"

    ERROR_CODE_MY2KS: dict = {
        429002: KsErrorCode.RATE_LIMITS_EXCEEDED,
        603059: KsErrorCode.LIQUIDITY_LACKED
    }

    def __init__(self, setting: dict):
        environment = setting.get('environment', Environment.TEST.value)
        self.is_test = Environment(setting.get('environment', Environment.TEST.value)) == Environment.TEST
        private_key_path = setting.get('private_key_path')
        tiger_id = setting.get('tiger_id')
        account_id = setting.get('account_id')
        self.account_id = account_id
        dd_secret = setting.get('dd_secret')
        dd_token = setting.get('dd_token')
        gateway_name = setting.get('gateway_name', self.gateway_name)

        self.client_config = get_client_config(private_key_path, tiger_id, account_id)
        self.push_client = None
        
        super().__init__(gateway_name=gateway_name, dd_secret=dd_secret, dd_token=dd_token)

        self.orders = {} # 用来记录成交数量
        self.order_id_status_map: dict = {} # 用于记录order_id和status的映射
        self.api_name_error_time_map: dict = {} # 用于记录api出错时间，限制超频访问
        
        self.init_handlers()

    def order_data_my2ks(self, data: Union[Order, OrderStatusData]) -> MyOrderData:
            is_order = isinstance(data, Order)
            orderid = data.id
            contract: Contract = data.contract if is_order else data
            symbol, exchange = extract_my_symbol(contract)
            timestamp: int = data.order_time if is_order else data.openTime
            dt: datetime = datetime.fromtimestamp(timestamp/1000)
            dt: datetime = dt.astimezone(CHINA_TZ)
            direction, offset = side_my2ks(data.action)
            order_type = data.order_type if is_order else data.orderType
            type = ORDERTYPE_MY2KS.get(str(order_type))
            price_float = data.limit_price if is_order else data.limitPrice
            price_float = price_float if not price_float == None else 0
            price = Decimal(str(price_float))

            volume = transform_scale(data.quantity, data.quantity_scale) if is_order else transform_scale(data.totalQuantity, data.totalQuantityScale)
            traded = Decimal(str(data.filled)) if is_order else transform_scale(data.filledQuantity, data.filledQuantityScale)
            user_mark = data.user_mark if is_order else data.userMark
            error = data.reason if is_order else data.errorMsg
            status = STATUS_MY2KS[data.status if is_order else getattr(OrderStatus, data.status)]
            
            order: MyOrderData = MyOrderData(
                symbol=symbol,
                exchange=exchange,
                orderid=orderid,
                type=type,
                direction=direction,
                offset=offset,
                price=price,
                volume=volume,
                traded=traded,
                status=status,
                error=error,
                datetime=dt,
                reference=user_mark,
                gateway_name=self.gateway_name
            )
            return order

    # 初始化行回调和订单回调
    def init_handlers(self):
        trade = self

        # self.quote_ctx = quote_ctx = QuoteContext(self.conn_config)
        client_config = self.client_config
        self.trd_ctx = trd_ctx = TradeClient(client_config) # todo!
        # self.trd_ctx = trd_ctx = TradeClient(client_config, logger=self.logger)
        # 随后传入配置参数对象来初始化QuoteClient
        self.trd_ctx = trd_ctx = TradeClient(client_config, logger=self.logger)
       

        # # 实时行情回调
        # def on_quote(symbol: str, data: PushQuote):
        #     self.on_quote(symbol, data)
        # quote_ctx.set_on_quote(on_quote)

        # # 盘口 callback
        # # 实时行情回调
        # def on_depth(symbol: str, data: PushDepth):
        #     self.on_depth(symbol, data)
        # quote_ctx.set_on_depth(on_depth)
        
        # # 分笔 callback
        # def on_trades(symbol: str, data: PushTrades):
        #     self.on_trades(symbol, data)
        # quote_ctx.set_on_trades(on_trades)

        # kline callback
        # class CurKlineHandler(CurKlineHandlerBase):
        #     def on_recv_rsp(self, rsp_pb):
        #         ret_code, data = super(CurKlineHandler,self).on_recv_rsp(rsp_pb)
        #         if ret_code != RET_OK:
        #             return RET_ERROR, data
        #         trade.on_cur_kline(data)
        #         return RET_OK, data
        # handler = CurKlineHandler()
        # quote_ctx.set_handler(handler) 

        # # 分时 callback
        # class RTDataHandler(RTDataHandlerBase):
        #     def on_recv_rsp(self, rsp_pb):
        #         ret_code, data = super(RTDataHandler,self).on_recv_rsp(rsp_pb)
        #         if ret_code != RET_OK:
        #             trade.log({'msg': data}, level=ERROR, name='on_rt_data')
        #             return RET_ERROR, data
        #         data = Munch.fromDict(data.to_dict('records')[0])
        #         # trade.log(data, name='on_rt_data')
        #         trade.on_rt_data(data)
        #         return RET_OK, data
        # handler = RTDataHandler()
        # quote_ctx.set_handler(handler)

        # order callback
        

     # 订阅行情
    def subscribe(self, vt_symbols, vt_subtype_list, extended_time=True) -> tuple[RetCode, Optional[ErrorData]]:
        if isinstance(vt_symbols, str):
            vt_symbols = [vt_symbols]

        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        my_subtype_list = [SUBTYPE_KS2MY.get(x) for x in vt_subtype_list]

        trade = self
        trd_ctx = self.trd_ctx
        if KsSubscribeType.USER_ORDER in my_subtype_list:
            if not self.push_client:
                client_config = self.client_config
                protocol, host, port = client_config.socket_host_port
                self.push_client = push_client = PushClient(host, port, use_ssl=(protocol == 'ssl'), use_protobuf=True)
                # 建立连接
                push_client.connect(client_config.tiger_id, client_config.private_key)

            # order callback
            def on_order_changed(data: OrderStatusData):
                # 先进行成交回调
                # if data.executed_quantity:
                # breakpoint() # todo
                # print('tttttt:', data.status, data.msg)
                order_id = data.id
                order = self.orders.get(order_id, None)
                executed_quantity = transform_scale(data.filledQuantity, data.filledQuantityScale)
                if not order:
                    self.orders[order_id] = order = { 'last_executed_quantity': executed_quantity, 'last_share': executed_quantity }
                else:
                    last_share = executed_quantity - self.orders[order_id]['last_executed_quantity']
                    # 某种情况下，前面的订单状态回调比后续的状态还快，这个时候不能再推送成交
                    if last_share > 0:
                        order['last_share'] = last_share
                        order['last_executed_quantity'] = executed_quantity
                    else:
                        order['last_share'] = 0

                if order['last_share']:
                    symbol, exchange = extract_my_symbol(data)
                    direction, offset = side_my2ks(data.action)
                    price = Decimal(str(data.avgFillPrice)) if data.avgFillPrice else Decimal('0')
                    volume = Decimal(str(order['last_share']))
                    dt = datetime.fromtimestamp(data.timestamp/1000)
                    dt = dt.astimezone(CHINA_TZ)
                    trade: MyTradeData = MyTradeData(
                        symbol=symbol,
                        exchange=exchange,
                        orderid=order_id,
                        tradeid=str(uuid.uuid4()),
                        direction=direction,
                        offset=offset,
                        price=price,
                        volume=volume,
                        datetime=dt,
                        gateway_name=self.gateway_name
                    )
                    # breakpoint() # todo
                    self.on_trade(trade)

                # 然后进行订单回调
                order: MyOrderData = self.order_data_my2ks(data)
                self.on_order(order)
                self.log(order, level=DEBUG) # todo! 是否影藏吊
                self.order_id_status_map[order_id] = order.status

            self.push_client.order_changed = on_order_changed
            # 订阅订单变化
            self.push_client.subscribe_order(account=self.account_id)

        return RET_OK, None

    # 下单
    @RateLimitChecker(RATES_INTERVAL)
    def send_order(
            self, 
            vt_symbol: str,
            price: Decimal,
            volume: Decimal,
            type: ksOrderType = ksOrderType.LIMIT,
            direction: KsDirection = KsDirection.LONG,
            offset: KsOffset = KsOffset.OPEN,
            time_in_force: KsTimeInForce = KsTimeInForce.GTC,
            trading_hours: KsTradingHours = KsTradingHours.RTH,
            reference: str = '',
            product: ksProduct = ksProduct.EQUITY
    ) -> Tuple[RetCode, Union[str, ErrorData]]:
        try:
            my_symbol = symbol_ks2my(vt_symbol)
            symbol, exchange = extract_vt_symbol(vt_symbol)
            order_type = ORDERTYPE_KS2MY.get(type)
            side = side_ks2my(direction, offset)
            time_in_force = TIF_KS2MY.get(time_in_force)
  
            # 生成股票合约
            currency: Currency = EXCHANGE_CURRENCY_MAP.get(exchange)
            if product == ksProduct.OPTION:
                option_data: OptionData = extract_option_vt_symbol(vt_symbol)
                contract = option_contract_by_symbol(
                    symbol=option_data.underlying_symbol,
                    expiry=option_data.expiry,
                    put_call=option_data.right,
                    strike=float(option_data.strike),
                    currency=currency
                )
            else:
                contract = stock_contract(symbol=my_symbol, currency=currency)
            #生成订单对象
            if type == ksOrderType.LIMIT:
                order = limit_order(account=self.client_config.account, contract=contract, action=side, limit_price=float(price), quantity=int(volume))
            else:
                order = market_order(account=self.client_config.account, contract=contract, action=side, quantity=int(volume))
            # 夜盘时间则加上夜盘session
            trading_hours: TradingHours = get_trading_hours()
            order.trading_session_type = TRADING_HOURS2TRADING_SESSION.get(trading_hours, TradingSession.Regular)
            order.user_mark = reference

            #下单
            order_id = self.trd_ctx.place_order(order)
            
            if order_id:
                symbol, exchange = extract_vt_symbol(vt_symbol)
                order_data: MyOrderData = MyOrderData(
                    symbol=symbol,
                    exchange=exchange,
                    orderid=order_id,
                    type=type,
                    direction=direction,
                    offset=offset,
                    price=price,
                    volume=volume,
                    reference=reference,
                    gateway_name=self.gateway_name
                )
                if not self.order_id_status_map.get(order_id):
                    self.on_order(order_data)
                else:
                    self.log(f'由于订单回调已经先于send_order返回，跳过执行on_order。order_id={order_id},current_status={self.order_id_status_map.get(order_id)}', level=WARNING)
            self.log({
                'symbol': my_symbol,
                'order_type': order_type,
                'side': side,
                'submitted_quantity': volume,
                'submitted_price': price,
                'time_in_force': time_in_force,
                'trading_hours': trading_hours,
                'trading_session_type': order.trading_session_type,
                'remark': reference,
                'order_id': order_id
            })
            return RET_OK, order_data.vt_orderid
        except Exception as e:
            error = self.get_error(params={
                'symbol': my_symbol,
                'order_type': order_type,
                'side': side,
                'submitted_quantity': volume,
                'submitted_price': price,
                'time_in_force': time_in_force,
                'trading_hours': trading_hours,
                'trading_session_type': order.trading_session_type,
                'remark': reference,
            }, e=e)
            return RET_ERROR, error
        
    # My.add 直接向服务器请求合约数据
    @RateLimitChecker(RATES_INTERVAL)
    def request_cancel_orders(
            self,
            vt_symbol: Optional[str] = None,
            direction: KsDirection = None,
            offset: KsOffset = None
        ) -> tuple[RetCode,  list[MyOrderData]]:
        ret = RET_OK
        orders = []
        
        ret_query, open_orders = self.query_open_orders(vt_symbol=vt_symbol, direction=direction, offset=offset)
        if ret_query == RET_ASYNC:
            # todo 异步尚未处理好
            return ret_query, open_orders
        
        if ret_query == RET_OK:  
            for order in open_orders:
                order: MyOrderData
                ret_cancel, cancel_res = self.cancel_order(order.vt_orderid)
                # todo这里没有处理异步
                if ret_cancel == RET_OK:
                    order.status = KsStatus.CANCELLED
                    orders.append(order)
                else:
                    ret = ret_cancel
                    orders = cancel_res
                    break
        else:
            ret = ret_query
            orders = open_orders
            

        return ret, orders

    # 撤单
    @RateLimitChecker(RATES_INTERVAL)
    def cancel_order(self, vt_orderid: str) -> Tuple[RetCode, Optional[ErrorData]]:
        self.log({'vt_orderid': vt_orderid}, level=DEBUG)
        try:
            gateway_name, orderid = extract_vt_orderid(vt_orderid)
            data = self.trd_ctx.cancel_order(id=orderid)
        except Exception as e:
            error = self.get_error(orderid, e=e)
            return RET_ERROR, error

        return RET_OK, vt_orderid

    # 获取账号信息
    def query_account(self, currencies: list[KsCurrency] = []) -> tuple[RetCode, Union[MyAccountData, ErrorData]]:
        try:
            if not currencies:
                currencies = [KsCurrency.USD, KsCurrency.HKD]
            accounts = []
            for currency in currencies:
                data: PortfolioAccount = self.trd_ctx.get_prime_assets(self.account_id, base_currency=currency.name)
                segment: Segment = data.segments['S']
                account = None
                if segment:
                    account: MyAccountData = MyAccountData(
                        accountid=self.account_id,
                        available_cash=to_decimal(segment.currency_assets[currency.name].cash_available_for_trade),
                        buy_power=to_decimal(segment.buying_power), 
                        balance=to_decimal(segment.net_liquidation),
                        currency=currency,
                        gateway_name=self.gateway_name,
                    )
                    account.available = segment.cash_available_for_trade
                    accounts.append(account)
            return RET_OK, accounts
        except Exception as e:
            error = self.get_error(currency=currency, e=e)
            return RET_ERROR, error
        
        segment: Segment = data.segments['S']
        account = None
        if segment:
            currency: KsCurrency = CURRENCY_MY2KS.get(segment.currency)
            account: MyAccountData = MyAccountData(
                accountid=self.account_id,
                balance=segment.net_liquidation,
                frozen=0,
                currency=currency,
                gateway_name=self.gateway_name,
            )
            account.available = segment.cash_available_for_trade
            return RET_OK, account
        return RET_OK, None


    # 获取持仓信息
    @RateLimitChecker(RATES_INTERVAL)
    def query_position(self, vt_symbols=[], directions: list[KsDirection] = []):
        try:
            # 要查询股票和期权
            data = self.trd_ctx.get_positions(symbol=None, sec_type=None)
        except Exception as e:
            error = self.get_error(vt_symbols, e=e)
            self.send_dd(error.msg, f'持仓查询错误')
            return RET_ERROR, error 
        
        positions = []
        if data:
            for position_data in data:
                position_data: Position
                symbol, exchange = extract_my_symbol(position_data.contract)
                volume = transform_scale(position_data.quantity, position_data.position_scale)
                direction = KsDirection.NET
                position = MyPositionData(
                    symbol=symbol,
                    exchange=exchange,
                    direction=direction,
                    price=position_data.average_cost,
                    volume=volume,
                    available=volume,
                    gateway_name=self.gateway_name
                )
                positions.append(position)

        # 去除多余持仓
        if vt_symbols:
            positions = [x for x in positions if x.vt_symbol in vt_symbols]

        # 补齐空持仓
        ret_ks_symbols = [x.vt_symbol for x in positions]
        lack_ks_symbols = [x for x in vt_symbols if not x in ret_ks_symbols]
        for lack_ks_symbol in lack_ks_symbols:
            if not lack_ks_symbol:
                continue
            symbol, exchange = extract_vt_symbol(lack_ks_symbol)
            lack_postion = MyPositionData(symbol=symbol, exchange=exchange, direction=KsDirection.NET, gateway_name=self.gateway_name)
            positions.append(lack_postion)

        return RET_OK, positions
    
    # 获取今日订单
    def query_orders(self, 
        vt_symbol: Optional[str] = None, 
        direction: Optional[KsDirection] = None, 
        offset: Optional[KsOffset] = None,
        status: Optional[list[KsStatus]] = None,
        orderid: Optional[str] = None,
        reference: Optional[str] = None 
    ) -> tuple[RetCode, Union[list[MyOrderData], ErrorData]]:
        try:
           
            if vt_symbol:
                my_symbol = symbol_ks2my(vt_symbol)
            else:
                my_symbol = None

            if not direction or not offset:
                side = None
            else:
                side = side_ks2my(direction, offset)

            my_status = None
            if status:
                my_status = []
                if KsStatus.NOTTRADED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.NOTTRADED]
                if KsStatus.CANCELLED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.CANCELLED]
                if KsStatus.REJECTED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.REJECTED]

                if KsStatus.PARTTRADED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.PARTTRADED]

                if KsStatus.ALLTRADED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.ALLTRADED]
            else:
                my_status = None

            # my_status = None
            yesterday = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
            # todo! my_status传入返回空
            # orders = self.trd_ctx.get_orders(symbol=my_symbol, start_time=yesterday, sec_type=None, states=my_status)
            orders = self.trd_ctx.get_orders(symbol=my_symbol, start_time=yesterday, sec_type=None, states=None)
        except Exception as e:
            error = self.get_error(vt_symbol, direction, offset, status, orderid, reference, e=e)
            return RET_ERROR, error
        
        ks_orders = [self.order_data_my2ks(x) for x in orders]
        if status:
            ks_orders = [x for x in ks_orders if x.status in status]
        if reference:
            ks_orders = [x for x in ks_orders if reference == x.reference]
        return RET_OK, ks_orders

        
    # 获取今日订单 # todo get_orders没有实现
    def query_open_orders(self, 
            vt_symbol: Optional[str]=None, 
            direction: Optional[KsDirection] = None, 
            offset: Optional[KsOffset] = None,
            status: Optional[list[KsStatus]] = None,
            orderid: Optional[str] = None,
            reference: Optional[str] = None
    ) -> tuple[RetCode, Union[list[MyOrderData], ErrorData]]:
        status = [KsStatus.SUBMITTING, KsStatus.NOTTRADED, KsStatus.PARTTRADED]
        return self.query_orders(
            vt_symbol=vt_symbol,
            direction=direction,
            offset=offset,
            orderid=orderid,
            status=status,
            reference=reference
        )


    # 关闭上下文连接
    def close(self):
        pass
        # self.quote_ctx.close()
        # self.trd_ctx.close()


        