# summon-evolution 角色图片生成规则

## 皮肤架构总则

- 每个主题都有两套皮肤：**classic（经典）** 与 **refreshed（焕新）**，由 `state.skin` 切换、按主题记忆。
- **焕新 = 程序化手绘**，**经典 = gpt-image 生成贴图**。
- 现有主题：节奏盒子（classic，21 角色）、山海经（brainrot，11 角色）、我的世界（minecraft，17 角色）、**召唤神鲲（kun，18 角色）**、**召唤神龙（dragon，18 角色）**、**光之巨人（ultraman，18 角色，最高级=赛罗 zero）**、**圣斗士（saintseiya，18 角色，最高级=雅典娜 athena）**、**忍者乱太郎（ninja，18 角色，最高级=猫丸·觉醒 nyamaropower，即黑木的猫）**、**召唤水果（fruit，18 角色，从西瓜到荔枝）**。
- 主题在模式选择器里的顺序：**kun（神鲲）→ dragon（神龙）→ classic（节奏盒子）→ brainrot（山海经）→ minecraft（我的世界）→ ultraman（奥特曼）→ saintseiya（圣斗士）→ ninja（忍者乱太郎）→ fruit（召唤水果）**。神鲲排最前（用户明确要求）；奥特曼/圣斗士/忍者靠后（用户要求放在我的世界之后）；水果排最后（用户要求从西瓜开始、荔枝结束）。

## 经典（classic）：gpt-image 一张大图 + 切割

1. 不要一个角色一张图地生；用 **gpt-image（gpt-image-2，yunwu.ai 转接）一次生成一张网格大图**，包含该主题全部角色。
2. 网格要求：
   - 布局固定 **6 列 × 3 行** 等分格子；每格一个角色，居中，约占格子高度 80%，各角色比例一致。
   - 角色不足 18 个时，多余格子留空（纯背景）。
   - 提示词必带：统一风格、相同比例、pixel-art、纯色背景、无文字/数字/标签/轮廓/阴影/装饰，角色不得越格。
3. 切割用 Python + PIL：
   - 按整行/整列"近白像素占比"检测网格带，再取带间区域为格子，避免单行采样误判。
   - 对每格做内容 bbox 裁剪，等比缩放到 **1024×1024** 画布。
   - 输出到 `images/<theme>/classic/<role>.png`，文件名与 `MINECRAFT_LEVELS` 等 `role` 字段一一对应。
4. 背景处理（二选一，新增主题优先"切割后置透明"）：
   - 生成时让 gpt 用统一纯色背景（如浅蓝 `#B5E2FC`），切割后用脚本把背景置透明（diff<35 全透明、35–70 渐变）；
   - 或保留纯色背景，由游戏加载图片后用 JS 去除。
   - 现状：**minecraft classic 的 17 张 PNG 已直接在文件里置透明**（皮肤选择器缩略图裸 `<img>` 不会露底）；**已移除 JS 端 `stripBg`**——图片源已透明，逐像素二次处理纯属浪费。游戏内直接 `drawImage` 原图。
5. 尺寸：**全部主题的 classic 图统一等比缩到最长边 256**（方形图即 256×256，非方形保持宽高比）。游戏内绘制最大约 `92×3.2≈294px`，256 足够清晰；三个主题压缩后合计约 1.6MB（此前 minecraft 4MB + sprunki 5.3MB + brainrot 9.8MB ≈ 19MB）。生成大图（1024+）仅作切片源，不要直接给游戏用。
6. 代码接入：
   - `preload*Images()` 只预加载 classic 图片（refreshed 无需图片资源，避免 404）。
   - `drawCharacter` 的 classic 分支用 `drawImage` 绘制对应角色图。

## 焕新（refreshed）：程序化手绘

- **不使用图片**。角色由 canvas 程序化绘制：
  - 节奏盒子/山海经 → 对应 `draw*Character` 手绘函数；
  - 我的世界 → `drawMinecraftCharacter` 方块人画法。
- 皮肤选择器缩略图：仅需 `images/<theme>/refreshed/<首个角色>.png` 一张（可程序化生成），其余角色无需图片。

## fallback 规则

