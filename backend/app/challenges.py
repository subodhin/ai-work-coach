CHALLENGES = [
    {
        "id": "se-problem-001",
        "title": "Define a Production API Problem",
        "role": "software_engineer",
        "difficulty": "intermediate",
        "target_skill": "problem_framing",
        "scenario": (
            "Your team owns a production API that has recently started "
            "experiencing performance problems. Different engineers have "
            "different opinions about the cause."
        ),
        "task": (
            "Use AI to help you define the problem clearly and determine "
            "what information you need before investigating the issue."
        ),
        "rubric": [
            "Clearly defines the problem",
            "States the desired outcome",
            "Identifies important constraints",
            "Separates known facts from assumptions",
            "Identifies missing information",
        ],
    },
    {
        "id": "se-context-001",
        "title": "Investigate a Slow API",
        "role": "software_engineer",
        "difficulty": "intermediate",
        "target_skill": "context",
        "scenario": (
            "A production API has intermittent latency problems. "
            "The issue appears mainly during periods of high traffic."
        ),
        "task": (
            "Use AI to investigate possible causes and develop a "
            "structured troubleshooting approach."
        ),
        "rubric": [
            "Provides relevant technical context",
            "Includes useful system information",
            "Identifies important missing context",
            "Distinguishes relevant from irrelevant information",
            "Uses context to narrow the investigation",
        ],
    },
    {
        "id": "se-verification-001",
        "title": "Diagnose a Production Bug",
        "role": "software_engineer",
        "difficulty": "intermediate",
        "target_skill": "verification",
        "scenario": (
            "An AI assistant has suggested several possible causes for "
            "an intermittent production bug."
        ),
        "task": (
            "Use AI to investigate the issue, challenge its suggestions, "
            "and determine how you would verify the likely root cause."
        ),
        "rubric": [
            "Challenges unsupported AI assumptions",
            "Requests or identifies supporting evidence",
            "Considers multiple hypotheses",
            "Defines concrete verification steps",
            "Avoids treating AI output as automatically correct",
        ],
    },
    {
        "id": "marketing-prompting-001",
        "title": "Improve a Marketing Brief",
        "role": "marketing",
        "difficulty": "beginner",
        "target_skill": "prompting",
        "scenario": (
            "Your marketing team needs to create a campaign brief "
            "for a new product launch."
        ),
        "task": (
            "Use AI to help create a useful marketing brief. "
            "Write prompts that guide the AI toward a specific, "
            "usable result."
        ),
        "rubric": [
            "Provides clear instructions",
            "Defines the desired output",
            "Provides relevant context",
            "Uses appropriate constraints",
            "Iterates on the prompt when necessary",
        ],
    },
    {
        "id": "marketing-reasoning-001",
        "title": "Analyze Customer Feedback",
        "role": "marketing",
        "difficulty": "intermediate",
        "target_skill": "reasoning",
        "scenario": (
            "Your company has collected a large amount of customer "
            "feedback. The feedback contains complaints, feature "
            "requests, and positive comments."
        ),
        "task": (
            "Use AI to analyze the feedback and identify the most "
            "important customer problems and potential marketing actions."
        ),
        "rubric": [
            "Breaks the problem into meaningful categories",
            "Identifies patterns in the information",
            "Considers alternative interpretations",
            "Connects findings to business implications",
            "Uses structured reasoning rather than accepting the first answer",
        ],
    },
    {
        "id": "product-output-001",
        "title": "Create an Executive Summary",
        "role": "product_manager",
        "difficulty": "beginner",
        "target_skill": "final_output",
        "scenario": (
            "You have used AI to analyze a product initiative and "
            "now need to communicate the findings to senior leadership."
        ),
        "task": (
            "Use AI to produce a concise executive summary that "
            "leadership can use to understand the situation and "
            "decide what to do next."
        ),
        "rubric": [
            "Clearly communicates the key findings",
            "Separates important information from unnecessary detail",
            "Provides actionable recommendations",
            "Uses appropriate language for the audience",
            "Produces a clear and decision-useful final output",
        ],
    },
]


def get_all_challenges() -> list[dict]:
    return CHALLENGES


def get_challenge_by_id(challenge_id: str) -> dict | None:
    for challenge in CHALLENGES:
        if challenge["id"] == challenge_id:
            return challenge

    return None