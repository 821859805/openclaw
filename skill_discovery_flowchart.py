#!/usr/bin/env python3
"""Generate a flowchart for Skill discovery and execution process"""

from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Skill Discovery and Execution', format='png')
dot.attr(rankdir='TB', splines='polyline', nodesep='0.5', ranksep='0.6', dpi='150')
dot.attr('node', fontname='SimHei,Arial', fontsize='11')
dot.attr('edge', fontname='SimHei,Arial', fontsize='9')

# ==================== 第一部分：会话启动时的 Skill 加载 ====================
dot.node('title1', '📂 第一阶段：会话启动 - Skill 加载', shape='plaintext', fontsize='14', fontcolor='#1565C0')

with dot.subgraph(name='cluster_load') as c:
    c.attr(label='会话启动时', style='rounded,filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')
    
    c.node('load_start', '会话启动', shape='ellipse', style='filled', fillcolor='#BBDEFB')
    
    # 加载 Skills 的四个来源
    c.node('load_bundled', '加载内置 Skills\n(bundled)', shape='box', style='rounded,filled', fillcolor='#E1F5FE')
    c.node('load_extra', '加载额外目录 Skills\n(extraDirs + plugins)', shape='box', style='rounded,filled', fillcolor='#E1F5FE')
    c.node('load_managed', '加载托管 Skills\n(~/.openclaw/skills)', shape='box', style='rounded,filled', fillcolor='#E1F5FE')
    c.node('load_workspace', '加载工作区 Skills\n(<workspace>/skills)', shape='box', style='rounded,filled', fillcolor='#E1F5FE')
    
    c.node('merge', '按优先级合并\n(workspace > managed > bundled > extra)', shape='box', style='rounded,filled', fillcolor='#B3E5FC')
    
    c.node('parse', '解析每个 SKILL.md\n提取 frontmatter 元数据', shape='box', style='rounded,filled', fillcolor='#B3E5FC')

