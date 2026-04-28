import pandas as pd
import json
import re
import csv

# 1. Define file paths
INPUT_FILE = 'Tickets - Machine Summary.csv'
OUTPUT_FILE = 'Tickets - Assessment Stats.csv'

def extract_json(text):
    """Extracts and parses the JSON block between [JSON_START] and [JSON_END]."""
    if pd.isna(text):
        return None
    
    # Regex to find everything between the custom tags
    match = re.search(r'\[JSON_START\](.*?)\[JSON_END\]', str(text), re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            return None
    return None

def main():
    try:
        # Load the CSV. Ignore commas by using tab as a separator, and declare no headers.
        df = pd.read_csv(INPUT_FILE, sep='\t', header=None)
        first_col_name = df.columns[0]
        
        # 2. Extract JSON metrics into a new column
        df['parsed_metrics'] = df[first_col_name].apply(extract_json)
        
        # Drop rows where JSON extraction failed
        valid_df = df.dropna(subset=['parsed_metrics']).copy()
        
        if valid_df.empty:
            print("No valid JSON blocks found in the CSV.")
            return

        # 3. Calculate Overall Status Metrics
        # Extract status into a separate column for easy counting
        valid_df['status'] = valid_df['parsed_metrics'].apply(lambda x: x.get('overall_status', 'Unknown').capitalize())
        
        status_counts = valid_df['status'].value_counts().to_dict()
        complete_count = status_counts.get('Complete', 0)
        partial_count = status_counts.get('Partial', 0)
        incomplete_count = status_counts.get('Incomplete', 0)

        # 4. Calculate Criteria Metrics
        # Sum up how many times each criteria was 'true'
        object_count = sum(1 for x in valid_df['parsed_metrics'] if x.get('criteria', {}).get('object_met') is True)
        nav_count = sum(1 for x in valid_df['parsed_metrics'] if x.get('criteria', {}).get('navigation_met') is True)
        issue_count = sum(1 for x in valid_df['parsed_metrics'] if x.get('criteria', {}).get('issue_met') is True)
        evidence_count = sum(1 for x in valid_df['parsed_metrics'] if x.get('criteria', {}).get('evidence_met') is True)

        # 5. Compile all stats into a dictionary
        final_stats = {
            "Total_Valid_Tickets_Processed": len(valid_df),
            "Status_Complete": complete_count,
            "Status_Partial": partial_count,
            "Status_Incomplete": incomplete_count,
            "Criteria_Object_Met": object_count,
            "Criteria_Navigation_Met": nav_count,
            "Criteria_Issue_Met": issue_count,
            "Criteria_Evidence_Met": evidence_count
        }

        # 6. Output to Console
        print("\n=== OVERALL ASSESSMENT STATS ===")
        print(f"Total Processed: {len(valid_df)}")
        print(f"Complete:   {complete_count}")
        print(f"Partial:    {partial_count}")
        print(f"Incomplete: {incomplete_count}")
        print("================================\n")

        # 7. Write to Output CSV
        with open(OUTPUT_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            for key, value in final_stats.items():
                writer.writerow([key, value])
                
        print(f"Detailed metrics successfully saved to '{OUTPUT_FILE}'.")

    except FileNotFoundError:
        print(f"Error: Could not find the file '{INPUT_FILE}'. Please ensure it is in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
