
def clean_layout(layout, delete=False):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
                 if delete:
                     widget.hide()
             else:
                 clean_layout(item.layout(), delete)