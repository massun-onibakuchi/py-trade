import alphalens

# Ingest and format data
factor_data = alphalens.utils.get_clean_factor_and_forward_returns(
    my_factor, pricing, quantiles=5, groupby=ticker_sector, groupby_labels=sector_names
)

# Run analysis
alphalens.tears.create_full_tear_sheet(factor_data)