# 24 级 2026 年春季学期读书实践周 \- Git 与代码版本管理实践报告

姓名：刘一诺  

仓库地址：https://github\.com/EnochLiu8086/LiuyinuoDushushijian2026

## 一、学习资料来源及相关链接

- Git 官方文档：https://git\-scm\.com/doc

- Git 入门教程：https://www\.liaoxuefeng\.com/wiki/896043488029600

- GitHub 官方使用指南：https://docs\.github\.com/zh/get\-started

## 二、实践流程

### 1\. Git 环境配置与本地仓库创建

#### Git 安装

从 Git 官网下载 Windows 版本安装包，默认配置完成安装，通过 `git \-\-version` 验证安装成功。

#### 全局配置

```bash
git config --global user.name "EnochLiu8086"
git config --global user.email "13403458086@163.com"
```

#### 创建本地仓库

进入代码文件夹，执行`git init` 初始化本地 Git 仓库。

### 2\. 远程仓库建立与代码提交

1\. 在 GitHub 创建公开仓库：LiuyinuoDushushijian2026

2\. 关联本地与远程仓库

```bash
git remote add origin https://github.com/EnochLiu8086/LiuyinuoDushushijian2026.git
```

3\. 完成代码添加、提交、推送操作

```bash
git add .
git commit -m "提交信息"
git push -u origin main
```

## 三、提交记录说明

本次实践完成 3 次有效提交，结合仓库实际提交内容，具体说明如下：

1. 第一次提交：上传0401的全部代码，包含Demo文件夹、作文文件夹、EssayAnalysis\.py、freq\.py、word\_frequency\.py等基础代码文件，以及相关的结果文件（如essay\_analysis\_result\.json、freq\_result\_top100\.json）和图片文件，完成本地仓库初始化及基础代码的远程同步。

2. 第二次提交：新增:050501作业代码1，完善050501文件夹的初始结构，上传该作业相关的基础代码文件，确保代码分类清晰，与0401相关代码区分管理。

3. 第三次提交：新增:050501作业代码2，补充050501文件夹内的作业代码，完成该作业所有相关代码的上传，同时检查仓库文件结构，确保所有代码文件同步至远程仓库。

## 四、遇到的问题及解决方法

### 问题 1：git push 提示认证失败

- 原因：GitHub 开启 2FA 后，无法使用密码登录

- 解决：生成个人访问令牌（PAT），推送时用 PAT 代替密码

### 问题 2：git push 提示分支不存在

- 原因：本地未完成提交，无可用分支

- 解决：先执行 git commit 提交代码，再推送远程仓库

### 问题 3：移动 Git 文件夹后命令失效

- 原因：系统环境变量路径未更新

- 解决：重新配置系统 Path 环境变量，指向新的 Git 安装路径

## 五、Git 学习心得

通过本次读书实践周的 Git 学习，我掌握了版本管理工具的核心使用方法，完成了从环境配置、本地仓库创建、远程仓库关联到代码提交推送的全流程操作。

Git 解决了代码版本混乱、无法回溯的问题，让代码管理更加规范、高效。同时，我学会了排查安装、配置、推送过程中的常见问题，培养了工程化的代码管理意识，为后续的课程学习和项目开发打下了坚实基础。

