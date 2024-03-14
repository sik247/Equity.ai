import numpy as np
import pandas as pd
import datetime
import sqlite3


### 비율을 입력하면 백테스팅을 수행해주는 코드입니다. 거래비용을 고려합니다.
### 일별 비율을 입력할수도 있고, 주별이나 월별 또는 다른 임의의 시점마다 추정된 비율을 입력할 수 있습니다.
def backtest(df_wgt, trade_cost=0.001):
    
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # 주식 데이터를 불러옵니다.
    raw_data = pd.read_csv('data/raw_data_ts.csv')
    
    # 무위험수익률로 사용할 3개월 단기 미국 국채 이자율 데이터를 불러옵니다.
    risk_free_data = pd.read_csv('data/TB3MS_daily.csv')
    risk_free_data = risk_free_data.loc[:, ['eval_d', 'value_']]
    risk_free_data['eval_d'] = pd.to_datetime(risk_free_data['eval_d'])
    risk_free_data['close_'] = (1. + risk_free_data['value_'] / 100. / 365).cumprod()
    risk_free_data = risk_free_data.drop(columns=['value_'])

    data_ = raw_data.loc[:, ['code_', 'eval_d', 'close_']]
    data_['eval_d'] = pd.to_datetime(data_['eval_d'])

    df_date = data_[['code_', 'eval_d']]
    df_date['next_d'] = df_date.groupby('code_')['eval_d'].shift(-1)

    df_prc = pd.merge(data_, risk_free_data, on='eval_d')
    df_prc.columns = ['code_', 'eval_d', 'close_', 'close_rf']

    df_target = df_wgt.copy()
    df_target['eval_d'] = pd.to_datetime(df_target['eval_d'])
    
        
    df_date.to_sql('date_', conn, index=False)
    df_prc.to_sql('prc_', conn, index=False)
    df_target.to_sql('target_wgt', conn, index=False)
    sql_ = f"""
        select  code_
                , eval_d
                , case when count(eval_d) = 2 then  abs(sum(case when rebal_d = eval_d then wgt_ else -wgt_ end)) else 0 end as turnover
                , sum(y) as y
                , sum(y) - {trade_cost} * (case when count(eval_d) = 2 then  abs(sum(case when rebal_d = eval_d then wgt_ else -wgt_ end)) else 0 end) as y_after_cost
            from (
                select code_, port_d, rebal_d, eval_d, wgt_, ifnull(cum_idx / lag(cum_idx, 1) over (partition by code_, port_d, rebal_d order by eval_d) - 1., 0.) as y
                    from (
                        -- 다음 리밸런싱 전까지 가격변동 반영
                        select d.code_, d.port_d, d.rebal_d, d.next_rebal_d, pt.eval_d, d.wgt_, d.wgt_ * Pt.close_ / P0.close_ + (1 - d.wgt_) * Pt.close_rf / P0.close_rf as cum_idx
                            from (
                                -- port_d 기준 데이터로 산출된 타겟비중값을 다음날 종가로 진입하여, 그다음 리밸런싱 다음날까지 투자
                                select  a.code_
                                        , a.eval_d as port_d
                                        , next_d as rebal_d
                                        , ifnull(lead(next_d, 1) over (partition by a.code_ order by next_d), '9999-01-01') as next_rebal_d
                                        , wgt_
                                        from (
                                            -- 최초 현금 100%보유 추가
                                            select code_, DATETIME(min_d, '-1 days') as eval_d, 0. as wgt_ 
                                                from (select code_, min(eval_d) as min_d from target_wgt group by code_) A
                                            union
                                            select * from target_wgt                 
                                        ) A
                                        join date_ B
                                        on a.code_ = b.code_ and a.eval_d = b.eval_d
                            ) D
                            join prc_ P0
                            on d.code_ = p0.code_ and d.rebal_d = p0.eval_d
                            join prc_ Pt
                            on d.code_ = pt.code_ and d.rebal_d <= Pt.eval_d and d.next_rebal_d >= Pt.eval_d
                    ) A
            ) A
            group by a.code_, a.eval_d
            order by a.code_, A.eval_d    
    """

    df_y =  pd.read_sql_query(sql_, conn)
    df_y['eval_d'] = pd.to_datetime(df_y['eval_d'])
#     df_y['idx'] = (1. + df_y['y']).cumprod()
#     df_y['idx_after_cost'] = (1. + df_y['y_after_cost']).cumprod()
    
    df_y['idx'] = (1+df_y.set_index('code_')['y']).groupby(level=0).cumprod().reset_index(drop=True)
    df_y['idx_after_cost'] = (1+df_y.set_index('code_')['y_after_cost']).groupby(level=0).cumprod().reset_index(drop=True)
    conn.close()
    
    return df_y



