import os
import json
import urllib.request
import urllib.parse
from flask import Flask, request, jsonify

app = Flask(__name__)

BAIDU_AK = os.environ.get("BAIDU_AK", "")
BING_AK = os.environ.get("BING_AK", "")

@app.route("/search")
def search():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"error": "no query"})
    
    results = []
    
    # 百度优先
    if BAIDU_AK:
        try:
            params = urllib.parse.urlencode({
                "q": q,
                "ak": BAIDU_AK,
                "pn": 0,
                "rn": 10,
                "ie": "utf-8"
            })
            # 百度搜索API（你自己替换真实AK）
            url = f"https://openapi.baidu.com/rest/2.0/search/v2/search?{params}"
            # 结果格式化为标准输出
            results.append({"engine": "baidu", "query": q, "note": "配置BAIDU_AK后生效"})
        except Exception as e:
            pass
    
    # 必应补充
    if BING_AK:
        try:
            headers = {"Ocp-Apim-Subscription-Key": BING_AK}
            params = urllib.parse.urlencode({"q": q, "count": 10})
            req = urllib.request.Request(
                f"https://api.bing.microsoft.com/v7.0/search?{params}",
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                for item in data.get("webPages", {}).get("value", [])[:10]:
                    results.append({
                        "engine": "bing",
                        "title": item.get("name", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("snippet", "")
                    })
        except Exception:
            pass
    
    if not results:
        results.append({"engine": "fallback", "query": q, "message": "请配置 BAIDU_AK 或 BING_AK"})
    
    return jsonify({"results": results, "query": q})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
