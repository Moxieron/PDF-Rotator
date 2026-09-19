import flet as ft
from dataclasses import dataclass, field
import shutil, os
import asyncio
import pypdf as pd
from pathlib import Path

@dataclass
class Pre_Upload:
    picked_files: list = field(default_factory=list)

@dataclass
class Uploading:
    progress: float = 0.0

@dataclass
class Upload_Complete:
    success: bool = True

@dataclass
class Finish:
    Done: bool = True

SAVED_DIR = Path("saved_files")
OUTPUT_DIR = Path(r"C:\Users\hughh\OneDrive\Documents\PDF Rotator")
async def main(page: ft.Page):
    page.session_state = Pre_Upload()
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    content = ft.Column()
    page.add(content)

    def render():

        state = page.session_state
        content.controls.clear()
        print(
            'ccc'
        )

        if isinstance(state, Pre_Upload):

            content.controls.append(ft.Text("Upload Files", size=50))
            content.controls.append(
                ft.Button(
                    content="Select File(s)",
                    on_click=handle_pick,
                )
            )

        elif isinstance(state, Uploading):

            saved = os.listdir("saved_files") if os.path.exists("saved_files") else []
            content.controls.append(ft.Text("Files Saved", size=50))

            for name in saved:
                content.controls.append(ft.Text(f"• {name}"))

            content.controls.append(ft.Button(content="clear?", on_click= clear))

        elif isinstance(state, Upload_Complete):

            saved = os.listdir("saved_files") if os.path.exists("saved_files") else []

            col_width = 320
            button_width = 130      
            col_gap = 10        

            content.controls.append(ft.Text("WP"))

            content.controls.append(
                ft.Row(
                    spacing=col_gap,
                    controls=[
                        ft.Container(
                            content=ft.Text("Files Saved", weight=ft.FontWeight.BOLD),
                            width=col_width,
                        ),

                        ft.Container(
                            content=ft.Text("Select Orientation of Starting Page", weight=ft.FontWeight.BOLD),
                            width=button_width * 2 + col_gap,
                        ),
                    ],
                )
            )

            for name in saved:
                content.controls.append(
                    ft.Row(
                        spacing=col_gap,
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    f"• {name}",
                                    no_wrap=True,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                width=col_width,
                            ),
                            ft.Button(content="Start Left", data=name, width=button_width, on_click=FileCleaning_Start_Left),
                            ft.Button(content="Start Right", data=name, width=button_width, on_click=FileCleaning_Start_Right),
                        ],
                    )
                )

            content.controls.append(ft.Button(content = "Done?", width= button_width*2, on_click = ending))

        elif isinstance(state, Finish):

            content.controls.append(ft.Text(value="Done", size= 60))

        content.update()

    def process_pdf(name, rotate_fn):

        src = SAVED_DIR / name                           
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)     
        dest = OUTPUT_DIR / f"{src.stem}_Fixed.pdf"       

        writer = rotate_fn(src)

        with open(dest, "wb") as d:
            writer.write(d)

        return dest

    async def clear(e):                                 

        page.session_state = Upload_Complete()
        render()

    async def ending(e):

        page.session_state = Finish()
        render()

    async def FileCleaning_Start_Left(e):

        await asyncio.to_thread(process_pdf, e.control.data, WriterRotateStartLeft)

        e.control.content = "Done!"
        e.control.update()

    async def FileCleaning_Start_Right(e):

        await asyncio.to_thread(process_pdf, e.control.data, WriterRotateStartRight)

        e.control.content = "Done!"
        e.control.update()
    async def handle_pick(e):

        files = await file_picker.pick_files(allow_multiple=True)

        if files:
            os.makedirs("saved_files", exist_ok=True)

            for f in files:
                shutil.copy(f.path, f"saved_files/{f.name}")
                print(f"Saved {f.name}")

            page.session_state = Uploading()

            render()

    render()


# For scans starting 90 deg Clockwise from center
def WriterRotateStartLeft(path) -> pd.PdfWriter:

    writer = pd.PdfWriter()
    reader = pd.PdfReader(path)

    for a in range(len(reader.pages)):
        print(a)
        page = reader.pages[a]
        writer.add_page(page)

        if(a%2 == 0):
            writer.pages[a].rotate(90)
        else:
            writer.pages[a].rotate(270)       

    return writer
# For scans staring 90 deg CCW from center         
def WriterRotateStartRight(path) -> pd.PdfWriter:

    writer = pd.PdfWriter()
    reader = pd.PdfReader(path, strict=True)

    for a in range(len(reader.pages)):
        print(a)
        page = reader.pages[a]
        writer.add_page(page)

        if(a%2 == 0):
            print("hi")
            writer.pages[a].rotate(270)
        else:
            print("bye")
            writer.pages[a].rotate(90)    

    return writer  

if __name__ == "__main__":

    ft.run(main) 

    shutil.rmtree("saved_files")
    os.close