#!/usr/bin/env python3

import requests
import argparse
from bs4 import BeautifulSoup
from typing import Dict, Tuple
import csv
import re

DEFAULT_HEADERS = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

def main(start_id: int, output_dir: str, limit: int):
  print(f'[+] downloading MTG cards starting with id {start_id}; saving to {output_dir}')
  images_list_file = f'{output_dir}/list.csv'
  with open(images_list_file, 'w') as fh:
    csv_writer = csv.writer(fh)
    for id in range(start_id, start_id + limit):
      print(f' [+] downloading {id} ... ', end='', flush=True)
      title, content = download_card(id)
      filename, output_path = save_file(output_dir, title, content)
      csv_writer.writerow([title, filename])
      print(f'{title} | saved as {output_path}')

def save_file(dir: str, title: str, content: bytes) -> Tuple[str, str]:
  filename = re.sub(r'\W', '', title.lower())
  output_path = f'{dir}/{filename}.jpg'
  with open(output_path, 'wb') as fh:
    fh.write(content)
  return filename, output_path


def download_card(id: int) -> Tuple[str, bytes]:
  base_url = 'https://gatherer.wizards.com'
  card_url = f'{base_url}/Pages/Card/Details.aspx?multiverseid={id}'
  res = requests.get(card_url, headers=DEFAULT_HEADERS)
  if res.ok:
    doc = BeautifulSoup(res.text, features='html.parser')
    image_container = doc.find('div', class_='cardImage')
    image = image_container.find('img')
    image_url = f'{base_url}/{image["src"][6:]}'
    image_res = requests.get(image_url, headers=DEFAULT_HEADERS)
    if image_res.ok:
      image_content = image_res.content
      card_name = image['alt']
      return (card_name, image_content)
  raise Exception('ERROR!')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--start_id', required=True, type=int)
  parser.add_argument('--output_dir', required=True, type=str)
  parser.add_argument('--limit', type=int, default=10)
  args = parser.parse_args()
  main(args.start_id, args.output_dir, args.limit)
