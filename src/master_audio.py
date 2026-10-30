"""Preserve lossless audio; loudness normalization is a future task."""
import shutil

def master(source, destination):
    shutil.copyfile(source, destination)
