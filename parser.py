import os
import numpy as np
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from collections import Counter
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, Dense
from keras_crf import CRFModel # This is from the keras-crf library
from keras_crf import losses, metrics
from tensorflow.keras.optimizers import Adam
import joblib
import json
# For evaluation (optional but recommended)
from sklearn_crfsuite.metrics import flat_classification_report

def read_conll_file(filepath: str) -> List[List[Tuple[str, str]]]:
    """
    Reads a CoNLL-formatted file and parses it into a list of sentences,
    where each sentence is a list of (word, tag) tuples.

    Args:
        filepath (str): The path to the .conll file.

    Returns:
        List[List[Tuple[str, str]]]: A list of sentences, each containing
                                     (word, tag) tuples.
    """
    sentences = []
    current_sentence = []
    
    # Using 'utf-8' is standard for CoNLL files, but if you encounter
    # decoding errors, try 'latin-1' or 'windows-1252' as a fallback.
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:  # Empty line indicates end of sentence
                    if current_sentence:
                        sentences.append(current_sentence)
                        current_sentence = []
                else:
                    # Assuming format is "word tag" (space-separated)
                    parts = line.split()
                    if len(parts) >= 2: # Ensure there's at least a word and a tag
                        word = parts[0]
                        tag = parts[1]
                        current_sentence.append((word, tag))
                    else:
                        print(f"Warning: Skipping malformed line in CoNLL file: '{line}'")

            # Add the last sentence if the file doesn't end with a blank line
            if current_sentence:
                sentences.append(current_sentence)
    except FileNotFoundError:
        print(f"Error: CoNLL file not found at {filepath}")
        return []
    except Exception as e:
        print(f"Error reading CoNLL file: {e}. Trying latin-1 encoding.")
        try: # Fallback to latin-1
            sentences = []
            current_sentence = []
            with open(filepath, 'r', encoding='latin-1') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        if current_sentence:
                            sentences.append(current_sentence)
                            current_sentence = []
                    else:
                        parts = line.split()
                        if len(parts) >= 2:
                            word = parts[0]
                            tag = parts[1]
                            current_sentence.append((word, tag))
                if current_sentence:
                    sentences.append(current_sentence)
        except Exception as e_latin1:
            print(f"Error reading CoNLL file even with latin-1: {e_latin1}")
            return []
            
    return sentences