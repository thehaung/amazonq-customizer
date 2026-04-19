from amazonq_customizer.templates import inject_header

def test_inject_header():
    skill_name = "brainstorming"
    original_content = "# Brainstorming\nContent here."
    result = inject_header(skill_name, original_content)
    
    assert "# INSTRUCTIONS FOR AMAZON Q" in result
    assert "ACTIVATED PROMPT: brainstorming" in result
    assert original_content in result