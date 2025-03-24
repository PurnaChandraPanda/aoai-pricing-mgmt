import pandas as pd

# Read the data into a DataFrame
df = pd.read_csv('aoai_requests.csv')

# Convert datetime column to date only
df['datetime'] = pd.to_datetime(df['datetime']).dt.date

# ## test only
# # Filter the DataFrame to only include data from 3/21/2025
# df = df[df['datetime'] == pd.to_datetime('2025-03-21').date()]
# print(df.shape)

# Define token prices for input and output tokens for each model (example prices)
token_prices = {
    'gpt-4o': {'input': 2.5 / 1_000_000, 'output': 10 / 1_000_000},
    'gpt-4o-mini': {'input': 0.15 / 1_000_000, 'output': 0.6 / 1_000_000},
    'text-embedding': {'input': 0.0001/1000}
}

# Function to get the correct token price based on model and token type
def get_token_price(model, token_type):
    for key in sorted(token_prices.keys(), key=len, reverse=True):
        # if key in model:
        if model.startswith(key):
            return token_prices[key].get(token_type, 0)
    return 0

# Create model_inp and model_op columns for each model name with different pricing
df['model_inp'] = df.apply(lambda row: row['prompt_tokens'] * get_token_price(row['model'], 'input') if pd.notnull(row['prompt_tokens']) else 0, axis=1)
df['model_op'] = df.apply(lambda row: row['completion_tokens'] * get_token_price(row['model'], 'output') if pd.notnull(row['completion_tokens']) else 0, axis=1)

# Create a new DataFrame for input tokens
inp_df = pd.DataFrame()
inp_df['date'] = df['datetime']
inp_df['meterName'] = df.apply(lambda row: f"{row['model'].replace('gpt-', 'gpt ').replace('-', ' ')} Inp glbl Tokens", axis=1)
inp_df['costInUsd'] = df['model_inp']

# Create a new DataFrame for output tokens
outp_df = pd.DataFrame()
outp_df['date'] = df['datetime']
outp_df['meterName'] = df.apply(lambda row: f"{row['model'].replace('gpt-', 'gpt ').replace('-', ' ')} Outp glbl Tokens" if not row['model'].startswith('text-embedding') else None, axis=1)
outp_df['costInUsd'] = df.apply(lambda row: row['model_op'] if not row['model'].startswith('text-embedding') else None, axis=1)

# Concatenate the input and output DataFrames
combined_df = pd.concat([inp_df.dropna(), outp_df.dropna()])

# Group by date and meterName and sum the costInUsd
grouped_df = combined_df.groupby(['date', 'meterName'])['costInUsd'].sum().reset_index()

# Print the grouped DataFrame
print(grouped_df.to_string(index=False))



