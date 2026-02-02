# Skill 创建流程图（图片版）

本目录包含 4 张详细的流程图，涵盖 OpenClaw Skill 创建的完整过程。

## 📊 流程图列表

### 1. 综合创建流程（全景图）
**文件**: `skill-creation-comprehensive.png`

这是最核心的流程图，展示从需求分析到迭代改进的完整六步法：

- **第1步**: 理解需求 - 收集具体使用示例
- **第2步**: 规划资源 - 决定需要 scripts/references/assets
- **第3步**: 初始化 - 运行 init_skill.py 生成结构
- **第4步**: 编辑内容 - 实现 SKILL.md 和资源文件
- **第5步**: 打包验证 - 运行 package_skill.py
- **第6步**: 迭代改进 - 在实际使用中优化

同时包含：
- 资源决策流程（scripts/references/assets）
- 加载机制概览（三级披露）
- 触发流程概览（六道关卡）

**适用场景**: 首次学习 Skill 创建流程时作为全局参考

---

### 2. 加载和触发流程（技术细节）
**文件**: `skill-loading-trigger.png`

展示 OpenClaw 如何发现、过滤和使用 Skills 的完整技术流程：

**加载阶段**:
- 扫描四个位置：workspace > local > plugin > bundled
- 加载所有 SKILL.md
- 解析 YAML Frontmatter
- 按优先级合并

**过滤阶段（六道关卡）**:
1. 平台检查（OS）
2. 二进制依赖（requires.bins / requires.anyBins）
3. 环境变量（requires.env）
4. 配置检查（requires.config）
5. 手动启用（skills.entries.enabled）
6. 白名单（bundled skills）

**运行时阶段**:
- 创建 SkillSnapshot
- 应用环境覆盖
- 构建 Skills XML
- 注入到系统提示
- 渐进式加载（Metadata → Body → References）

**适用场景**: 理解 Skill 过滤规则和加载机制

---

### 3. 资源组织决策树（内容规划）
**文件**: `skill-resource-decision.png`

帮助决定不同类型的内容应该放在哪里：

**决策流程**:
```
需要AI执行代码?
  ↓ 是 → 代码重复编写? → 是 → scripts/
  ↓ 否                    → 否 → SKILL.md内联

需要详细文档?
  ↓ 是 → 长度>500行? → 是 → references/
  ↓ 否                → 否 → 核心必读? → 是 → SKILL.md
                                    → 否 → references/

用于输出?
  ↓ 是 → 模板文件/图片字体/样板代码 → assets/

配置信息?
  ↓ 是 → 简短<100行 → Frontmatter metadata.openclaw
       → 较长>100行 → references/

使用指南?
  ↓ 是 → 核心工作流 → SKILL.md Body
       → 高级功能 → references/
       → API参考 → references/
```

**资源类型总结**:
- `scripts/`: 可执行脚本，重复使用的代码
- `references/`: 参考文档，按需加载
- `assets/`: 输出资源，不加载到上下文
- `SKILL.md Frontmatter`: 元数据配置，始终可见
- `SKILL.md Body`: 核心指令，触发时加载

**Token 消耗对比**:
- Level 1: Metadata ~25 tokens/skill（始终消耗）
- Level 2: Body ~1000 tokens（触发时消耗）
- Level 3: References（按需消耗）

**适用场景**: 设计 Skill 结构时决定内容组织方式

---

### 4. 验证和打包流程（质量保证）
**文件**: `skill-validation-packaging.png`

展示 `package_skill.py` 的 10 项验证检查和打包流程：

**验证清单（10项）**:

✅ **必须通过的检查**:
1. YAML Frontmatter 格式正确（--- 开头结尾）
2. 包含必需字段（name + description）
3. 命名规范（hyphen-case，小写+连字符）
4. 名称长度不超过 64 字符
6. description 长度 > 50 字符
7. 不包含 TODO 占位符
10. Body 内容非空

⚠️ **建议优化的检查**:
5. 目录名与 skill name 一致
8. description 包含触发场景说明（"Use when..."）
9. 所有 scripts/ 和 references/ 被引用
- Body 长度 < 500 行（建议）

**打包流程**:
1. 收集所有文件（SKILL.md + 资源目录）
2. 创建 ZIP 压缩包（保持目录结构）
3. 重命名为 .skill 扩展名
4. 输出到指定目录或当前目录

**适用场景**: 打包 Skill 前检查质量标准

---

## 🎯 快速导航

| 需求 | 推荐图表 |
|------|---------|
| **我是新手，想了解整体流程** | → 综合创建流程 |
| **我想知道如何组织内容** | → 资源组织决策树 |
| **我想理解 Skill 如何被加载和触发** | → 加载和触发流程 |
| **我想确保 Skill 质量** | → 验证和打包流程 |
| **我的 Skill 没被触发** | → 加载和触发流程（检查六道关卡） |
| **我不知道内容该放哪** | → 资源组织决策树 |
| **打包失败** | → 验证和打包流程（查看验证清单） |

## 📐 图片规格

- **宽度**: 2200-2400 像素
- **高度**: 2800-3200 像素（根据内容）
- **格式**: PNG
- **主题**: Neutral（中性配色）
- **大小**: 约 200-400 KB/张

## 🔗 相关文档

- **详细文档**: `skill-creation-flowcharts.md` - 包含 Mermaid 源码和详细说明
- **架构分析**: `skills-workspace-agent-analysis.md` - OpenClaw 整体架构分析

## 📝 使用建议

1. **打印参考**: 这些图表适合打印成 A3/A4 大小作为桌面参考
2. **多屏显示**: 在一个屏幕上显示图表，另一个屏幕编写代码
3. **团队培训**: 用于培训新成员理解 Skill 创建流程
4. **文档嵌入**: 可以嵌入到内部文档或 Wiki

## 🛠️ 重新生成

如需修改图表或重新生成，使用以下命令：

```bash
# 需要 Node.js 和 npx
cd /workspace/.agent

# 生成单个图表
npx -y @mermaid-js/mermaid-cli@latest \
  -i skill-creation-comprehensive.mmd \
  -o skill-creation-comprehensive.png \
  -t neutral \
  -w 2400 \
  -H 3000

# 生成所有图表
for file in *.mmd; do
  npx -y @mermaid-js/mermaid-cli@latest \
    -i "$file" \
    -o "${file%.mmd}.png" \
    -t neutral \
    -w 2400 \
    -H 3000
done
```

## 💡 Tips

- **缩放查看**: 图片分辨率较高，建议用图片查看器缩放查看细节
- **打印**: 建议打印在 A3 纸上以保证清晰度
- **分享**: 可以直接在 Slack、Teams、Notion 等平台中使用
- **更新**: 如果代码流程发生变化，记得更新对应的 .mmd 文件后重新渲染

---

**生成时间**: 2026-02-02  
**工具**: Mermaid CLI (@mermaid-js/mermaid-cli)  
**基于**: OpenClaw Skills 系统分析
