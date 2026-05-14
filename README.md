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

## 部署到 GitHub Pages

仓库包含 `.github/workflows/pages.yml`。GitHub Pages 需要公开仓库，或账号计划支持私有仓库 Pages。

满足条件后，在 GitHub Actions 里手动运行 `Deploy HonKit to GitHub Pages`，它会构建 HonKit，并把 `doc/agent-best-practices/_book` 发布到 GitHub Pages。
