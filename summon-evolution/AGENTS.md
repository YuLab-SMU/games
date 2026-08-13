# summon-evolution 角色图片生成规则

> 角色图片已上移到 games 根下共享目录 `images/<theme>/`。图片生成/切割的通用规则见父级 [AGENTS.md](../AGENTS.md)。

## 皮肤架构总则

- 每个主题都有两套皮肤：**classic（经典）** 与 **refreshed（焕新）**，由 `state.skin` 切换、按主题记忆。
- **焕新 = 程序化手绘**，**经典 = gpt-image 生成贴图**。
- 现有主题：节奏盒子（classic，21 角色）、山海经（brainrot，11 角色）、我的世界（minecraft，17 角色）、**召唤神鲲（kun，18 角色）**、**召唤神龙（dragon，18 角色）**、**光之巨人（ultraman，18 角色，最高级=赛罗 zero）**、**圣斗士（saintseiya，18 角色，最高级=雅典娜 athena）**、**忍者乱太郎（ninja，18 角色，最高级=猫丸·觉醒 nyamaropower，即黑木的猫）**、**召唤水果（fruit，18 角色，从西瓜到荔枝）**、**召唤蛋仔（eggy，18 角色，从白蛋仔到蛋皇 eggking）**。
- 主题在模式选择器里的顺序：**kun（神鲲）→ dragon（神龙）→ classic（节奏盒子）→ brainrot（山海经）→ minecraft（我的世界）→ ultraman（奥特曼）→ fruit（召唤水果）→ eggy（召唤蛋仔）→ saintseiya（圣斗士）→ ninja（忍者乱太郎）**。神鲲排最前（用户明确要求）；奥特曼/圣斗士/忍者靠后（用户要求放在我的世界之后）；**水果与蛋仔放在圣斗士、乱太郎之前**（用户明确要求：把水果和蛋仔放在圣斗士和乱太郎前面）。

## 经典（classic）代码接入

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

## 开发踩坑记录（summon-evolution 特有）

### 代码接入三处必须同步

- 新增角色必须同时改：**`*_LEVELS`（进化链）+ `preload*Images()` 的 ROLES + `draw*Character` 的 case**。
  - 曾经只加了 case 忘了 LEVELS，导致游戏内进化链缺角色——浏览器实测才发现。
- 预加载**只加载 classic**：refreshed 皮肤纯手绘无图片，预加载不存在的图会产生 404 噪音（曾一次产生 16 条）。
- 焕新缩略图只需首角色一张（可程序化生成），否则皮肤选择器破图。
- 新增**主题**（mode）时，除 `*_LEVELS` 外还要同步 6 处：`SCENES`（专属场景，`stageOnly:true`）、`state.skinByMode`、`drawStaticScene` 场景分支、`drawSceneBg` 的 `pulseColors`、`MODE_NAMES/MODE_TAGLINES/MODE_ICONS`、`renderSkinSelector` 的 first/classicBase/refreshedBase、`startGame` 直入分支、`initModeSelector` 的模式数组与 LEVELS 分支（`updateTitle` 已统一负责 HUD 图标/标题/口号）。`drawCharacter` 的 img 分支判断也要把新主题排除在外。
- 直入式主题（brainrot/minecraft/kun/dragon/ultraman/saintseiya/ninja/fruit/eggy）不参与 `resolveSceneChoice` 随机场景，`state.scene` 直接指向专属场景 id（`stageOnly:true`）。新主题场景配色：dragon 凌霄云海 `#1B2A52`、ultraman 光之国度 `#1A2E4A`、saintseiya 圣域 `#2A2440`、ninja 忍术学园 `#2E3A2E`、fruit 果园星空 `#3A2F2A`、eggy 蛋仔乐园 `#3A2A4A`。

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
