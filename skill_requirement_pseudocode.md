# Skill 需求理解流程 - 伪代码

## 概述

当用户请求创建一个 Skill 时，Agent 需要通过对话收集足够的信息来理解需求。
这个过程是迭代式的，每次只问 1-2 个问题，避免让用户感到压力。

---

## 伪代码

```python
def understand_skill_requirement(user_request: str) -> SkillRequirement:
    """
    理解 Skill 需求的完整流程
    
    Args:
        user_request: 用户的原始请求，例如 "帮我创建一个图片编辑skill"
    
    Returns:
        SkillRequirement: 完整的需求文档
    """
    
    # ==================== 1. 初始化上下文 ====================
    context = RequirementContext(
        original_request=user_request,
        skill_name=extract_skill_name(user_request),  # 可能为空
        known_info={},           # 已知信息
        pending_questions=[],    # 待确认问题
        examples=[],             # 使用场景示例
        confirmed=False
    )
    
    # ==================== 2. 初始评估 ====================
    if is_requirement_already_clear(user_request):
        # 如果用户请求已经足够详细，跳过收集阶段
        return compile_requirement(context)
    
    # ==================== 3. 生成初始问题列表 ====================
    context.pending_questions = generate_initial_questions(user_request)
    
    # ==================== 4. 信息收集循环 ====================
    while not is_requirement_complete(context):
        
        # 4.1 选择最重要的问题
        question = select_most_important_question(context)
        
        # 4.2 向用户提问（每次最多 1-2 个问题）
        user_response = ask_user(question)
        
        # 4.3 解析用户回复
        extracted_info = parse_user_response(user_response, question)
        
        # 4.4 更新上下文
        context = update_context(context, extracted_info)
        
        # 4.5 检查是否需要生成假设示例
        if needs_generated_examples(context):
            hypothetical_examples = generate_hypothetical_examples(context)
            validated_examples = ask_user_to_validate(hypothetical_examples)
            context.examples.extend(validated_examples)
    
    # ==================== 5. 编译需求文档 ====================
    return compile_requirement(context)


# ==================== 核心数据结构 ====================

@dataclass
class RequirementContext:
    original_request: str           # 用户原始请求
    skill_name: Optional[str]       # Skill 名称
    known_info: Dict[str, Any]      # 已收集的信息
    pending_questions: List[Question]  # 待确认问题
    examples: List[UsageExample]    # 使用场景示例
    confirmed: bool                 # 是否已确认完成


@dataclass
class SkillRequirement:
    name: str                       # Skill 名称
    description: str                # Skill 描述
    functionality: List[str]        # 功能列表
    usage_examples: List[UsageExample]  # 使用场景示例
    trigger_patterns: List[str]     # 触发条件/用户可能说的话
    expected_output: str            # 预期输出格式
    dependencies: List[str]         # 依赖项（可选）


@dataclass
class UsageExample:
    user_input: str                 # 用户输入示例
    expected_behavior: str          # 预期行为
    output_format: Optional[str]    # 输出格式


# ==================== 核心问题类型 ====================

QUESTION_TYPES = {
    "functionality": {
        "priority": 1,
        "template": "这个 {skill_name} skill 应该支持哪些功能？{suggestions}",
        "examples": [
            "图片编辑skill应该支持：编辑、旋转、裁剪、滤镜？",
            "天气skill应该支持：当前天气、天气预报、多城市？"
        ]
    },
    "usage_examples": {
        "priority": 2,
        "template": "能给一些具体的使用场景示例吗？用户会怎样使用这个skill？",
        "examples": [
            "用户可能会说：'帮我把这张图片旋转90度'",
            "用户可能会说：'北京今天天气怎么样？'"
        ]
    },
    "trigger_patterns": {
        "priority": 3,
        "template": "用户说什么话应该触发这个skill？",
        "examples": [
            "当用户提到'编辑图片'、'处理照片'时触发",
            "当用户询问'天气'、'气温'、'下雨'时触发"
        ]
    },
    "expected_output": {
        "priority": 4,
        "template": "期望的输出是什么格式？文本、图片、文件？",
        "examples": [
            "输出处理后的图片文件",
            "输出天气信息的文本描述"
        ]
    }
}


# ==================== 辅助函数 ====================

def generate_initial_questions(user_request: str) -> List[Question]:
    """根据用户请求生成初始问题列表"""
    questions = []
    
    # 分析用户请求，确定哪些信息缺失
    if not has_functionality_info(user_request):
        questions.append(Question(
            type="functionality",
            priority=1,
            text=generate_functionality_question(user_request)
        ))
    
    if not has_examples(user_request):
        questions.append(Question(
            type="usage_examples", 
            priority=2,
            text="能给一些具体的使用场景示例吗？"
        ))
    
    if not has_trigger_patterns(user_request):
        questions.append(Question(
            type="trigger_patterns",
            priority=3,
            text="用户说什么话应该触发这个skill？"
        ))
    
    return sorted(questions, key=lambda q: q.priority)


def select_most_important_question(context: RequirementContext) -> Question:
    """选择当前最重要的待确认问题"""
    
    # 优先级排序
    # 1. 功能范围（最重要，决定skill的边界）
    # 2. 使用场景示例（帮助理解具体需求）
    # 3. 触发条件（确定何时使用skill）
    # 4. 预期输出（输出格式）
    
    if not context.pending_questions:
        return None
    
    return min(context.pending_questions, key=lambda q: q.priority)


def is_requirement_complete(context: RequirementContext) -> bool:
    """检查需求信息是否完整"""
    
    checks = [
        has_clear_functionality(context),   # 功能范围明确
        has_concrete_examples(context),     # 有具体示例
        has_trigger_conditions(context),    # 触发条件清晰
    ]
    
    return all(checks)


def has_clear_functionality(context: RequirementContext) -> bool:
    """检查功能范围是否明确"""
    return (
        "functionality" in context.known_info and
        len(context.known_info["functionality"]) > 0
    )


def has_concrete_examples(context: RequirementContext) -> bool:
    """检查是否有具体的使用场景示例"""
    return len(context.examples) >= 2  # 至少需要2个示例


def has_trigger_conditions(context: RequirementContext) -> bool:
    """检查触发条件是否清晰"""
    return (
        "triggers" in context.known_info and
        len(context.known_info["triggers"]) > 0
    )


def needs_generated_examples(context: RequirementContext) -> bool:
    """判断是否需要 Agent 生成假设示例供用户确认"""
    return (
        has_clear_functionality(context) and  # 已知功能
        not has_concrete_examples(context)    # 但缺少示例
    )


def generate_hypothetical_examples(context: RequirementContext) -> List[UsageExample]:
    """
    根据已知信息生成假设的使用场景示例
    
    示例输出:
    "我想象用户可能会这样使用这个skill:
     - '帮我把这张图片旋转90度'
     - '移除这张照片中的红眼'
     - '给这张图片加一个复古滤镜'
     这些符合你的预期吗？还有其他使用方式吗？"
    """
    functionality = context.known_info.get("functionality", [])
    skill_name = context.skill_name
    
    examples = []
    for func in functionality[:3]:  # 最多生成3个示例
        example = UsageExample(
            user_input=generate_example_input(func, skill_name),
            expected_behavior=generate_expected_behavior(func),
            output_format=None
        )
        examples.append(example)
    
    return examples


def compile_requirement(context: RequirementContext) -> SkillRequirement:
    """将收集的信息编译成需求文档"""
    
    return SkillRequirement(
        name=context.skill_name or generate_skill_name(context),
        description=generate_description(context),
        functionality=context.known_info.get("functionality", []),
        usage_examples=context.examples,
        trigger_patterns=context.known_info.get("triggers", []),
        expected_output=context.known_info.get("output_format", "text"),
        dependencies=context.known_info.get("dependencies", [])
    )


# ==================== 对话示例 ====================

"""
用户: 帮我创建一个图片编辑skill

Agent: 好的！我来帮你创建一个图片编辑skill。首先我需要了解一些信息：
       这个图片编辑skill应该支持哪些功能？
       比如：旋转、裁剪、滤镜、调整大小、移除背景？

用户: 主要是旋转和裁剪，还要能调整亮度

Agent: 明白了，功能包括：旋转、裁剪、调整亮度。
       能给一些具体的使用场景示例吗？用户通常会怎样描述他们的需求？

用户: 比如说"把这张图片顺时针旋转90度"，或者"把这张图裁剪成正方形"

Agent: 很好！我再想象几个可能的使用场景：
       - "帮我把这张图片的亮度调高一点"
       - "把这张照片旋转180度"
       - "裁剪这张图片，只保留中间部分"
       这些符合你的预期吗？

用户: 对，差不多就是这样

Agent: 好的，需求已经清晰了。总结一下：
       
       📋 Skill 需求文档:
       - 名称: image-editor
       - 功能: 旋转、裁剪、调整亮度
       - 使用示例:
         * "把这张图片顺时针旋转90度"
         * "把这张图裁剪成正方形"
         * "帮我把这张图片的亮度调高一点"
       - 触发条件: 用户提到编辑图片、处理照片、旋转、裁剪、亮度等
       
       现在我来规划需要哪些资源...
"""
```

---

## 流程要点

### 1. 核心原则

- **每次只问 1-2 个问题**：避免让用户感到压力
- **从最重要的问题开始**：功能范围 → 使用示例 → 触发条件 → 输出格式
- **主动生成假设示例**：当用户难以描述时，Agent 可以先给出假设让用户确认

### 2. 完整性检查清单

| 检查项 | 说明 | 必须 |
|-------|------|-----|
| 功能范围明确 | Skill 支持哪些操作 | ✅ |
| 有具体示例 | 至少 2 个使用场景 | ✅ |
| 触发条件清晰 | 用户说什么会触发 | ✅ |
| 预期输出格式 | 输出类型和格式 | ⚪ |

### 3. 退出条件

当以下条件都满足时，结束需求收集阶段：

```python
is_complete = (
    has_clear_functionality(context) and
    len(context.examples) >= 2 and
    has_trigger_conditions(context)
)
```
