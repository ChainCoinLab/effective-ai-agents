# AI Learn

AI 工程学习笔记与 Agent 最佳实践文档。

## 本地构建

```bash
npm install
npm run docs:build
```

构建产物位于：

```text
doc/agent-best-practices/_book
```

## 本地预览

```bash
npm run docs:serve
```

## 部署到 Cloudflare Workers 静态站点

先登录 Cloudflare：

```bash
npx wrangler login
```

然后部署：

```bash
npm run deploy:worker
```

Workers 静态资源目录由 `wrangler.toml` 指定为 `doc/agent-best-practices/_book`。
