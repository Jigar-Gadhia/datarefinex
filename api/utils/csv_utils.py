import pandas as pd
from api.utils.storage_utils import upload_to_hf
import gdown
import chardet
import logging
import os

logger = logging.getLogger(__name__)


def process_csv_file(file_url: str):
    try:
        # Download if Google Drive
        if "drive.google.com" in file_url:
            gdown.download(file_url, "downloaded.csv", quiet=False)
            file_url = "downloaded.csv"

        if not os.path.exists(file_url):
            raise FileNotFoundError(file_url)

        # Clean null bytes
        with open(file_url, "rb") as f:
            raw = f.read().replace(b"\x00", b"")
        with open(file_url, "wb") as f:
            f.write(raw)

        # Detect encoding
        detected = chardet.detect(raw[:100000])
        encoding = detected.get("encoding") or "utf-8"
        conf = detected.get("confidence", 0)
        logger.info(f"[Encoding detected] {encoding} (confidence={conf})")

        def read_chunks(enc):
            total = 0
            for chunk in pd.read_csv(
                file_url,
                chunksize=50000,
                encoding=enc,
                encoding_errors="replace",
                engine="python",
                on_bad_lines="skip",
                sep=None,  # autodetect delimiter
                quoting=3,  # <- disable quote parsing
                quotechar='"',  # still define it
                escapechar="\\",  # escape sequences safe
            ):
                chunk = chunk.drop_duplicates().dropna()
                total += len(chunk)
                chunk.to_csv("cleaned_data.csv", mode="a", index=False)
            return total

        output_file = "cleaned_data.csv"
        total_rows = 0
        try:
            total_rows = read_chunks(encoding)
        except UnicodeDecodeError:
            logger.warning(f"[Encoding fallback] Retrying with latin1")
            total_rows = read_chunks("latin1")

        remote_path = upload_to_hf(output_file)
        return {
            "uploaded": remote_path,
            "file": output_file,
            "status": "done",
            "encoding_used": encoding,
            "rows_cleaned": total_rows,
        }

    except Exception as e:
        import traceback

        trace = traceback.format_exc()
        logger.warning(trace)
        return {
            "uploaded": None,
            "file": None,
            "status": "error",
            "error": str(e),
            "trace": trace,
        }
