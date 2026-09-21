from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw


PDF_PATH = Path(r"D:\Mini_project\output\pdf\guide explanation.pdf")
RENDER_DIR = Path(r"D:\Mini_project\tmp\pdfs\rendered")


def main() -> None:
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    document = pdfium.PdfDocument(str(PDF_PATH))
    rendered: list[Path] = []

    for page_index in range(len(document)):
        page = document[page_index]
        image = page.render(scale=1.5).to_pil().convert("RGB")
        output = RENDER_DIR / f"page-{page_index + 1:02d}.png"
        image.save(output, optimize=True)
        rendered.append(output)

    thumb_width = 310
    gap = 18
    label_height = 28
    sheets: list[Path] = []
    for sheet_index in range(0, len(rendered), 6):
        batch = rendered[sheet_index : sheet_index + 6]
        thumbs: list[Image.Image] = []
        for path in batch:
            image = Image.open(path).convert("RGB")
            ratio = thumb_width / image.width
            thumbs.append(image.resize((thumb_width, int(image.height * ratio))))

        thumb_height = max(image.height for image in thumbs)
        sheet = Image.new("RGB", (gap * 4 + thumb_width * 3, gap * 3 + (thumb_height + label_height) * 2), "#d8dee5")
        draw = ImageDraw.Draw(sheet)
        for offset, (path, thumb) in enumerate(zip(batch, thumbs)):
            row, column = divmod(offset, 3)
            x = gap + column * (thumb_width + gap)
            y = gap + row * (thumb_height + label_height + gap)
            sheet.paste(thumb, (x, y + label_height))
            draw.text((x, y + 5), path.stem.replace("page-", "Page "), fill="#182532")

        sheet_path = RENDER_DIR / f"contact-sheet-{sheet_index // 6 + 1}.png"
        sheet.save(sheet_path, optimize=True)
        sheets.append(sheet_path)

    print(f"Rendered {len(rendered)} pages and {len(sheets)} contact sheets to {RENDER_DIR}")


if __name__ == "__main__":
    main()