# ==================== 第二部分：Skill 过滤 ====================
with dot.subgraph(name='cluster_filter') as c:
    c.attr(label='Skill 资格过滤', style='rounded,filled', fillcolor='#F3E5F5', color='#7B1FA2', penwidth='2')
    
    c.node('filter_start', '检查每个 Skill', shape='box', style='rounded,filled', fillcolor='#E1BEE7')
    
    c.node('check_enabled', '检查 config 中\nenabled 设置', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.3')
    c.node('check_bins', '检查 requires.bins\n(二进制依赖)', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.3')
    c.node('check_env', '检查 requires.env\n(环境变量)', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.3')
    c.node('check_config', '检查 requires.config\n(配置项)', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.3')
    c.node('check_os', '检查 os 平台\n(darwin/linux/win32)', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.3')
    
    c.node('skill_excluded', '排除该 Skill', shape='box', style='rounded,filled', fillcolor='#FFCDD2')
    c.node('skill_eligible', '加入 eligible 列表', shape='box', style='rounded,filled', fillcolor='#C8E6C9')

# ==================== 第三部分：构建系统提示词 ====================
with dot.subgraph(name='cluster_prompt') as c:
    c.attr(label='构建系统提示词', style='rounded,filled', fillcolor='#E8F5E9', color='#388E3C', penwidth='2')
    
    c.node('format_skills', 'formatSkillsForPrompt()\n生成 XML 格式列表', shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    c.node('xml_example', '&lt;available_skills&gt;\n  &lt;skill&gt;\n    &lt;name&gt;weather&lt;/name&gt;\n    &lt;description&gt;...&lt;/description&gt;\n    &lt;location&gt;path&lt;/location&gt;\n  &lt;/skill&gt;\n&lt;/available_skills&gt;', shape='note', style='filled', fillcolor='#DCEDC8', fontsize='9')
    c.node('inject_prompt', '注入到系统提示词\n## Skills (mandatory)', shape='box', style='rounded,filled', fillcolor='#A5D6A7')
    c.node('snapshot', '创建 SkillSnapshot\n(缓存到会话)', shape='box', style='rounded,filled', fillcolor='#A5D6A7')

# ==================== 第四部分：用户消息处理 ====================
dot.node('title2', '💬 第二阶段：用户消息 - Skill 触发', shape='plaintext', fontsize='14', fontcolor='#C62828')

with dot.subgraph(name='cluster_message') as c:
    c.attr(label='用户消息处理', style='rounded,filled', fillcolor='#FFF8E1', color='#FFA000', penwidth='2')
    
    c.node('user_msg', '用户发送消息', shape='ellipse', style='filled', fillcolor='#FFECB3')
    c.node('check_slash', '是否以 / 开头?', shape='diamond', style='filled', fillcolor='#FFE082', width='1.2')
    
    # 斜杠命令分支
    c.node('parse_cmd', '解析斜杠命令\n/skill_name [args]', shape='box', style='rounded,filled', fillcolor='#FFCC80')
    c.node('find_skill_cmd', '查找匹配的\nSkillCommandSpec', shape='box', style='rounded,filled', fillcolor='#FFCC80')
    c.node('skill_found', '找到匹配 Skill?', shape='diamond', style='filled', fillcolor='#FFE082', width='1.2')
    c.node('direct_invoke', '直接调用 Skill\n(跳过 LLM 判断)', shape='box', style='rounded,filled', fillcolor='#FFB74D')
    
    # 普通消息分支 - LLM 判断
    c.node('send_llm', '发送到 LLM\n(包含系统提示词)', shape='box', style='rounded,filled', fillcolor='#FFF59D')

# ==================== 第五部分：LLM Skill 选择 ====================
with dot.subgraph(name='cluster_llm') as c:
    c.attr(label='LLM Skill 选择', style='rounded,filled', fillcolor='#FCE4EC', color='#C2185B', penwidth='2')
    
    c.node('llm_scan', 'LLM 扫描\n<available_skills>\n中的 <description>', shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('llm_match', '是否有 Skill\n明确匹配任务?', shape='diamond', style='filled', fillcolor='#F48FB1', width='1.3')
    c.node('llm_select', '选择最具体的 Skill', shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('llm_read', '使用 read 工具\n读取 SKILL.md', shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('llm_no_skill', '不使用任何 Skill\n直接回复', shape='box', style='rounded,filled', fillcolor='#FFCDD2')

# ==================== 第六部分：Skill 执行 ====================
with dot.subgraph(name='cluster_exec') as c:
    c.attr(label='Skill 执行', style='rounded,filled', fillcolor='#E0F2F1', color='#00897B', penwidth='2')
    
    c.node('parse_skill', '解析 SKILL.md 指令', shape='box', style='rounded,filled', fillcolor='#B2DFDB')
    c.node('exec_workflow', '执行工作流程', shape='box', style='rounded,filled', fillcolor='#B2DFDB')
    
    c.node('use_scripts', '调用 scripts/\n中的脚本', shape='box', style='rounded,filled', fillcolor='#80CBC4')
    c.node('read_refs', '读取 references/\n中的文档', shape='box', style='rounded,filled', fillcolor='#80CBC4')
    c.node('use_assets', '使用 assets/\n中的资源', shape='box', style='rounded,filled', fillcolor='#80CBC4')
    
    c.node('generate_response', '生成回复', shape='box', style='rounded,filled', fillcolor='#4DB6AC')

# 结束
dot.node('end', '返回结果给用户', shape='ellipse', style='filled', fillcolor='#C8E6C9', color='#388E3C', penwidth='2')

# ==================== 连接边 ====================

# 第一阶段连接
dot.edge('title1', 'load_start', style='invis')
dot.edge('load_start', 'load_bundled', penwidth='1.5')
dot.edge('load_start', 'load_extra', penwidth='1.5')
dot.edge('load_start', 'load_managed', penwidth='1.5')
dot.edge('load_start', 'load_workspace', penwidth='1.5')
dot.edge('load_bundled', 'merge', penwidth='1.5')
dot.edge('load_extra', 'merge', penwidth='1.5')
dot.edge('load_managed', 'merge', penwidth='1.5')
dot.edge('load_workspace', 'merge', penwidth='1.5')
dot.edge('merge', 'parse', penwidth='1.5')

# 过滤连接
dot.edge('parse', 'filter_start', penwidth='1.5')
dot.edge('filter_start', 'check_enabled', penwidth='1.5')
dot.edge('check_enabled', 'skill_excluded', label=' 禁用 ', color='#E57373', fontcolor='#C62828')
dot.edge('check_enabled', 'check_bins', label=' 启用 ', color='#81C784', fontcolor='#2E7D32')
dot.edge('check_bins', 'skill_excluded', label=' 缺失 ', color='#E57373', fontcolor='#C62828')
dot.edge('check_bins', 'check_env', label=' 存在 ', color='#81C784', fontcolor='#2E7D32')
dot.edge('check_env', 'skill_excluded', label=' 缺失 ', color='#E57373', fontcolor='#C62828')
dot.edge('check_env', 'check_config', label=' 存在 ', color='#81C784', fontcolor='#2E7D32')
dot.edge('check_config', 'skill_excluded', label=' 不满足 ', color='#E57373', fontcolor='#C62828')
dot.edge('check_config', 'check_os', label=' 满足 ', color='#81C784', fontcolor='#2E7D32')
dot.edge('check_os', 'skill_excluded', label=' 不匹配 ', color='#E57373', fontcolor='#C62828')
dot.edge('check_os', 'skill_eligible', label=' 匹配 ', color='#81C784', fontcolor='#2E7D32')

# 构建提示词连接
dot.edge('skill_eligible', 'format_skills', penwidth='1.5')
dot.edge('format_skills', 'xml_example', style='dashed', color='#666666')
dot.edge('format_skills', 'inject_prompt', penwidth='1.5')
dot.edge('inject_prompt', 'snapshot', penwidth='1.5')

# 用户消息连接
dot.edge('snapshot', 'title2', style='invis')
dot.edge('title2', 'user_msg', style='invis')
dot.edge('user_msg', 'check_slash', penwidth='1.5')
dot.edge('check_slash', 'parse_cmd', label=' 是 ', color='#FF9800', fontcolor='#E65100')
dot.edge('check_slash', 'send_llm', label=' 否 ', color='#2196F3', fontcolor='#1565C0')

# 斜杠命令分支
dot.edge('parse_cmd', 'find_skill_cmd', penwidth='1.5')
dot.edge('find_skill_cmd', 'skill_found', penwidth='1.5')
dot.edge('skill_found', 'direct_invoke', label=' 是 ', color='#81C784', fontcolor='#2E7D32')
dot.edge('skill_found', 'send_llm', label=' 否 ', color='#E57373', fontcolor='#C62828')

# LLM 判断分支
dot.edge('send_llm', 'llm_scan', penwidth='1.5')
dot.edge('llm_scan', 'llm_match', penwidth='1.5')
dot.edge('llm_match', 'llm_select', label=' 是 ', color='#81C784', fontcolor='#2E7D32')
dot.edge('llm_match', 'llm_no_skill', label=' 否 ', color='#E57373', fontcolor='#C62828')
dot.edge('llm_select', 'llm_read', penwidth='1.5')

# Skill 执行
dot.edge('direct_invoke', 'parse_skill', penwidth='1.5')
dot.edge('llm_read', 'parse_skill', penwidth='1.5')
dot.edge('parse_skill', 'exec_workflow', penwidth='1.5')
dot.edge('exec_workflow', 'use_scripts', penwidth='1.5')
dot.edge('exec_workflow', 'read_refs', penwidth='1.5')
dot.edge('exec_workflow', 'use_assets', penwidth='1.5')
dot.edge('use_scripts', 'generate_response', penwidth='1.5')
dot.edge('read_refs', 'generate_response', penwidth='1.5')
dot.edge('use_assets', 'generate_response', penwidth='1.5')

# 结束
dot.edge('generate_response', 'end', penwidth='1.5')
dot.edge('llm_no_skill', 'end', penwidth='1.5')

# Render
output_path = '/workspace/skill_discovery_flowchart'
dot.render(output_path, cleanup=True)
print(f"Flowchart saved to: {output_path}.png")
