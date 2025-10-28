from flask import Flask, render_template, request, jsonify
import tushare as ts
import pandas as pd
import json
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to Python path to ensure config can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import config
    TUSHARE_TOKEN = config.TUSHARE_TOKEN
except ImportError:
    print("Warning: config.py not found, using environment variable for TUSHARE_TOKEN")
    TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN', 'cd0342a926136018b801150b53f040b5175b7f785c0c0f092fc0c013')

app = Flask(__name__)

def init_tushare():
    """Initialize Tushare with your token"""
    ts.set_token(TUSHARE_TOKEN)
    return ts.pro_api()

def get_stock_basic(pro, ts_code):
    """Get basic stock information"""
    try:
        df = pro.stock_basic(ts_code=ts_code, 
                            fields='ts_code,symbol,name,area,industry,market,list_date')
        return df.iloc[0].to_dict() if not df.empty else None
    except Exception as e:
        print(f"Error getting stock basic: {e}")
        return None

def get_income_data(pro, ts_code, years=3):
    """Get income statement data for the specified number of years"""
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y%m%d')
        
        df = pro.income(ts_code=ts_code, 
                       start_date=start_date, 
                       end_date=end_date,
                       fields='end_date,revenue,operate_profit,total_profit,n_income')
        
        # Sort by date and get the latest 3 years
        if not df.empty:
            df = df.sort_values('end_date', ascending=False)
            return df.head(years).to_dict('records')
        return []
    except Exception as e:
        print(f"Error getting income data: {e}")
        return []

def get_daily_basic(pro, ts_code):
    """Get daily basic data including valuation metrics"""
    try:
        trade_date = datetime.now().strftime('%Y%m%d')
        df = pro.daily_basic(ts_code=ts_code, 
                            trade_date=trade_date,
                            fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,total_mv')
        
        return df.iloc[0].to_dict() if not df.empty else None
    except Exception as e:
        print(f"Error getting daily basic: {e}")
        return None

def get_balance_sheet(pro, ts_code):
    """Get balance sheet data for equity analysis"""
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        df = pro.balancesheet(ts_code=ts_code, 
                             end_date=end_date,
                             fields='end_date,total_assets,total_liab,total_equity')
        
        return df.iloc[0].to_dict() if not df.empty else None
    except Exception as e:
        print(f"Error getting balance sheet: {e}")
        return None

def get_historical_prices(pro, ts_code, days=365):
    """Get historical price data for charting"""
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        df = pro.daily(ts_code=ts_code, 
                      start_date=start_date, 
                      end_date=end_date,
                      fields='trade_date,open,high,low,close,vol')
        
        if not df.empty:
            df = df.sort_values('trade_date')
            return df.to_dict('records')
        return []
    except Exception as e:
        print(f"Error getting historical prices: {e}")
        return []

def predict_future_trend(income_data, historical_prices):
    """Generate future trend predictions based on historical data"""
    if not income_data or not historical_prices:
        return None
    
    try:
        # Simple trend analysis based on income growth
        recent_revenue = [item['revenue'] for item in income_data[:2]]
        if len(recent_revenue) >= 2:
            revenue_growth = (recent_revenue[0] - recent_revenue[1]) / recent_revenue[1] * 100
        else:
            revenue_growth = 0
        
        # Price trend analysis
        recent_prices = [item['close'] for item in historical_prices[-30:]]
        if len(recent_prices) >= 10:
            price_trend = (recent_prices[-1] - recent_prices[0]) / recent_prices[0] * 100
        else:
            price_trend = 0
        
        # Generate prediction
        if revenue_growth > 20 and price_trend > 10:
            trend = "strong_bullish"
            confidence = "high"
            explanation = "公司业绩增长强劲，股价趋势向上，预计未来表现良好"
        elif revenue_growth > 10 and price_trend > 0:
            trend = "bullish"
            confidence = "medium"
            explanation = "业绩稳定增长，股价有上升趋势，未来可期"
        elif revenue_growth < -10 and price_trend < -5:
            trend = "bearish"
            confidence = "medium"
            explanation = "业绩下滑，股价走弱，需谨慎投资"
        else:
            trend = "neutral"
            confidence = "low"
            explanation = "业绩和股价表现平稳，建议观望"
        
        return {
            'trend': trend,
            'confidence': confidence,
            'explanation': explanation,
            'revenue_growth': round(revenue_growth, 2),
            'price_trend': round(price_trend, 2),
            'next_quarter_prediction': round(recent_revenue[0] * (1 + revenue_growth/100), 2) if recent_revenue else None
        }
    except Exception as e:
        print(f"Error in trend prediction: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    stock_code = request.form.get('stock_code')
    
    if not stock_code:
        return jsonify({'error': '请输入股票代码'})
    
    try:
        # Initialize Tushare
        print(f"Attempting to analyze stock: {stock_code}")
        pro = init_tushare()
        print("Tushare initialized successfully")
        
        # Get stock data
        stock_basic = get_stock_basic(pro, stock_code)
        print(f"Stock basic data: {stock_basic}")
        if not stock_basic:
            return jsonify({'error': f'未找到股票代码: {stock_code}。请确认格式正确（例如：000001.SZ, 600000.SH）'})
        
        income_data = get_income_data(pro, stock_code)
        print(f"Income data: {income_data}")
        daily_basic = get_daily_basic(pro, stock_code)
        print(f"Daily basic data: {daily_basic}")
        balance_sheet = get_balance_sheet(pro, stock_code)
        print(f"Balance sheet data: {balance_sheet}")
        
        # Get historical prices for charts
        historical_prices = get_historical_prices(pro, stock_code)
        print(f"Historical prices data points: {len(historical_prices) if historical_prices else 0}")
        
        # Generate trend predictions
        trend_prediction = predict_future_trend(income_data, historical_prices)
        print(f"Trend prediction: {trend_prediction}")
        
        # Calculate ROE if we have the data
        roe = None
        if daily_basic and balance_sheet:
            try:
                net_income = income_data[0].get('n_income') if income_data else None
                total_equity = balance_sheet.get('total_equity')
                if net_income and total_equity and total_equity > 0:
                    roe = (net_income / total_equity) * 100
            except:
                pass
        
        analysis_result = {
            'stock_basic': stock_basic,
            'income_data': income_data,
            'daily_basic': daily_basic,
            'balance_sheet': balance_sheet,
            'roe': roe,
            'historical_prices': historical_prices,
            'trend_prediction': trend_prediction
        }
        
        print(f"Analysis result prepared: {analysis_result}")
        return jsonify(analysis_result)
        
    except Exception as e:
        print(f"Error in analyze_stock: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'分析过程中出现错误: {str(e)}。请检查Tushare Token是否正确配置。'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
