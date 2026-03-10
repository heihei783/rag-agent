from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import os
import requests

rag = RagSummarizeService()
api_key = os.getenv("AMAP_API_KEY")

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)



@tool(description="获取指定城市或地区的实时天气信息")
def get_weather(city: str) -> str:
    
    # 1. 查询行政区划代码 (adcode)
    # 高德天气 API 必须传入 adcode，不能直接传入中文名
    geo_url = f"https://restapi.amap.com/v3/config/district?keywords={city}&key={api_key}&subdistrict=0"
    
    try:
        geo_res = requests.get(geo_url, timeout=5).json()
        
        if geo_res["status"] == "1" and geo_res["districts"]:
            # 获取第一个匹配结果的 adcode
            adcode = geo_res["districts"][0]["adcode"]
            city_full_name = geo_res["districts"][0]["name"]
            
            # 2. 查询实时天气
            weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={adcode}&key={api_key}&extensions=base"
            weather_res = requests.get(weather_url, timeout=5).json()
            
            if weather_res["status"] == "1" and weather_res["lives"]:
                live = weather_res["lives"][0]
                return (f"{city_full_name}当前天气：{live['reporttime']}发布，"
                        f"天气{live['weather']}，温度{live['temperature']}°C，"
                        f"{live['winddirection']}风{live['windpower']}级，湿度{live['humidity']}%。")
            
        return f"未能查找到 '{city}' 的天气信息，请确认城市名称是否正确。"
        
    except Exception as e:
        return f"天气查询服务暂时不可用: {str(e)}" 



@tool(description="获取当前用户所在城市")
def get_user_location() -> str:
    # 高德 IP 定位接口
    url = f"https://restapi.amap.com/v3/ip?key={api_key}"
    try:
        res = requests.get(url).json()
        if res["status"] == "1":
            return res["city"]
        return "未知城市"
    except:
        return "定位失败"
    


if __name__ == "__main__":
    print(get_user_location())

