"""
Toon格式轉換工具

將JSON數據轉換為toon格式以減少token消耗
"""
from toon_format import encode, decode
import json
from typing import Union, Dict, List


def convert_json_to_toon(json_data: Union[str, dict, list]) -> str:
    """
    將JSON數據轉換為toon格式
    
    Args:
        json_data: JSON字符串或Python字典/列表
        
    Returns:
        toon格式的字符串
    """
    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            # 如果無法解析，直接返回原始字符串
            return json_data
    else:
        data = json_data
    
    try:
        return encode(data)
    except Exception as e:
        print(f"警告：toon轉換失敗：{e}，返回原始數據")
        return json.dumps(data, ensure_ascii=False) if not isinstance(json_data, str) else json_data


def convert_toon_to_json(toon_data: str) -> dict:
    """
    將toon數據轉換回JSON/Python字典
    
    Args:
        toon_data: toon格式的字符串
        
    Returns:
        Python字典
    """
    try:
        return decode(toon_data) # type: ignore
    except Exception as e:
        print(f"警告：toon解碼失敗：{e}")
        # 嘗試作為JSON解析
        try:
            return json.loads(toon_data)
        except:
            return {"error": "無法解析數據", "原始數據": toon_data}
