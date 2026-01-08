#!/usr/bin/env python3
"""
Analyze gender distribution of authors in Archimedes mental rotation papers.
Requires: pip install gender-guesser
"""

import json
import os
from collections import Counter

try:
    import gender_guesser.detector as gender
    detector = gender.Detector()
except ImportError:
    print("Installing gender-guesser...")
    os.system("pip install gender-guesser")
    import gender_guesser.detector as gender
    detector = gender.Detector()

def get_first_name(full_name):
    """Extract first name from full name."""
    if not full_name:
        return None
    parts = full_name.strip().split()
    if not parts:
        return None
    return parts[0]

def analyze_papers(json_path):
    """Analyze gender distribution in a dataset."""
    with open(json_path, 'r') as f:
        papers = json.load(f)
    
    all_authors = []
    for paper in papers:
        authors = paper.get('authors', [])
        all_authors.extend(authors)
    
    gender_counts = Counter()
    first_author_genders = Counter()
    
    for i, author in enumerate(all_authors):
        first_name = get_first_name(author)
        if not first_name:
            continue
        
        detected_gender = detector.get_gender(first_name)
        
        # Simplify categories
        if detected_gender in ['male', 'mostly_male']:
            gender = 'male'
        elif detected_gender in ['female', 'mostly_female']:
            gender = 'female'
        else:
            gender = 'unknown'
        
        gender_counts[gender] += 1
    
    # Analyze first authors
    for paper in papers:
        authors = paper.get('authors', [])
        if not authors:
            continue
        
        first_author = authors[0]
        first_name = get_first_name(first_author)
        if not first_name:
            continue
        
        detected_gender = detector.get_gender(first_name)
        if detected_gender in ['male', 'mostly_male']:
            gender = 'male'
        elif detected_gender in ['female', 'mostly_female']:
            gender = 'female'
        else:
            gender = 'unknown'
        
        first_author_genders[gender] += 1
    
    return {
        'total_authors': len(all_authors),
        'all_authors': gender_counts,
        'first_authors': first_author_genders,
        'papers': len(papers)
    }

def main():
    archimedes_dir = os.path.expanduser('~/Archimedes')
    
    datasets = {
        'Shepard & Metzler Citations': 'shepard_metzler_1971_citations_clean.json',
        'Vandenberg & Kuse Citations': 'vandenberg_kuse_1978_citations_clean.json',
        'Overlap Citations': 'overlap_citations_clean.json'
    }
    
    results = {}
    
    for name, filename in datasets.items():
        filepath = os.path.join(archimedes_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found")
            continue
        
        print(f"\nAnalyzing {name}...")
        results[name] = analyze_papers(filepath)
    
    # Print summary
    print("\n" + "="*70)
    print("GENDER ANALYSIS: MENTAL ROTATION CITATION NETWORK")
    print("="*70)
    
    for dataset_name, data in results.items():
        print(f"\n{dataset_name}:")
        print(f"  Papers: {data['papers']}")
        print(f"  Total authors: {data['total_authors']}")
        print(f"\n  All Authors:")
        for gender, count in data['all_authors'].items():
            pct = (count / data['total_authors']) * 100
            print(f"    {gender.capitalize()}: {count} ({pct:.1f}%)")
        
        print(f"\n  First Authors:")
        total_first = sum(data['first_authors'].values())
        for gender, count in data['first_authors'].items():
            pct = (count / total_first) * 100 if total_first > 0 else 0
            print(f"    {gender.capitalize()}: {count} ({pct:.1f}%)")
    
    # Combined stats
    print("\n" + "="*70)
    print("COMBINED STATISTICS")
    print("="*70)
    
    total_authors = sum(d['total_authors'] for d in results.values())
    combined_gender = Counter()
    for data in results.values():
        combined_gender.update(data['all_authors'])
    
    print(f"\nTotal authors across all datasets: {total_authors}")
    for gender, count in combined_gender.items():
        pct = (count / total_authors) * 100
        print(f"  {gender.capitalize()}: {count} ({pct:.1f}%)")
    
    # Save to JSON
    output_path = os.path.join(archimedes_dir, 'gender_analysis.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()
