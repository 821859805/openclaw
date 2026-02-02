#!/usr/bin/env python3
"""Generate a flowchart showing where merged skill list is returned to"""

from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Skill Merge Return Path', format='png')
dot.attr(rankdir='TB', splines='polyline', nodesep='0.6', ranksep='0.8', dpi='150')
dot.attr('node', fontname='SimHei,Arial', fontsize='11')
dot.attr('edge', fontname='SimHei,Arial', fontsize='9')

# ==================== 合并过程 ====================
with dot.subgraph(name='cluster_merge') as c:
    c.attr(label='🔀 合并过程 (loadSkillEntries)', style='rounded,filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')
    
    c.node('sources', '四个来源加载\nextra → bundled → managed → workspace', 
           shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('map_merge', 'Map&lt;string, Skill&gt;\n按 name 去重合并', 
           shape='box', style='rounded,filled', fillcolor='#90CAF9')
    c.node('to_array', 'Array.from(merged.values())\n转换为数组', 
           shape='box', style='rounded,filled', fillcolor='#64B5F6')
    c.node('parse_fm', '解析 frontmatter\n提取 metadata', 
           shape='box', style='rounded,filled', fillcolor='#42A5F5')
    c.node('skill_entries', 'SkillEntry[]\n去重后的完整列表', 
           shape='box', style='rounded,filled', fillcolor='#1E88E5', fontcolor='white')

# ==================== 返回路径 ====================
dot.node('return_title', '📤 返回到以下位置', shape='plaintext', fontsize='14', fontcolor='#C62828')

# 直接导出
with dot.subgraph(name='cluster_export') as c:
    c.attr(label='① 直接导出', style='rounded,filled', fillcolor='#E8F5E9', color='#388E3C', penwidth='2')
    c.node('export_func', 'loadWorkspaceSkillEntries()\n公开 API', 
           shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    c.node('export_callers', '''调用方:
• skills-install.ts (安装 skill)
• skills-status.ts (状态报告)
• skills-remote.ts (远程节点)
• pi-embedded-runner (Agent 运行)
• gateway/skills.ts (Gateway API)''', 
           shape='note', style='filled', fillcolor='#A5D6A7', fontsize='9')

# SkillSnapshot
with dot.subgraph(name='cluster_snapshot') as c:
    c.attr(label='② SkillSnapshot', style='rounded,filled', fillcolor='#FFF8E1', color='#FFA000', penwidth='2')
    c.node('snapshot_func', 'buildWorkspaceSkillSnapshot()', 
           shape='box', style='rounded,filled', fillcolor='#FFECB3')
    c.node('snapshot_result', '''SkillSnapshot {
  prompt: string         // XML
  skills: [{name, env}]
  resolvedSkills: Skill[] // 👈 这里
  version: number
}''', shape='note', style='filled', fillcolor='#FFE082', fontsize='9')
    c.node('snapshot_store', '缓存到 SessionEntry\n→ ~/.openclaw/sessions.json', 
           shape='box', style='rounded,filled', fillcolor='#FFD54F')

# 系统提示词
with dot.subgraph(name='cluster_prompt') as c:
    c.attr(label='③ 系统提示词', style='rounded,filled', fillcolor='#F3E5F5', color='#7B1FA2', penwidth='2')
    c.node('prompt_func', 'buildWorkspaceSkillsPrompt()', 
           shape='box', style='rounded,filled', fillcolor='#E1BEE7')
    c.node('format_xml', 'formatSkillsForPrompt()\n生成 XML', 
           shape='box', style='rounded,filled', fillcolor='#CE93D8')
    c.node('xml_result', '''&lt;available_skills&gt;
  &lt;skill&gt;
    &lt;name&gt;weather&lt;/name&gt;
    &lt;description&gt;...&lt;/description&gt;
    &lt;location&gt;path&lt;/location&gt;
  &lt;/skill&gt;
  ...
&lt;/available_skills&gt;''', shape='note', style='filled', fillcolor='#BA68C8', fontsize='9', fontcolor='white')

# 斜杠命令
with dot.subgraph(name='cluster_commands') as c:
    c.attr(label='④ 斜杠命令规格', style='rounded,filled', fillcolor='#FCE4EC', color='#C2185B', penwidth='2')
    c.node('cmd_func', 'buildWorkspaceSkillCommandSpecs()', 
           shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('cmd_result', '''SkillCommandSpec[] {
  name: "weather"      // /weather
  skillName: "weather"
  description: "..."
  dispatch?: {...}     // 可选工具调度
}''', shape='note', style='filled', fillcolor='#F48FB1', fontsize='9')
    c.node('cmd_use', '注册为斜杠命令\nTelegram / Discord / CLI', 
           shape='box', style='rounded,filled', fillcolor='#EC407A', fontcolor='white')

# 沙盒同步
with dot.subgraph(name='cluster_sync') as c:
    c.attr(label='⑤ 沙盒同步', style='rounded,filled', fillcolor='#E0F2F1', color='#00897B', penwidth='2')
    c.node('sync_func', 'syncSkillsToWorkspace()', 
           shape='box', style='rounded,filled', fillcolor='#B2DFDB')
    c.node('sync_result', '复制到沙盒工作区\n&lt;sandbox&gt;/skills/', 
           shape='box', style='rounded,filled', fillcolor='#80CBC4')

# ==================== 连接 ====================

# 合并流程
dot.edge('sources', 'map_merge', penwidth='1.5')
dot.edge('map_merge', 'to_array', penwidth='1.5')
dot.edge('to_array', 'parse_fm', penwidth='1.5')
dot.edge('parse_fm', 'skill_entries', penwidth='2')

# 返回路径
dot.edge('skill_entries', 'return_title', style='invis')

dot.edge('skill_entries', 'export_func', penwidth='2', color='#388E3C', label='  return  ')
dot.edge('export_func', 'export_callers', style='dashed', color='#388E3C')

dot.edge('skill_entries', 'snapshot_func', penwidth='2', color='#FFA000', label='  参数  ')
dot.edge('snapshot_func', 'snapshot_result', penwidth='1.5', color='#FFA000')
dot.edge('snapshot_result', 'snapshot_store', penwidth='1.5', color='#FFA000')

dot.edge('skill_entries', 'prompt_func', penwidth='2', color='#7B1FA2', label='  参数  ')
dot.edge('prompt_func', 'format_xml', penwidth='1.5', color='#7B1FA2')
dot.edge('format_xml', 'xml_result', penwidth='1.5', color='#7B1FA2')

dot.edge('skill_entries', 'cmd_func', penwidth='2', color='#C2185B', label='  参数  ')
dot.edge('cmd_func', 'cmd_result', penwidth='1.5', color='#C2185B')
dot.edge('cmd_result', 'cmd_use', penwidth='1.5', color='#C2185B')

dot.edge('skill_entries', 'sync_func', penwidth='2', color='#00897B', label='  参数  ')
dot.edge('sync_func', 'sync_result', penwidth='1.5', color='#00897B')

# Render
output_path = '/workspace/skill_return_path_flowchart'
dot.render(output_path, cleanup=True)
print(f"Flowchart saved to: {output_path}.png")
