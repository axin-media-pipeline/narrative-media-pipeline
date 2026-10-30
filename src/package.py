"""Bundle generated deliverables without source or intermediates."""
from zipfile import ZipFile, ZIP_DEFLATED

def package(paths, target):
    with ZipFile(target, "w", compression=ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, arcname=path.name)