- **经典缺图 → 回退焕新手绘**：classic 图片加载失败（`img.complete && img.naturalWidth > 0` 不满足）时，调用对应的手绘 `draw*Character`，保证任何情况下都能渲染。
- 经典皮肤在"图片就绪"与"手绘兜底"两种状态下都应外观可接受。

## 生成工作流速查

1. 写 prompt 文件（含 6×3 网格 + 角色顺序 + 风格约束）→ 运行 `gpt-image.py --prompt-file <file> --out <theme>/_sheet.png`。
2. 运行切割脚本（检测网格带 → bbox → 1024 画布 → `images/<theme>/classic/`）。
3. 拼图预览 + 浏览器实测（经典/焕新 × 图片就绪/兜底 四组合）。
4. 清理临时脚本；`_sheet.png` 源图可保留在 `images/<theme>/` 下。

## 开发踩坑记录（务必遵守）

### gpt-image 生图

- API：gpt-image-2 走 yunwu.ai 转接，key 在 `e:\YuNotebooks\.trae\skills\ppt-master\.env`（`OPENAI_BASE_URL=https://yunwu.ai/v1`）。
- **直连超时必挂**：yunwu.ai 直连报 `WinError 10060`（连接超时）。必须带系统代理 `127.0.0.1:7897` 跑（`export http_proxy/https_proxy/all_proxy`）。urllib 会自动读环境变量，gpt-image.py 无需改代码。
- **沙箱会吞输出**：直接调 `gpt-image.py` 可能静默失败无输出。用 `nohup ... &` 重定向日志，或直接写 Python 脚本调用 API 并落盘。
- **大响应会被代理切断**（"Remote end closed connection without response"）：`--quality medium`（响应约 1.4MB），重试循环 `range(1,6)`、`--timeout 240`。
- 网格线不是纯白，实测约 `(253,253,254)`；格子背景也不是提示词里的精确色，实测 `(181,226,252)`。**不要假设颜色值，先跑分析脚本采样。**
- sheet 尺寸不保证是 1024 整数倍（实测 1536×1024），各列宽略有不均。

### 切割

- 用**整行/整列"近白像素占比"**检测网格带（阈值 >244，占比 >0.9），再取带间区域为格子；单行采样易误判。
- bbox 若从 `(0,0)` 开始说明格子切到了网格线残留；切完务必扫四边像素确认无白边（非背景像素数应为 0）。
- 内容检测用 `abs(r-bg[0])+abs(g-bg[1])+abs(b-bg[2]) > 60`，缩放用 `Image.LANCZOS`。
- **gpt 不保证画网格线**（神鲲实测 1692×930，纯背景无分隔线）：改用"内容密度"检测——逐行/逐列统计与背景 diff>60 的像素占比，按 >0.5% 聚成内容区段，取相邻区段中点作格线。注意区段边界可能等于图片宽高，遍历用半开区间 `range(c0,c1)` 防越界。
- **先缩放、后置透明**：若先置透明再 `LANCZOS` 缩放，透明像素残留的背景 RGB 会被混回内容边缘，形成近背景色光晕（18 张全中招）。顺序必须是 `crop -> resize -> 置透明`。
- **bbox 初始化必须用相对坐标**：`minx, miny, maxx, maxy = cell.width, cell.height, -1, -1`，不能拿格子的绝对坐标 `x1,y1,x0,y0` 作初值，否则除首格外的格子全裁错（只显示半个角色）。
- **列间距过窄时切 6 列会失败**（忍者图实测只有 2 个全空白带）：`segs` 少于预期时改用 `--even` 等分网格 + bbox 兜底（等分线为 `round(i*W/N)`）。
- **合并过近分割线**：gpt 偶尔画出横跨格子的薄装饰带（6px 宽），会让行方向多检出 1 条分割线。`grid_lines` 里丢弃与上一线间距 <20px 的伪线。
- **18 角色 prompt 的 Row 分配必须逐个核对**：忍者大图曾把 Row2 写成 8 个角色（13-14 误入 Row2）、Row3 只剩 4 个，生成图 6×3 错位。生成前先数 prompt 里 Row1/Row2/Row3 的角色个数=6/6/6。

### 代码接入三处必须同步

