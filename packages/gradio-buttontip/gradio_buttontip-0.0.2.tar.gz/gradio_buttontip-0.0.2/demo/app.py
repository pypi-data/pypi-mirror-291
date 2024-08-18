
import gradio as gr
from gradio_buttontip import ButtonTip

def button_click():
    return "Button clicked!"

demo = gr.Interface(
    title="Button with Tooltip",
    description="This interface showcases a button with a tooltip.",
    fn=button_click,
    inputs=[
        ButtonTip(
            tooltip="Tooltip Text",
            tooltip_color="white",  # Custom color
            tooltip_background_color="red",
            x=120,  # No horizontal offset
            y=-20,  # Above the button
            value="Top Button"
        ),
        ButtonTip(
            tooltip="Tooltip Text",
            tooltip_color="white",  # Custom color
            tooltip_background_color="green",
            x=140,  # No horizontal offset
            y=20,  # Below the button
            value="Bottom Button"
        )
    ],
    outputs="text",
)


if __name__ == "__main__":
    demo.launch()
