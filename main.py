from src.analyzer import analyze
import src.config as cfg

if __name__ == "__main__":
    analyze(cfg.INPUT_FILE, cfg.OUTPUT_DIR)