export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const query = url.searchParams.get("q") || "";
    
    if (!query) {
      return new Response(JSON.stringify({ error: "no query" }), {
        headers: { "Content-Type": "application/json" }
      });
    }
    
    const results = [];
    const BAIDU_AK = env.BAIDU_AK || "";
    const BING_KEY = env.BING_KEY || "";
    
    if (BAIDU_AK) {
      try {
        const baiduUrl = `https://openapi.baidu.com/rest/2.0/search/v2/search?q=${encodeURIComponent(query)}&ak=${BAIDU_AK}&pn=0&rn=10&ie=utf-8`;
        const baiduResp = await fetch(baiduUrl, { timeout: 5000 });
        const baiduData = await baiduResp.json();
        results.push({ engine: "baidu", data: baiduData });
      } catch (e) { results.push({ engine: "baidu", error: String(e) }); }
    }
    
    if (BING_KEY) {
      try {
        const bingUrl = `https://api.bing.microsoft.com/v7.0/search?q=${encodeURIComponent(query)}&count=10`;
        const bingResp = await fetch(bingUrl, {
          headers: { "Ocp-Apim-Subscription-Key": BING_KEY }
        });
        const bingData = await bingResp.json();
        results.push({ engine: "bing", data: bingData });
      } catch (e) { results.push({ engine: "bing", error: String(e) }); }
    }
    
    if (results.length === 0) {
      results.push({ 
        engine: "placeholder", 
        query, 
        message: "请配置 BAIDU_AK 或 BING_KEY 环境变量",
        hint: "Baidu: https://login.bce.baidu.com/ , Bing: https://azure.microsoft.com/"
      });
    }
    
    return new Response(JSON.stringify({ results, query, count: results.length }), {
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
};