def backtest_fast(df_wgt, trade_cost=0.001):
    # 주식 데이터를 불러옵니다.
    raw_data = pd.read_csv('data/raw_data_ts.csv')
    
    # 무위험수익률로 사용할 3개월 단기 미국 국채 이자율 데이터를 불러옵니다.
    risk_free_data = pd.read_csv('data/tb3ms_daily_preprocessed.csv')
    risk_free_data = risk_free_data.loc[:, ['eval_d', 'value_']]
    #Change 1 
    # risk_free_data['eval_d'] = pd.to_datetime(risk_free_data['eval_d'])
    risk_free_data['eval_d'] = pd.to_datetime(risk_free_data['eval_d'])
    risk_free_data['close_'] = (1. + risk_free_data['value_'] / 100. / 365).cumprod()
    risk_free_data = risk_free_data.drop(columns=['value_'])

    df_target = df_wgt.copy()
    df_target['eval_d'] = pd.to_datetime(df_target['eval_d'])


    # 최초 현금100% 보유 추가 
    df_target0 = df_target.groupby('code_')['eval_d'].min().apply(lambda x: x + datetime.timedelta(days=-1)).reset_index()
    df_target0['wgt_'] = 0.
    
    df_target = pd.concat([df_target0, df_target], axis=0).sort_values(['code_', 'eval_d'])
    df_target['port_d'] = df_target['eval_d']


    data_ = raw_data.loc[:, ['code_', 'eval_d', 'close_']]
    #Change 2 
    # data_['eval_d'] = pd.to_datetime(data_['eval_d'])
    data_['eval_d'] = pd.to_datetime(data_['eval_d'], format='%m/%d/%y')
    # df_target 기준으로 데이터 최소날짜 맞추기 
    selected = pd.merge(data_, df_target[['code_', 'eval_d', 'port_d']], on=['code_', 'eval_d'], how='left').groupby(['code_']).ffill().dropna().index
    data_ = data_.loc[selected]

    df_date = data_[['code_', 'eval_d']]
    df_date['next_d'] = df_date.groupby('code_')['eval_d'].shift(-1)

    df_prc = pd.merge(data_, risk_free_data, on='eval_d')
    df_prc.columns = ['code_', 'eval_d', 'close_', 'close_rf']

    # 리밸런싱 시작 날짜값(열) 추가
    df_target_w_d0 = pd.merge(df_date, df_target, how='inner', on = ['code_', 'eval_d']).rename(columns={'next_d': 'rebal_d0'})
    df_target_w_d = pd.merge(df_date.loc[:, ['code_', 'eval_d', 'next_d']], df_target_w_d0, how='left', on = ['code_', 'eval_d']).ffill().rename(columns={'next_d': 'rebal_d'}).drop(columns=['eval_d'])
    
    # 다음 리밸런싱 날짜(행) 추가 
    df_target_w_d0['next_rebal_d0'] = df_target_w_d0['rebal_d0'].shift(-1)
    df_target_w_d = pd.concat([df_target_w_d, df_target_w_d0.loc[:, ['code_', 'next_rebal_d0', 'rebal_d0', 'wgt_', 'port_d']].rename(columns={'next_rebal_d0': 'rebal_d'})], axis=0).sort_values(['code_', 'port_d', 'rebal_d']).reset_index(drop=True)

    df_target_w_d['prc_0'] = pd.merge(df_target_w_d[['code_', 'rebal_d0']], df_prc, how='left', left_on=['code_', 'rebal_d0'], right_on=['code_', 'eval_d'])[['close_']]
    df_target_w_d['prc_rf_0'] = pd.merge(df_target_w_d[['code_', 'rebal_d0']], df_prc, how='left', left_on=['code_', 'rebal_d0'], right_on=['code_', 'eval_d'])[['close_rf']]
    df_target_w_d['prc_t'] = pd.merge(df_target_w_d[['code_', 'rebal_d']], df_prc, how='left', left_on=['code_', 'rebal_d'], right_on=['code_', 'eval_d'])[['close_']]
    df_target_w_d['prc_rf_t'] = pd.merge(df_target_w_d[['code_', 'rebal_d']], df_prc, how='left', left_on=['code_', 'rebal_d'], right_on=['code_', 'eval_d'])[['close_rf']]
    df_target_w_d['cum_idx'] = df_target_w_d['prc_t'] / df_target_w_d['prc_0'] * df_target_w_d['wgt_'] +  df_target_w_d['prc_rf_t'] / df_target_w_d['prc_rf_0'] * (1-df_target_w_d['wgt_'])
    df_target_w_d['cum_idx_p'] = df_target_w_d['prc_t'] / df_target_w_d['prc_0'] * df_target_w_d['wgt_']
    df_target_w_d['y'] = df_target_w_d.groupby(['code_', 'port_d'])['cum_idx'].pct_change().fillna(0.)
    df_target_w_d['next_rebal_d'] = df_target_w_d.groupby('code_')['rebal_d0'].shift(-1)

    df_turnover_base = df_target_w_d[(df_target_w_d.rebal_d == df_target_w_d.next_rebal_d) | (df_target_w_d.rebal_d == df_target_w_d.rebal_d0)]
    df_turnover_base['calc_wgt'] = (df_turnover_base['cum_idx_p'] / df_turnover_base['cum_idx']) * ((df_turnover_base['rebal_d']== df_turnover_base['rebal_d0']) * 2 - 1)


    pf_y = df_target_w_d.groupby(['code_', 'rebal_d'])['y'].sum().reset_index()
    pf_turnover = df_turnover_base.groupby(['code_', 'rebal_d'])['calc_wgt'].sum().abs().reset_index().rename(columns={'calc_wgt': 'turnover'})
    
    df_y = pd.merge(pf_turnover, pf_y, how='right', on=['code_', 'rebal_d']).fillna(0.).rename(columns={'rebal_d': 'eval_d'}).reset_index(drop=True)
    df_y['y_after_cost'] = df_y['y'] - trade_cost * df_y['turnover']    
    df_y['idx'] = (1+df_y.set_index('code_')['y']).groupby(level=0).cumprod().reset_index(drop=True)
    df_y['idx_after_cost'] = (1+df_y.set_index('code_')['y_after_cost']).groupby(level=0).cumprod().reset_index(drop=True)

    return df_y



