"""
Nivå 5: JSON-databearbetning och mallersättning.
Läs JSON-data, beräkna genomsnittlig poäng och hitta bästa prestation.
Ersätt platshållare i markdown-mallen.
"""
import json


def build_report(api_json_path: str, template_path: str) -> str:
    """
    Läser JSON-data med poäng och en markdown-mall med platshållare.
    Beräknar genomsnittlig poäng och hittar bästa prestationen.
    Ersätter platshållarna {{avg}}, {{top.name}}, {{top.score}} i mallen.
    
    Args:
        api_json_path: Sökväg till JSON-filen med items
        template_path: Sökväg till markdown-mallen
        
    Returns:
        Den renderade markdown-strängen med ersatta värden
    """
    # Läs JSON-data
    with open(api_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get("items", [])
    
    # Beräkna genomsnittlig poäng
    if not items:
        avg = 0
        top = {"name": "N/A", "score": 0}
    else:
        total_score = sum(item["score"] for item in items)
        avg = total_score / len(items)
        
        # Hitta bästa prestationen (högst poäng)
        top = max(items, key=lambda x: x["score"])
    
    # Läs mallen
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Ersätt platshållare
    rendered = template
    rendered = rendered.replace("{{avg}}", str(avg))
    rendered = rendered.replace("{{top.name}}", top["name"])
    rendered = rendered.replace("{{top.score}}", str(top["score"]))
    
    return rendered












