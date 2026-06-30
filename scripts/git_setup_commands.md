# Git 初始化与同步命令

## 1. 初始化本地仓库

```bash
git init
git add .
git commit -m "初始化山河无名项目框架"
```

## 2. 添加极空间 Gitea 远程仓库

把 IP、用户名、仓库名替换成你自己的。

```bash
git remote add nas ssh://git@192.168.1.23:2222/你的用户名/shanhe-wuming.git
git branch -M main
git push -u nas main
```

## 3. 添加 GitHub 远程仓库，供 Codex 使用

```bash
git remote add github git@github.com:你的GitHub用户名/shanhe-wuming.git
git push -u github main
```

## 4. 日常提交

```bash
git add .
git commit -m "完善第一章礼崩之世主线大纲"
git push nas main
git push github main
```

## 5. 查看远程

```bash
git remote -v
```

## 6. 如果远程地址写错

```bash
git remote remove nas
git remote add nas ssh://git@你的极空间IP:2222/你的用户名/shanhe-wuming.git
```
