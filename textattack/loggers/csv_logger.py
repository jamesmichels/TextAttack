"""
Attack Logs to CSV
========================
"""

import csv

import pandas as pd

from textattack.shared import AttackedText, logger

from .logger import Logger


class CSVLogger(Logger):
    """Logs attack results to a CSV."""

    def __init__(self, filename="results.csv", color_method="file"):
        logger.info(f"Logging to CSV at path {filename}")
        self.filename = filename
        self.color_method = color_method
        self.row_list = []
        self._flushed = True
        self.df = pd.DataFrame()

    def log_attack_result(self, result):
        original_text, perturbed_text = result.diff_color(self.color_method)
        original_text = original_text.replace("\n", AttackedText.SPLIT_TOKEN)
        perturbed_text = perturbed_text.replace("\n", AttackedText.SPLIT_TOKEN)
        result_type = result.__class__.__name__.replace("AttackResult", "")
        row = {
            "original_text": original_text,
            "perturbed_text": perturbed_text,
            "original_score": result.original_result.score,
            "perturbed_score": result.perturbed_result.score,
            "original_output": result.original_result.output,
            "perturbed_output": result.perturbed_result.output,
            "ground_truth_output": result.original_result.ground_truth_output,
            # Add new lines for words changed, original probability, and perturbed probability
            # Words changed checks words individually, outputs number of words different between the two.
            "words changed":sum(1 for word1, word2 in zip(original_text.split(), perturbed_text.split()) if word1 != word2),
            "original_proba:":result.original_result.get_colored_output(self.color_method),
            "perturbed_proba":result.perturbed_result.get_colored_output(self.color_method) if result_type == "Successful" else result_type,
            "num_queries": result.num_queries,
            "result_type": result_type,
        }
        self.row_list.append(row)
        self.df = pd.DataFrame.from_records(self.row_list)
        self._flushed = False

    def flush(self):
        self.df.to_csv(self.filename, quoting=csv.QUOTE_NONNUMERIC, index=False)
        self._flushed = True

    def close(self):
        # self.fout.close()
        super().close()

    def __del__(self):
        if not self._flushed:
            logger.warning("CSVLogger exiting without calling flush().")
