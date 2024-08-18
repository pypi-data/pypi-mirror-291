# sentry-plugin-alert-dingtalk

> Sentry 钉钉通知插件

## 安装

新版本在 self-hosted 目录的 `sentry/enhance-image.sh` 中加入 `pip install sentry-plugin-alert-dingtalk`
老版本在 onpremise 目录的 `sentry/requirements.txt` 中添加 `sentry-plugin-alert-dingtalk`

然后执行:

```sh
docker-compose stop
./install.sh
docker-compose up -d
```

## 使用

在项目的所有集成页面找到 `DingTalk-Alert` 插件，启用，并设置模板
