# first-item

## Pixiv App 下载工具 / Pixiv App Downloader

一个使用 [pixivpy3](https://github.com/upbit/pixivpy) 从 Pixiv 下载插图的命令行工具。  
A command-line tool for downloading illustrations from Pixiv using [pixivpy3](https://github.com/upbit/pixivpy).

### 环境要求 / Requirements

- Python 3.7+
- pip

### 安装 / Installation

```bash
pip install -r requirements.txt
```

### 获取 Refresh Token / Getting a Refresh Token

使用 Pixiv OAuth 登录获取 refresh token：  
Use Pixiv OAuth login to obtain a refresh token:

```bash
python -m pixivpy_async.utils get_token
```

或参考 [pixivpy3 文档](https://github.com/upbit/pixivpy#usage) 了解更多方式。  
Or refer to the [pixivpy3 documentation](https://github.com/upbit/pixivpy#usage) for more methods.

### 用法 / Usage

#### 下载单张插图 / Download a single illustration

```bash
python pixiv_downloader.py --refresh-token <your_token> --illust-id <illust_id>
```

#### 下载某用户的所有插图 / Download all illustrations by a user

```bash
python pixiv_downloader.py --refresh-token <your_token> --user-id <user_id>
```

#### 下载排行榜插图 / Download ranking illustrations

```bash
# 下载每日排行榜前 30 张（默认）/ Download top 30 from daily ranking (default)
python pixiv_downloader.py --refresh-token <your_token> --ranking

# 下载每周排行榜前 50 张 / Download top 50 from weekly ranking
python pixiv_downloader.py --refresh-token <your_token> --ranking --ranking-mode week --ranking-limit 50
```

#### 指定保存目录 / Specify output directory

```bash
python pixiv_downloader.py --refresh-token <your_token> --illust-id 12345678 --output-dir /path/to/save
```

### 排行榜模式 / Ranking Modes

| 模式 / Mode    | 说明 / Description     |
|----------------|------------------------|
| `day`          | 每日 / Daily           |
| `week`         | 每周 / Weekly          |
| `month`        | 每月 / Monthly         |
| `day_male`     | 每日（男性向）/ Daily (male) |
| `day_female`   | 每日（女性向）/ Daily (female) |
| `week_original`| 每周原创 / Weekly original |
| `week_rookie`  | 每周新人 / Weekly rookie |

### 完整参数 / All Options

```
usage: pixiv_downloader.py [-h] --refresh-token TOKEN [--output-dir DIR]
                           (--illust-id ID | --user-id ID | --ranking)
                           [--ranking-mode MODE] [--ranking-limit N]

optional arguments:
  --refresh-token TOKEN  Pixiv refresh token for authentication
  --output-dir DIR       Directory to save downloaded files (default: downloads)
  --illust-id ID         Download a single illustration by ID
  --user-id ID           Download all illustrations by a user
  --ranking              Download top-ranking illustrations
  --ranking-mode MODE    Ranking mode (default: day)
  --ranking-limit N      Maximum number of ranking illustrations to download (default: 30)
```