- 新增角色必须同时改：**`*_LEVELS`（进化链）+ `preload*Images()` 的 ROLES + `draw*Character` 的 case**。
  - 曾经只加了 case 忘了 LEVELS，导致游戏内进化链缺角色——浏览器实测才发现。
- 预加载**只加载 classic**：refreshed 皮肤纯手绘无图片，预加载不存在的图会产生 404 噪音（曾一次产生 16 条）。
- 焕新缩略图只需首角色一张（可程序化生成），否则皮肤选择器破图。
- 新增**主题**（mode）时，除 `*_LEVELS` 外还要同步 6 处：`SCENES`（专属场景，`stageOnly:true`）、`state.skinByMode`、`drawStaticScene` 场景分支、`drawSceneBg` 的 `pulseColors`、`MODE_NAMES/MODE_TAGLINES/MODE_ICONS`、`renderSkinSelector` 的 first/classicBase/refreshedBase、`startGame` 直入分支、`initModeSelector` 的模式数组与 LEVELS 分支（`updateTitle` 已统一负责 HUD 图标/标题/口号）。`drawCharacter` 的 img 分支判断也要把新主题排除在外。
- 直入式主题（brainrot/minecraft/kun/dragon/ultraman/saintseiya/ninja/fruit）不参与 `resolveSceneChoice` 随机场景，`state.scene` 直接指向专属场景 id（`stageOnly:true`）。新主题场景配色：dragon 凌霄云海 `#1B2A52`、ultraman 光之国度 `#1A2E4A`、saintseiya 圣域 `#2A2440`、ninja 忍术学园 `#2E3A2E`、fruit 果园星空 `#3A2F2A`。

### 验证与实测

- 浏览器实测用 evaluate 读取内部状态：如 `LEVELS.map(l=>l.name+':'+l.role)`（注意 LEVELS 是模块作用域 `let`，不在 window 上）。
- 四组合必须都测：经典/焕新 × 图片就绪/手绘兜底。
- 可通过 monkey-patch `ctx.drawImage` 统计，确认游戏内到底用的是图片还是手绘。

### 经典图加载性能（踩过坑）

- 根因：①每张 1024×1024 PNG 加载后在 `onload` 里跑 `stripBg` 逐像素循环（17 张 × 100 万像素），主线程被卡死，游戏开局卡顿、进化到新角色时图还没就绪 → 走手绘兜底；②17 张 1024 图共 4MB，加载慢。
- 处理：图片切片后直接置透明 + 缩到 **256×256**（总 0.5MB）；删除 JS 端 `stripBg`/`_clean`，`drawCharacter` 直接 `drawImage` 原图。
- 教训：**图片源处理能做的，不要在运行时逐像素做**；运行时 `onload` 回调里绝不放 O(N) 像素级循环。

### 本机环境

- 终端是 PowerShell：不支持 `&&`、heredoc、`2>/dev/null`。多用 `;` 分隔；git commit 用单引号字符串。
- `node --check` 不能直接查 .html：先用 Python 正则抽 `<script>` 到临时 .js 再检查，用完删除。
- 中文在 PowerShell 终端显示乱码是编码显示问题，文件本身 UTF-8 正常，不要据此改文件。
- Git：分支 `gh-pages`，远端 `YuLab-SMU/games`。

## 多设备适配（电脑浏览器 / 平板 / 手机）

- 目标：同一页面完整支持桌面、平板、手机三端，**移动端优先**，改样式时三端都要过一遍。
- 断点约定：≤900px 为平板/手机（折叠菜单、缩小面板）；≤600px 为手机（显示 joystick）；≤380px 为小屏。
- 主菜单：内容超一屏时用折叠块收纳，现为 `fold-mode / fold-scene / fold-difficulty / fold-skin` 四个区块；窄屏（≤900px）默认折叠"场景选择"与"难度选择"（省空间，用户要求）。`initMenuFolds()` 在 `init()` 和 `showMenu()` 里各调一次，每次回菜单按当前视口宽度重置折叠状态。
- overlay-panel 统一 `max-height: calc(100vh - 24px)` + `overflow-y: auto`，保证任意屏幕一屏内可滚动到底。
- joystick：手机端（≤600px）显示、桌面端隐藏，经 `@media` 控制。
