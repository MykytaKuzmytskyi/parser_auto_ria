import csv
import os

from django.core.management import call_command

from auto_card.models import Card
from parser_auto_ria.settings import BASE_DIR


def dumpdata_to_json(output_json_path: str):
    fixture_file_name = os.path.join(BASE_DIR, output_json_path)
    call_command('dumpdata', 'auto_card.Card', output=fixture_file_name)
    print(f'Data has been dumped to {fixture_file_name}')


def dumpdata_to_csv(output_csv_path: str):
    dumps_dir = os.path.join(BASE_DIR, 'dumps')
    csv_file_path = os.path.join(dumps_dir, output_csv_path)

    batch_size = 1000

    card_fields = [field.name for field in Card._meta.get_fields()]

    total_records = Card.objects.count()
    offset = 0

    with open(csv_file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=card_fields)
        writer.writeheader()

        while offset < total_records:
            cards = Card.objects.all()[offset:offset + batch_size].values(*card_fields)
            writer.writerows(cards)
            offset += batch_size

    print(f'Path - {csv_file_path}')
    print(f'Data has been dumped to {output_csv_path}')
