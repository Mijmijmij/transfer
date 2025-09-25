import argparse
import logging
import os
import pandas as pd
import re
import yaml
from dateutil import parser as date_parser
from typing import Optional

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка паттернов из config.yaml
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)['patterns']
patterns = {k: re.compile(v) for k, v in cfg.items()}

def extract_sid(dep: str, shr: str, arr: str) -> Optional[int]:
    """Извлекает flight_id из полей DEP, SHR, ARR."""
    for block in (dep, shr, arr):
        if pd.isna(block):
            continue
        m = patterns['sid'].search(block)
        if m:
            return int(float(m.group(1)))
    return None

def coord_to_decimal(coord: str) -> Optional[str]:
    """Очищает строку с координатами."""
    if pd.isna(coord):
        return None
    return coord.strip()

def parse_row(row: pd.Series) -> dict:
    """Парсит одну строку Excel и возвращает dict для БД."""
    dep = row.get('DEP', '')
    shr = row.get('SHR', '')
    arr = row.get('ARR', '')

    sid = extract_sid(dep, shr, arr) or 0

    # Разбор времени
    atd = row.get('ATD')
    ata = row.get('ATA')
    departure_time = date_parser.parse(str(atd), fuzzy=True).time() if pd.notna(atd) else None
    arrival_time = date_parser.parse(str(ata), fuzzy=True).time() if pd.notna(ata) else None

    return {
        'flight_id': sid,
        'drone_type': row.get('TYP', ''),
        'departure_date': None,
        'departure_time': departure_time,
        'departure_coords': coord_to_decimal(row.get('LATDEP')),
        'arrival_date': None,
        'arrival_time': arrival_time,
        'arrival_coords': coord_to_decimal(row.get('LATARR')),
        'duration': None
    }

def main():
    parser = argparse.ArgumentParser(description="Drone flights parser")
    parser.add_argument('input', help="Path to input Excel (.xlsx)")
    parser.add_argument('-o', '--output', required=True, help="Path to output CSV")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        logger.error(f"Input file not found: {args.input}")
        return

    df = pd.read_excel(args.input, engine='openpyxl')
    logger.info(f"Read {len(df)} rows from {args.input}")

    records = [parse_row(row) for _, row in df.iterrows()]
    out_df = pd.DataFrame(records)
    out_df.to_csv(args.output, index=False)
    logger.info(f"Wrote parsed data to {args.output}")

if __name__ == "__main__":
    main()
