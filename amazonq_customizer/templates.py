AMAZON_Q_HEADER_TEMPLATE = """# INSTRUCTIONS FOR AMAZON Q
When the user invokes this prompt, you MUST immediately print the following before taking any action or answering any questions:
"ACTIVATED PROMPT: {skill_name}" 
"Executing the following steps:" 
(Briefly list the core steps or rules you are about to follow based on the instructions below.)

---
{original_content}"""

def inject_header(skill_name: str, original_content: str) -> str:
    return AMAZON_Q_HEADER_TEMPLATE.format(
        skill_name=skill_name,
        original_content=original_content
    )