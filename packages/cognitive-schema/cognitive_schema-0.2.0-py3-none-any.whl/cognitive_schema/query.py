import os
import glob
from openai import OpenAI
import click

def load_profiles(profiles_path):
    """Load all profiles from the specified directory."""
    profile_files = glob.glob(os.path.join(profiles_path, "*.md"))
    if not profile_files:
        return None
    profiles_content = ""
    for file in profile_files:
        with open(file, 'r') as f:
            profiles_content += f.read() + "\n\n"
    return profiles_content

def construct_prompt(profiles_content, query):
    """Construct the prompt for the OpenAI API."""
    return f"""
    You are an expert in data analysis. Based on the following database profiles, answer the query:
    {profiles_content}
    Query: {query}
    """

def query_openai(prompt):
    """Query the OpenAI API with the given prompt."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in data analysis."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192
        )
        return response.choices[0].message.content
    except Exception as e:
        click.echo(f"An error occurred while querying: {e}")
        return None