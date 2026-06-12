"""Scheduler - 数据同步定时任务"""
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# 延迟导入，避免启动时就需要 akshare
scheduler = None


def _get_scheduler():
    """延迟初始化 scheduler"""
    global scheduler
    if scheduler is not None:
        return scheduler

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()

        # 注册定时任务
        _register_jobs(scheduler)
        return scheduler
    except ImportError:
        logger.warning("APScheduler 未安装，定时任务不可用")
        return None


def _register_jobs(scheduler):
    """注册所有定时任务"""
    from apscheduler.triggers.cron import CronTrigger

    # 交易时段每 5 分钟同步实时行情
    scheduler.add_job(
        sync_market_data_job,
        trigger=CronTrigger(day_of_week='mon-fri', hour='9-11,13-14', minute='*/5'),
        id='sync_market_data',
        replace_existing=True,
    )

    # 每日收盘后同步机构预测
    scheduler.add_job(
        sync_institutional_forecast_job,
        trigger=CronTrigger(day_of_week='mon-fri', hour='16', minute='0'),
        id='sync_institutional_forecast',
        replace_existing=True,
    )

    # 每日收盘后同步 K 线
    scheduler.add_job(
        sync_kline_job,
        trigger=CronTrigger(day_of_week='mon-fri', hour='16', minute='30'),
        id='sync_kline',
        replace_existing=True,
    )


def sync_market_data_job():
    """同步全市场实时行情"""
    logger.info("开始同步实时行情...")
    try:
        from infrastructure.data_sources.akshare_adapter import AkShareAdapter
        from infrastructure.database.connection import get_sync_session
        from infrastructure.database.models import MarketDataModel
        import pandas as pd

        df = AkShareAdapter.get_realtime_market()
        if df.empty:
            logger.warning("实时行情数据为空")
            return

        db = get_sync_session()
        try:
            today = datetime.now().date()
            for _, row in df.iterrows():
                ticker = str(row.get("ticker", "")).strip()
                if not ticker:
                    continue

                # 删除当天旧数据
                db.query(MarketDataModel).filter(
                    MarketDataModel.ticker == ticker,
                    MarketDataModel.trade_date == today
                ).delete()

                record = MarketDataModel(
                    ticker=ticker,
                    trade_date=today,
                    latest_price=float(row.get("latest_price", 0) or 0),
                    change_pct=float(row.get("change_pct", 0) or 0),
                    volume=int(row.get("volume", 0) or 0),
                    market_cap=float(row.get("market_cap", 0) or 0),
                    turnover=float(row.get("turnover", 0) or 0),
                )
                db.add(record)

            db.commit()
            logger.info(f"同步了 {len(df)} 条实时行情数据")
        except Exception as e:
            db.rollback()
            logger.error(f"保存实时行情失败: {e}")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"同步实时行情任务异常: {e}")


