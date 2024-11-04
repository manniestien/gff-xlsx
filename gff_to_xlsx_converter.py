import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def gff_to_xlsx(gff_file, output_xlsx):
    try:
        if not os.path.isfile(gff_file):
            logging.error(f"The file '{gff_file}' does not exist.")
            return

        logging.info("Reading GFF file...")
        gff_df = pd.read_csv(gff_file, sep='\t', comment='#', header=None,
                             names=['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'])

        logging.info("Processing attributes...")
        attributes = gff_df['attributes'].str.split(';').apply(lambda x: dict(item.split('=') for item in x if '=' in item))
        attributes_expanded_df = attributes.apply(pd.Series)

        logging.info("Combining data...")
        gff_expanded_df = pd.concat([gff_df.drop(columns=['attributes']), attributes_expanded_df], axis=1)

        logging.info(f"Writing to '{output_xlsx}'...")
        gff_expanded_df.to_excel(output_xlsx, index=False, engine='openpyxl')  # Ensure using an efficient engine
        logging.info(f"Success: GFF file converted to '{output_xlsx}'.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
