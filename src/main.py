import flet as ft
from dataclasses import dataclass, field
import shutil, os
import pypdf as pd

@dataclass
class Pre_Upload:
    picked_files: list = field(default_factory=list)

@dataclass
class Uploading:
    progress: float = 0.0

@dataclass
class Upload_Complete:
    success: bool = True

async def main(page: ft.Page):
    page.session_state = Pre_Upload()
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    content = ft.Column()
    page.add(content)

    def render():
        state = page.session_state
        content.controls.clear()

        if isinstance(state, Pre_Upload):
            content.controls.append(ft.Text("Upload Files", size=50))
            content.controls.append(
                ft.Button(
                    content="test",
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
            content.controls.append(ft.Text("WP"))
            content.controls.append(ft.Text("Files Saved", size=50))
            for name in saved:
                content.controls.append(ft.Text(f"• {name}"))

        content.update()

    async def clear():
        page.session_state = Upload_Complete()
        print("wow")
        render()
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


"""
Testing visual GUI purposes

def main(page: ft.Page):
    main.state = state
    print(main.state.__class__)
    if(main.state == Pre_Upload):
        picked_files: list[ft.FilePickerFile] = field(default_factory=list)



        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, key="upload", on_click=file_picker
        )

        page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Container(
                    content=ft.Text("Upload File", size = 50),
                    alignment=ft.Alignment.CENTER,
                ),
            )
        )
"""
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

    #Files not uploaded due to copyright issues

    #Pdf_write = WriterRotateStartLeft(path="20260819083638176.pdf")

    #Pdf_write.write("Violin 003 Solo fixed.pdf")
    shutil.rmtree("saved_files")
    os.close