def sync_institutional_forecast_job():
    """同步机构预测"""
    logger.info("开始同步机构预测...")
    try:
        from infrastructure.data_sources.akshare_adapter import AkShareAdapter
        from infrastructure.data_sources.zhitu_adapter import ZhituAdapter
        from infrastructure.database.connection import get_sync_session
        from infrastructure.database.models import StockModel, InstitutionalForecastModel, MarketDataModel

        db = get_sync_session()
        try:
            stocks = db.query(StockModel).all()
            today = datetime.now().date()

            for stock in stocks:
                ticker = stock.ticker
                try:
                    yjyg_df = AkShareAdapter.get_institutional_forecast(ticker)
                    target_data = ZhituAdapter.get_target_price(ticker)

                    if yjyg_df.empty and not target_data:
                        continue

                    # 删除旧数据
                    db.query(InstitutionalForecastModel).filter(
                        InstitutionalForecastModel.ticker == ticker,
                        InstitutionalForecastModel.report_date == today
                    ).delete()

                    eps_neutral = None
                    net_profit_growth = None
                    source_count = None

                    if not yjyg_df.empty:
                        row = yjyg_df.iloc[0]
                        eps_val = row.get("eps_forecast_neutral")
                        eps_neutral = float(eps_val) if pd.notna(eps_val) else None

                        npg_val = row.get("net_profit_growth")
                        net_profit_growth = float(npg_val) / 100 if pd.notna(npg_val) else None

                        sc_val = row.get("source_count")
                        source_count = int(sc_val) if pd.notna(sc_val) else None

                    # 计算 PEG
                    peg = None
                    if net_profit_growth and net_profit_growth > 0:
                        from infrastructure.database.models import ValuationModel
                        val = db.query(ValuationModel).join(
                            StockModel, StockModel.id == ValuationModel.stock_id
                        ).filter(StockModel.ticker == ticker).first()
                        if val and val.pe_ttm:
                            peg = val.pe_ttm / (net_profit_growth * 100)

                    # 计算上涨空间
                    upside_opt = upside_neu = upside_pes = None
                    if target_data:
                        tp_opt = target_data.get("target_price_optimistic")
                        tp_neu = target_data.get("target_price_neutral")
                        tp_pes = target_data.get("target_price_pessimistic")

                        market = db.query(MarketDataModel).filter(
                            MarketDataModel.ticker == ticker
                        ).order_by(MarketDataModel.trade_date.desc()).first()

                        if market and market.latest_price and market.latest_price > 0:
                            if tp_opt:
                                upside_opt = (tp_opt - market.latest_price) / market.latest_price
                            if tp_neu:
                                upside_neu = (tp_neu - market.latest_price) / market.latest_price
                            if tp_pes:
                                upside_pes = (tp_pes - market.latest_price) / market.latest_price

                    record = InstitutionalForecastModel(
                        ticker=ticker,
                        report_date=today,
                        eps_forecast_neutral=eps_neutral,
                        net_profit_growth=net_profit_growth,
                        target_price_optimistic=target_data.get("target_price_optimistic") if target_data else None,
                        target_price_neutral=target_data.get("target_price_neutral") if target_data else None,
                        target_price_pessimistic=target_data.get("target_price_pessimistic") if target_data else None,
                        source_count=source_count or (target_data.get("source_count") if target_data else None),
                        source_names=str(target_data.get("source_names", [])) if target_data else None,
                        peg=peg,
                        upside_optimistic=upside_opt,
                        upside_neutral=upside_neu,
                        upside_pessimistic=upside_pes,
                    )
                    db.add(record)
                except Exception as e:
                    logger.error(f"处理 {ticker} 预测数据失败: {e}")
                    continue

            db.commit()
            logger.info(f"机构预测同步完成，处理 {len(stocks)} 只股票")
        except Exception as e:
            db.rollback()
            logger.error(f"保存机构预测失败: {e}")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"同步机构预测任务异常: {e}")


def sync_kline_job():
    """同步日 K 线"""
    logger.info("开始同步 K 线...")
    try:
        from infrastructure.data_sources.akshare_adapter import AkShareAdapter
        from infrastructure.database.connection import get_sync_session
        from infrastructure.database.models import KlineDailyModel, StockModel

        db = get_sync_session()
        try:
            stocks = db.query(StockModel).all()
            for stock in stocks:
                ticker = stock.ticker
                try:
                    df = AkShareAdapter.get_daily_kline(ticker, days=90)
                    if df.empty:
                        continue

                    for _, row in df.iterrows():
                        trade_date = row.get("trade_date")
                        if isinstance(trade_date, str):
                            trade_date = datetime.strptime(trade_date, "%Y-%m-%d").date()

                        existing = db.query(KlineDailyModel).filter(
                            KlineDailyModel.ticker == ticker,
                            KlineDailyModel.trade_date == trade_date
                        ).first()

                        if existing:
                            continue

                        record = KlineDailyModel(
                            ticker=ticker,
                            trade_date=trade_date,
                            open=float(row.get("open", 0) or 0),
                            high=float(row.get("high", 0) or 0),
                            low=float(row.get("low", 0) or 0),
                            close=float(row.get("close", 0) or 0),
                            volume=int(row.get("volume", 0) or 0),
                        )
                        db.add(record)
                except Exception as e:
                    logger.error(f"同步 {ticker} K线失败: {e}")
                    continue

            db.commit()
            logger.info(f"K线同步完成，处理 {len(stocks)} 只股票")
        except Exception as e:
            db.rollback()
            logger.error(f"保存 K线失败: {e}")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"同步 K线任务异常: {e}")


def start_scheduler():
    """启动定时任务"""
    s = _get_scheduler()
    if s:
        s.start()
        logger.info("定时任务已启动")


def shutdown_scheduler():
    """关闭定时任务"""
    global scheduler
    if scheduler:
        scheduler.shutdown()
        logger.info("定时任务已关闭")
