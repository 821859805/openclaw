#!/usr/bin/env python3
"""Generate a flowchart for Skill merge process with priority"""

from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Skill Merge Process', format='png')
dot.attr(rankdir='TB', splines='polyline', nodesep='0.6', ranksep='0.7', dpi='150')
dot.attr('node', fontname='SimHei,Arial', fontsize='11')
dot.attr('edge', fontname='SimHei,Arial', fontsize='9')

# ==================== 标题 ====================
dot.node('title', '🔀 Skill 按优先级合并流程', shape='plaintext', fontsize='16', fontcolor='#1565C0')

# ==================== 四个来源 ====================
with dot.subgraph(name='cluster_sources') as c:
    c.attr(label='📂 四个 Skill 来源（按优先级从低到高）', style='rounded,filled', fillcolor='#ECEFF1', color='#546E7A', penwidth='2')
    
    # 优先级 1：Extra（最低）
    c.node('src_extra', '① Extra Skills\n(extraDirs + plugins)\n优先级: 最低', 
           shape='box', style='rounded,filled', fillcolor='#FFCDD2', color='#C62828', penwidth='2')
    c.node('path_extra', '路径:\n- config.skills.load.extraDirs\n- 插件目录/skills/', 
           shape='note', style='filled', fillcolor='#FFEBEE', fontsize='9')
    
    # 优先级 2：Bundled
    c.node('src_bundled', '② Bundled Skills\n(内置)\n优先级: 低', 
           shape='box', style='rounded,filled', fillcolor='#FFE0B2', color='#E65100', penwidth='2')
    c.node('path_bundled', '路径:\n- npm包/skills/\n- OpenClaw.app/skills/', 
           shape='note', style='filled', fillcolor='#FFF3E0', fontsize='9')
    
    # 优先级 3：Managed
    c.node('src_managed', '③ Managed Skills\n(本地托管)\n优先级: 高', 
           shape='box', style='rounded,filled', fillcolor='#C8E6C9', color='#2E7D32', penwidth='2')
    c.node('path_managed', '路径:\n~/.openclaw/skills/', 
           shape='note', style='filled', fillcolor='#E8F5E9', fontsize='9')
    
    # 优先级 4：Workspace（最高）
    c.node('src_workspace', '④ Workspace Skills\n(工作区)\n优先级: 最高', 
           shape='box', style='rounded,filled', fillcolor='#BBDEFB', color='#1565C0', penwidth='2')
    c.node('path_workspace', '路径:\n&lt;workspace&gt;/skills/', 
           shape='note', style='filled', fillcolor='#E3F2FD', fontsize='9')

# ==================== 加载过程 ====================
with dot.subgraph(name='cluster_load') as c:
    c.attr(label='📥 加载过程', style='rounded,filled', fillcolor='#FFF8E1', color='#FFA000', penwidth='2')
    
    c.node('load_extra', 'loadSkillsFromDir()\nsource: "openclaw-extra"', 
           shape='box', style='rounded,filled', fillcolor='#FFECB3')
    c.node('load_bundled', 'loadSkillsFromDir()\nsource: "openclaw-bundled"', 
           shape='box', style='rounded,filled', fillcolor='#FFECB3')
    c.node('load_managed', 'loadSkillsFromDir()\nsource: "openclaw-managed"', 
           shape='box', style='rounded,filled', fillcolor='#FFECB3')
    c.node('load_workspace', 'loadSkillsFromDir()\nsource: "openclaw-workspace"', 
           shape='box', style='rounded,filled', fillcolor='#FFECB3')