def make_summary(df_y):
    
    # 무위험수익률로 사용할 3개월 단기 미국 국채 이자율 데이터를 불러옵니다.
    risk_free_data = pd.read_csv('data/tb3ms_daily_preprocessed.csv')
    risk_free_data = risk_free_data.loc[:, ['eval_d', 'value_']]
    #change 3 
    risk_free_data['eval_d'] = pd.to_datetime(risk_free_data['eval_d'])

    # risk_free_data['eval_d'] = pd.to_datetime(risk_free_data['eval_d'])
    risk_free_data['close_'] = (1. + risk_free_data['value_'] / 100. / 365).cumprod()
    risk_free_data = risk_free_data.drop(columns=['value_']).set_index('eval_d')
    
    
    out = list()
    
    for key in df_y.code_.unique():
        res = df_y.loc[df_y.code_ == key].copy().set_index('eval_d')
        y_month = res['idx_after_cost'].resample('M').last().pct_change()
        rf_month = risk_free_data.reindex(y_month.index).pct_change()['close_']
        # MDD, CAGR, Volatility, Sharpe 값을 계산합니다.
        mdd = (res['idx_after_cost'] / res['idx_after_cost'].cummax() - 1).min()
        mean = y_month.mean() * 12
        rf_mean = rf_month.mean() * 12
        vol = y_month.std() * np.sqrt(12)
        sharpe = (mean - rf_mean) / vol 
        
        # Excess Return 기준 통계량을 계산합니다. 
        y_daily = res['idx_after_cost'].pct_change()
        rf_daily = risk_free_data.reindex(y_daily.index).pct_change()['close_']        
        ex_idx_daily = (1. + (y_daily - rf_daily).fillna(0.)).cumprod()
        ex_idx_monthly = ex_idx_daily.resample('M').last().pct_change()
        ex_mdd = (ex_idx_daily / ex_idx_daily.cummax() - 1).min()
        ex_mean = ex_idx_monthly.mean() * 12
        ex_vol = ex_idx_monthly.std() * np.sqrt(12)

        # 계산 결과를 저장합니다.
        results = {}
        results['RETURN'] = res['idx_after_cost'].iloc[-1]
        results['MDD'] = mdd
        results['MEAN'] = mean
        results['VOL'] = vol
        results['exMDD'] = ex_mdd
        results['exMEAN'] = ex_mean
        results['exVOL'] = ex_vol
        results['SHARPE'] = sharpe 
        results['TURNOVER'] = res['turnover'].resample('Y').sum().mean()  # 연간 회전율 평균
        out.append(pd.DataFrame(results, index=[key]))
        
    return pd.concat(out, axis=0)

