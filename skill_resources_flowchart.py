#!/usr/bin/env python3
"""
Skill Resources (references, assets, scripts) Usage Flowchart
技能资源（references、assets、scripts）使用原理流程图
"""

from graphviz import Digraph

def create_skill_resources_flowchart():
    dot = Digraph(comment='Skill Resources Usage Flowchart')
    dot.attr(rankdir='TB', splines='polyline', nodesep='0.5', ranksep='0.8')
    dot.attr('node', shape='box', style='rounded,filled', fontname='SimHei,Arial', fontsize='11')
    dot.attr('edge', fontname='SimHei,Arial', fontsize='10')

    # ========== 第一部分：Skill 目录结构 ==========
    with dot.subgraph(name='cluster_structure') as s:
        s.attr(label='Skill 目录结构', style='dashed', color='gray')
        s.node('skill_dir', 'skill-name/\n(技能目录)', fillcolor='#E8F4FD')
        s.node('skill_md', 'SKILL.md\n(必需)', fillcolor='#90EE90')
        s.node('scripts_dir', 'scripts/\n(可执行脚本)', fillcolor='#FFD700')
        s.node('refs_dir', 'references/\n(参考文档)', fillcolor='#87CEEB')
        s.node('assets_dir', 'assets/\n(输出资源)', fillcolor='#DDA0DD')
        
        s.edge('skill_dir', 'skill_md')
        s.edge('skill_dir', 'scripts_dir')
        s.edge('skill_dir', 'refs_dir')
        s.edge('skill_dir', 'assets_dir')

    # ========== 第二部分：系统加载阶段 ==========
    with dot.subgraph(name='cluster_system') as s:
        s.attr(label='系统加载阶段 (Gateway启动时)', style='dashed', color='blue')
        s.node('load_skills', 'loadSkillsFromDir()\n扫描 skills/ 目录', fillcolor='#E8F4FD')
        s.node('parse_skill', '解析每个 SKILL.md\n提取 name + description', fillcolor='#E8F4FD')
        s.node('build_xml', 'formatSkillsForPrompt()\n生成 XML 格式', fillcolor='#E8F4FD')
        s.node('xml_output', '&lt;available_skills&gt;\n  &lt;skill&gt;\n    &lt;name&gt;...&lt;/name&gt;\n    &lt;description&gt;...&lt;/description&gt;\n    &lt;location&gt;/path/SKILL.md&lt;/location&gt;\n  &lt;/skill&gt;\n&lt;/available_skills&gt;', 
               shape='note', fillcolor='#FFFACD')
        
        s.edge('load_skills', 'parse_skill')
        s.edge('parse_skill', 'build_xml')
        s.edge('build_xml', 'xml_output')

    # ========== 第三部分：系统提示词注入 ==========
    with dot.subgraph(name='cluster_prompt') as s:
        s.attr(label='系统提示词注入', style='dashed', color='green')
        s.node('system_prompt', 'buildSkillsSection()\n构建技能章节', fillcolor='#90EE90')
        s.node('inject_xml', '注入到 System Prompt\n(LLM 系统提示词)', fillcolor='#90EE90')
        s.node('instruction', '指令: "read its SKILL.md\nat &lt;location&gt; with Read"', 
               shape='note', fillcolor='#98FB98')
        
        s.edge('system_prompt', 'inject_xml')
        s.edge('inject_xml', 'instruction')

    # ========== 第四部分：LLM 运行时决策 ==========
    with dot.subgraph(name='cluster_llm') as s:
        s.attr(label='LLM 运行时决策', style='dashed', color='orange')
        s.node('user_msg', '用户消息\n"帮我处理这个PDF"', fillcolor='#FFE4B5')
        s.node('scan_skills', 'LLM 扫描\n&lt;available_skills&gt;', fillcolor='#FFE4B5')
        s.node('match_skill', '匹配技能\ndescription 符合需求?', shape='diamond', fillcolor='#FFDAB9')
        s.node('read_skill_md', 'Read 工具\n读取 SKILL.md', fillcolor='#FFD700')
        s.node('understand', 'LLM 理解\nSKILL.md 指引', fillcolor='#FFE4B5')
        
        s.edge('user_msg', 'scan_skills')
        s.edge('scan_skills', 'match_skill')
        s.edge('match_skill', 'read_skill_md', label='匹配成功')

    # ========== 第五部分：资源使用分支 ==========
    with dot.subgraph(name='cluster_resources') as s:
        s.attr(label='根据 SKILL.md 指引使用资源', style='dashed', color='purple')
        
        # References 分支
        s.node('need_refs', '需要参考文档?', shape='diamond', fillcolor='#87CEEB')
        s.node('read_refs', 'Read 工具\n读取 references/*.md', fillcolor='#87CEEB')
        s.node('refs_context', '文档内容\n加载到上下文', fillcolor='#ADD8E6')
        
        # Scripts 分支
        s.node('need_scripts', '需要执行脚本?', shape='diamond', fillcolor='#FFD700')
        s.node('run_scripts', 'Shell 工具\npython scripts/xxx.py', fillcolor='#FFD700')
        s.node('scripts_output', '脚本执行结果\n返回给 LLM', fillcolor='#FFEC8B')
        
        # Assets 分支
        s.node('need_assets', '需要输出资源?', shape='diamond', fillcolor='#DDA0DD')
        s.node('copy_assets', 'Shell 工具\ncp assets/xxx 目标位置', fillcolor='#DDA0DD')
        s.node('assets_output', '资源文件\n复制到输出目录', fillcolor='#E6E6FA')
        
        # References 流程
        s.edge('need_refs', 'read_refs', label='是')
        s.edge('read_refs', 'refs_context')
        
        # Scripts 流程
        s.edge('need_scripts', 'run_scripts', label='是')
        s.edge('run_scripts', 'scripts_output')
        
        # Assets 流程
        s.edge('need_assets', 'copy_assets', label='是')
        s.edge('copy_assets', 'assets_output')

    # ========== 第六部分：最终响应 ==========
    with dot.subgraph(name='cluster_response') as s:
        s.attr(label='生成最终响应', style='dashed', color='red')
        s.node('combine', '综合所有信息\n生成回复', fillcolor='#FFB6C1')
        s.node('response', '返回用户\n完成任务', fillcolor='#FF69B4')
        
        s.edge('combine', 'response')

    # ========== 连接各阶段 ==========
    dot.edge('xml_output', 'system_prompt', style='dashed')
    dot.edge('instruction', 'scan_skills', style='dashed', label='LLM 遵循指令')
    dot.edge('read_skill_md', 'understand')
    dot.edge('understand', 'need_refs')
    dot.edge('understand', 'need_scripts')
    dot.edge('understand', 'need_assets')
    
    # 资源使用后汇总
    dot.edge('refs_context', 'combine', style='dashed')
    dot.edge('scripts_output', 'combine', style='dashed')
    dot.edge('assets_output', 'combine', style='dashed')
    dot.edge('need_refs', 'need_scripts', label='否', constraint='false')
    dot.edge('need_scripts', 'need_assets', label='否', constraint='false')
    dot.edge('need_assets', 'combine', label='否')

    # 渲染
    dot.render('skill_resources_flowchart', format='png', cleanup=True)
    print("流程图已生成: skill_resources_flowchart.png")

if __name__ == '__main__':
    create_skill_resources_flowchart()