# ==================== 合并数据结构 ====================
with dot.subgraph(name='cluster_merge') as c:
    c.attr(label='🗂️ 合并数据结构: Map&lt;string, Skill&gt;', style='rounded,filled', fillcolor='#E8F5E9', color='#388E3C', penwidth='2')
    
    c.node('map_init', 'const merged = new Map()', 
           shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    
    c.node('merge1', '① merged.set(skill.name, skill)\n遍历 extraSkills', 
           shape='box', style='rounded,filled', fillcolor='#FFCDD2')
    c.node('merge2', '② merged.set(skill.name, skill)\n遍历 bundledSkills\n(覆盖同名extra)', 
           shape='box', style='rounded,filled', fillcolor='#FFE0B2')
    c.node('merge3', '③ merged.set(skill.name, skill)\n遍历 managedSkills\n(覆盖同名bundled)', 
           shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    c.node('merge4', '④ merged.set(skill.name, skill)\n遍历 workspaceSkills\n(覆盖同名managed)', 
           shape='box', style='rounded,filled', fillcolor='#BBDEFB')

# ==================== 合并示例 ====================
with dot.subgraph(name='cluster_example') as c:
    c.attr(label='💡 合并示例: "weather" skill', style='rounded,filled', fillcolor='#F3E5F5', color='#7B1FA2', penwidth='2')
    
    c.node('ex_init', 'Map = {}', shape='box', style='rounded,filled', fillcolor='#E1BEE7')
    c.node('ex_extra', 'Map = {\n  "weather": /extra/weather\n}', 
           shape='box', style='rounded,filled', fillcolor='#FFCDD2', fontsize='10')
    c.node('ex_bundled', 'Map = {\n  "weather": /bundled/weather\n}', 
           shape='box', style='rounded,filled', fillcolor='#FFE0B2', fontsize='10')
    c.node('ex_managed', 'Map = {\n  "weather": ~/.openclaw/skills/weather\n}', 
           shape='box', style='rounded,filled', fillcolor='#C8E6C9', fontsize='10')
    c.node('ex_final', 'Map = {\n  "weather": &lt;workspace&gt;/skills/weather\n}\n✅ 最终使用工作区版本', 
           shape='box', style='rounded,filled', fillcolor='#BBDEFB', fontsize='10')

# ==================== 转换为 SkillEntry ====================
with dot.subgraph(name='cluster_convert') as c:
    c.attr(label='📋 转换为 SkillEntry[]', style='rounded,filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')
    
    c.node('convert', 'Array.from(merged.values()).map()', 
           shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('parse_fm', '解析每个 SKILL.md\nparseFrontmatter()', 
           shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('resolve_meta', '提取 OpenClaw 元数据\nresolveOpenClawMetadata()', 
           shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('skill_entry', 'SkillEntry {\n  skill: Skill\n  frontmatter: {...}\n  metadata: {...}\n  invocation: {...}\n}', 
           shape='note', style='filled', fillcolor='#90CAF9', fontsize='10')

# ==================== 输出 ====================
dot.node('output', '📤 返回 SkillEntry[]\n(去重后的完整列表)', 
         shape='ellipse', style='filled', fillcolor='#C8E6C9', color='#388E3C', penwidth='2')

# ==================== 连接 ====================

# 标题连接
dot.edge('title', 'src_extra', style='invis')

# 来源到路径
dot.edge('src_extra', 'path_extra', style='dashed', color='#9E9E9E')
dot.edge('src_bundled', 'path_bundled', style='dashed', color='#9E9E9E')
dot.edge('src_managed', 'path_managed', style='dashed', color='#9E9E9E')
dot.edge('src_workspace', 'path_workspace', style='dashed', color='#9E9E9E')

# 来源到加载
dot.edge('src_extra', 'load_extra', penwidth='1.5', color='#C62828')
dot.edge('src_bundled', 'load_bundled', penwidth='1.5', color='#E65100')
dot.edge('src_managed', 'load_managed', penwidth='1.5', color='#2E7D32')
dot.edge('src_workspace', 'load_workspace', penwidth='1.5', color='#1565C0')

# 加载到合并
dot.edge('load_extra', 'map_init', penwidth='1.5')
dot.edge('load_bundled', 'map_init', penwidth='1.5')
dot.edge('load_managed', 'map_init', penwidth='1.5')
dot.edge('load_workspace', 'map_init', penwidth='1.5')

# 合并顺序
dot.edge('map_init', 'merge1', penwidth='2', color='#C62828')
dot.edge('merge1', 'merge2', penwidth='2', color='#E65100', label=' 覆盖 ')
dot.edge('merge2', 'merge3', penwidth='2', color='#2E7D32', label=' 覆盖 ')
dot.edge('merge3', 'merge4', penwidth='2', color='#1565C0', label=' 覆盖 ')

# 示例流程
dot.edge('ex_init', 'ex_extra', penwidth='1.5', color='#C62828')
dot.edge('ex_extra', 'ex_bundled', penwidth='1.5', color='#E65100', label=' 覆盖 ')
dot.edge('ex_bundled', 'ex_managed', penwidth='1.5', color='#2E7D32', label=' 覆盖 ')
dot.edge('ex_managed', 'ex_final', penwidth='1.5', color='#1565C0', label=' 覆盖 ')

# 合并到转换
dot.edge('merge4', 'convert', penwidth='1.5')
dot.edge('convert', 'parse_fm', penwidth='1.5')
dot.edge('parse_fm', 'resolve_meta', penwidth='1.5')
dot.edge('resolve_meta', 'skill_entry', penwidth='1.5')
dot.edge('skill_entry', 'output', penwidth='1.5')

# Render
output_path = '/workspace/skill_merge_flowchart'
dot.render(output_path, cleanup=True)
print(f"Flowchart saved to: {output_path}.png")
