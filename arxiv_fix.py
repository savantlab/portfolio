# Corrected XML parsing for ArXiv API
# Replace the parse_xml_to_dataframe function with this:

def parse_xml_to_dataframe(xml_data, search_word):
    """Parse ArXiv API XML data correctly using namespaces."""
    import xml.etree.ElementTree as ET
    import pandas as pd
    
    # ArXiv uses Atom namespace
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    root = ET.fromstring(xml_data)
    
    dates = []
    titles = []
    abstracts = []
    
    # Parse each entry
    for entry in root.findall('atom:entry', ns):
        # Get published date
        pub = entry.find('atom:published', ns)
        dates.append(pub.text if pub is not None else None)
        
        # Get title
        title = entry.find('atom:title', ns)
        title_text = title.text if title is not None else ''
        if title_text:
            # Clean up whitespace and newlines
            title_text = ' '.join(title_text.split())
        titles.append(title_text.lower())
        
        # Get abstract/summary
        abstract = entry.find('atom:summary', ns)
        abstract_text = abstract.text if abstract is not None else ''
        if abstract_text:
            abstract_text = ' '.join(abstract_text.split())
        abstracts.append(abstract_text.lower())
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'title': titles,
        'abstract': abstracts
    })
    
    # Filter out empty titles
    print(f"Total entries before filtering: {len(df)}")
    print(f"Empty titles: {df['title'].str.strip().eq('').sum()}")
    
    df = df[df['title'].str.strip() != ''].reset_index(drop=True)
    
    print(f"Total entries after filtering: {len(df)}")
    if len(df) > 0:
        print(f"Sample title: {df['title'].iloc[0][:100]}")
    
    # Add search string column
    df['contains_search_string'] = df['title'].str.contains(search_word, na=False)
    
    # Sort by date
    df = df.sort_values(by='date').reset_index(drop=True)
    
    return df
