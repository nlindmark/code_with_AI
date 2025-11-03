"""
Nivå 3: Beräkna genomsnitt per kategori från CSV-fil.
CSV-filen har format: kategori, värde
Returnera en dictionary med genomsnitt per kategori.
"""
import csv


def avg_per_category(csv_path: str) -> dict:
    """
    Läser en CSV-fil med format "kategori, värde" och beräknar genomsnittet per kategori.
    
    Args:
        csv_path: Sökväg till CSV-filen
        
    Returns:
        Dictionary med kategorier som nycklar och genomsnittsvärden som värden
    """
    category_sums = {}
    category_counts = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            
            category = row[0].strip()
            value = float(row[1].strip())
            
            if category not in category_sums:
                category_sums[category] = 0
                category_counts[category] = 0
            
            category_sums[category] += value
            category_counts[category] += 1
    
    # Beräkna genomsnitt per kategori
    averages = {}
    for category in category_sums:
        averages[category] = category_sums[category] / category_counts[category]
    
    return averages












