from dataclasses import dataclass
from typing import Dict, List

@dataclass
class JobDescription:
    """Data model for job description"""
    raw_text: str
    tech_stacks: Dict[str, List[str]]  # {stack_name: [bullet1, bullet2,...]}
    
    def validate_bullet_points(self):
        """Ensure exactly 6 bullet points per stack"""
        for stack, bullets in self.tech_stacks.items():
            if len(bullets) != 6:
                raise ValueError(f"Tech stack '{stack}' must have exactly 6 bullet points")

@dataclass
class Resume:
    """Data model for resume processing"""
    file_path: str
    anchor_method: str  # 'placeholders' or 'heuristics'
    project_anchors: Dict[int, str]  # {project_num: anchor_text}

@dataclass
class EmailConfig:
    """Data model for email settings"""
    recipients: List[str]
    subject: str
    body: str