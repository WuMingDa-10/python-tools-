const http = require('http');
const url = require('url');

// 简单的 API 服务
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    
    // 设置 CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // 路由处理
    if (path === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(`
<!DOCTYPE html>
<html>
<head>
    <title>AI 代码助手 API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .method { color: #fff; padding: 3px 8px; border-radius: 3px; font-size: 12px; }
        .get { background: #61affe; }
        .post { background: #49cc90; }
        code { background: #eee; padding: 2px 5px; }
    </style>
</head>
<body>
    <h1>🤖 AI 代码助手 API</h1>
    <p>免费 API 服务，支持代码生成、翻译、优化</p>
    
    <h2>API 端点</h2>
    
    <div class="endpoint">
        <span class="method get">GET</span> <code>/api/health</code>
        <p>健康检查</p>
    </div>
    
    <div class="endpoint">
        <span class="method post">POST</span> <code>/api/generate</code>
        <p>生成代码</p>
        <pre>{"prompt": "写一个Python排序算法"}</pre>
    </div>
    
    <div class="endpoint">
        <span class="method post">POST</span> <code>/api/translate</code>
        <p>翻译代码</p>
        <pre>{"code": "print('hello')", "from": "python", "to": "javascript"}</pre>
    </div>
    
    <h2>使用示例</h2>
    <pre>
curl -X POST http://localhost:3000/api/generate \\
  -H "Content-Type: application/json" \\
  -d '{"prompt": "写一个快速排序算法"}'
    </pre>
    
    <h2>支持这个项目</h2>
    <p>如果这个 API 对你有帮助，请考虑支持：</p>
    <ul>
        <li>☕ Ko-fi: <a href="https://ko-fi.com">请我喝咖啡</a></li>
        <li>💳 PayPal: <a href="https://paypal.me">PayPal.Me</a></li>
    </ul>
</body>
</html>
        `);
    } else if (path === '/api/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
    } else if (path === '/api/generate' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const { prompt } = JSON.parse(body);
                // 简单的代码生成逻辑
                const response = generateCode(prompt);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ code: response }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
    } else if (path === '/api/translate' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const { code, from, to } = JSON.parse(body);
                const translated = translateCode(code, from, to);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ translated }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found' }));
    }
});

function generateCode(prompt) {
    // 简单的代码生成模板
    if (prompt.includes('排序') || prompt.includes('sort')) {
        return `def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# 使用示例
arr = [3, 6, 8, 10, 1, 2, 1]
print(quicksort(arr))`;
    } else if (prompt.includes('斐波那契') || prompt.includes('fibonacci')) {
        return `def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# 使用示例
print(fibonacci(10))`;
    } else {
        return `# 根据提示: "${prompt}"
# 这是一个示例代码模板

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()`;
    }
}

function translateCode(code, from, to) {
    // 简单的代码翻译
    if (from === 'python' && to === 'javascript') {
        return code
            .replace(/def (\w+)\((.*?)\):/g, 'function $1($2) {')
            .replace(/print\(/g, 'console.log(')
            .replace(/# (.*)/g, '// $1')
            .replace(/elif/g, 'else if')
            .replace(/True/g, 'true')
            .replace(/False/g, 'false')
            .replace(/None/g, 'null');
    }
    return code;
}

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
    console.log('使用 localtunnel 暴露到互联网...');
});
