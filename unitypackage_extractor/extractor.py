import tarsafe
import tempfile
import sys
import os
import time
import shutil
import re
from pathlib import Path


def count_files(packagePath, encoding='utf-8'):
    """
  Counts the number of files in the .unitypackage
  """
    file_count = 0
    with tarsafe.open(name=packagePath, encoding=encoding) as upkg:
        for _ in upkg:
            file_count += 1
    return file_count


def extractPackage(packagePath, outputPath=None, encoding='utf-8'):
    """
  Extracts a .unitypackage into the current directory
  @param {string} packagePath The path to the .unitypackage
  @param {string} [outputPath=os.getcwd()] Optional output path, otherwise will use cwd
  """
    if not outputPath:
        outputPath = os.getcwd()

    total_files = count_files(packagePath, encoding)

    with tempfile.TemporaryDirectory() as tmpDir:
        with tarsafe.open(name=packagePath, encoding=encoding) as upkg:
            extracted_files = 0
            for member in upkg:
                upkg.extract(member, path=tmpDir)
                extracted_files += 1
                progress = extracted_files / total_files * 100
                sys.stdout.write("\rExtracting... Progress: %.2f%% (%d/%d)" % (progress, extracted_files, total_files))
                sys.stdout.flush()

                assetEntryDir = os.path.join(tmpDir, member.name)
                # Rest of your extraction logic here...

    print("\nExtraction completed.")


def cli(args):
    """
  CLI entrypoint, takes CLI arguments array
  """
    if not args:
        raise TypeError(
            "No .unitypackage path was given. \n\nUSAGE: unitypackage_extractor [XXX.unitypackage] (optional/output/path)")

    startTime = time.time()
    extractPackage(args[0], args[1] if len(args) > 1 else "")
    print("--- Finished in %s seconds ---" % (time.time() - startTime))


if __name__ == "__main__":
    cli(sys.argv[1:])
