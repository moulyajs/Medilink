import subprocess
import os


def pdf_to_images_docker(pdf_path, out_dir):
    pdf_path = os.path.abspath(pdf_path)
    out_dir = os.path.abspath(out_dir)

    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.path.dirname(pdf_path)}:/input",
        "-v", f"{out_dir}:/output",
        "poppler-service",
        "/input/" + os.path.basename(pdf_path),
        "/output/page",
        "-png"
    ]

    subprocess.run(cmd, check=True)

    return sorted([
        os.path.join(out_dir, f)
        for f in os.listdir(out_dir)
        if f.startswith("page")
    ])
