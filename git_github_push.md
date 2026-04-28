````md
# 🚀 Git + GitHub 从零到推送（ROS 项目实战完整流程）

> 适用于：你这种 **clone 别人项目 + 修改 + 上传到自己 GitHub** 的场景  
> 已帮你规避：大文件污染、嵌套仓库、token认证等常见坑

---

# 🧠 一、核心概念（必须理解）

## 1️⃣ Git 三个区域

- 工作区（你修改文件的地方）
- 暂存区（git add）
- 仓库（git commit）

---

## 2️⃣ clone vs 新建文件夹

| 操作 | 状态 |
|------|------|
| git clone | 已是 Git 仓库 |
| 新建文件夹 | 需要 git init |

---

## 3️⃣ Git 只适合存代码 ❗

❌ 不要放：
- `.bag`
- `.tar.gz`
- `build/`
- `log/`

---

# 🚨 二、问题背景（你遇到的）

你的项目：

- 总大小：10G
- `.git`：4.9G ❗（已污染）

👉 原因：大文件被加入 Git 历史

---

# 🧹 三、解决方案（重建干净仓库）

## 1️⃣ 复制项目

```bash
cd ~
cp -r kuavo-ros-opensource kuavo-clean
cd kuavo-clean
````

---

## 2️⃣ 删除旧 Git 历史

```bash
rm -rf .git
```

---

## 3️⃣ 修改 `.gitignore`

```bash
nano .gitignore
```

添加：

```gitignore
# ROS
build/
install/
log/

# 数据
*.bag
*.db3

# 压缩
*.tar.gz
*.zip
*.7z

# 图片（可选）
*.png
*.jpg
```

---

## 4️⃣ 初始化仓库

```bash
git init
```

---

## 5️⃣ 添加文件

```bash
git add .
```

---

## 6️⃣ 提交

```bash
git commit -m "clean project"
```

---

# ⚠️ 四、处理嵌套 Git 仓库（重要）

如果出现：

```text
warning: adding embedded git repository
```

执行：

```bash
git rm --cached -r -f src/apriltag
git rm --cached -r -f src/aws-robomaker-hospital-world

rm -rf src/apriltag/.git
rm -rf src/aws-robomaker-hospital-world/.git

git add .
git commit -m "fix nested repos"
```

---

# 🌐 五、创建 GitHub 仓库

在 GitHub：

### 设置：

* Repository name：随便
* Visibility：Private（推荐）
* ❗ 不勾选：

  * README
  * .gitignore
  * license

---

# 🔗 六、绑定远程仓库

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
```

---

# 🌿 七、处理分支问题

如果报错：

```text
error: src refspec main does not match
```

执行：

```bash
git branch -M main
```

---

# 🚀 八、推送代码

```bash
git push -u origin main
```

---

# 🔐 九、GitHub 登录（token）

## ❗ 不能用密码

👉 必须用 token

---

## ✅ 创建 token（推荐 classic）

路径：

```
GitHub → Settings
→ Developer settings
→ Personal access tokens
→ Tokens (classic)
→ Generate new token
```

---

## 设置：

* Name：随便
* Expiration：90 days 或 No expiration
* 勾选：

```
repo
```

---

## 使用：

```text
Username: GitHub用户名
Password: 粘贴token（不会显示）
```

---

# 💾 十、保存登录（强烈推荐）

```bash
git config --global credential.helper store
```

👉 以后不用再输入 token

---

# 🧪 十一、验证是否成功

成功后终端会显示：

```text
Enumerating objects...
Writing objects...
```

GitHub 页面会出现你的代码 ✅

---

# 📦 十二、仓库结构（标准 ROS）

```text
workspace/
├── src/        ✅
├── build/      ❌
├── install/    ❌
├── log/        ❌
├── bags/       ❌
```

---

# 🚨 十三、常见问题总结

## ❌ git add 很慢

👉 原因：大文件

✔ 解决：`.gitignore`

---

## ❌ push 失败

👉 原因：

* token问题
* 分支错误
* 地址错误

---

## ❌ 仓库巨大

👉 原因：`.git/objects`

✔ 解决：重建仓库

---

# 👍 最终总结

👉 Git 管代码
👉 数据不要进 Git
👉 token 代替密码
👉 `.gitignore` 是关键

---

# 🎯 你现在的状态

✔ 已清理仓库
✔ 已配置 Git
✔ 已准备 push

👉 **只差最后一步 push 就完全成功 🚀**

---

# 🔥 进阶建议（以后）

* 使用 SSH（免登录）
* 学习分支管理（main/dev）
* ROS workspace 标准化

---

```
```

