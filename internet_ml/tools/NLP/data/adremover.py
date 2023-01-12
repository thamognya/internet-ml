from typing import List

from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


class AdRemover:
    def __init__(self, rules: list[str]):
        self.rules = set()
        with ThreadPoolExecutor(max_workers=500) as executor:
            future_to_rule = {
                executor.submit(requests.get, rule): rule for rule in rules
            }
            for future in as_completed(future_to_rule):
                rule = future_to_rule[future]
                try:
                    response = future.result()
                    self.rules.update(response.text.splitlines())
                except Exception as e:
                    print(f"{rule} generated an exception: {e}")

    def remove_ads(self, html: str) -> str:
        """Remove ads from the HTML based on the ad block rules"""
        with ThreadPoolExecutor(max_workers=500) as executor:
            future_to_rule = {
                executor.submit(html.replace, rule, ""): rule for rule in self.rules
            }
            for future in as_completed(future_to_rule):
                rule = future_to_rule[future]
                try:
                    html = future.result()
                except Exception as e:
                    print(f"{rule} generated an exception: {e}")
        return html
