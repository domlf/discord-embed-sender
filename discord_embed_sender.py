import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QTextEdit, QLineEdit, QLabel, QHBoxLayout, QScrollArea, 
                             QCheckBox, QColorDialog)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QFile, QTextStream

CONFIG_FILE = 'config.json'

class EmbedApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.webhook_url_edit = QLineEdit(self)
        self.webhook_url_edit.setPlaceholderText('Enter webhook URL')
        layout.addWidget(self.webhook_url_edit)

        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText('Enter embed title')
        layout.addWidget(self.title_edit)

        self.url_edit = QLineEdit(self)
        self.url_edit.setPlaceholderText('Enter embed URL')
        layout.addWidget(self.url_edit)

        self.description_edit = QTextEdit(self)
        self.description_edit.setPlaceholderText('Enter embed description')
        layout.addWidget(self.description_edit)

        color_layout = QHBoxLayout()
        self.color_edit = QLineEdit(self)
        self.color_edit.setPlaceholderText('Enter embed color (hex code, e.g., #FF0000)')
        color_layout.addWidget(self.color_edit)

        self.color_button = QPushButton('Pick Color', self)
        self.color_button.clicked.connect(self.pick_color)
        color_layout.addWidget(self.color_button)

        layout.addLayout(color_layout)

        self.author_name_edit = QLineEdit(self)
        self.author_name_edit.setPlaceholderText('Enter author name')
        self.author_name_edit.textChanged.connect(self.toggle_author_fields)
        layout.addWidget(self.author_name_edit)

        self.author_link_edit = QLineEdit(self)
        self.author_link_edit.setPlaceholderText('Enter author link')
        self.author_link_edit.setEnabled(False)
        layout.addWidget(self.author_link_edit)

        self.author_icon_edit = QLineEdit(self)
        self.author_icon_edit.setPlaceholderText('Enter author icon URL')
        self.author_icon_edit.setEnabled(False)
        layout.addWidget(self.author_icon_edit)

        self.image_url_edit = QLineEdit(self)
        self.image_url_edit.setPlaceholderText('Enter image URL')
        layout.addWidget(self.image_url_edit)

        self.icon_url_edit = QLineEdit(self)
        self.icon_url_edit.setPlaceholderText('Enter icon URL')
        layout.addWidget(self.icon_url_edit)

        self.footer_text_edit = QLineEdit(self)
        self.footer_text_edit.setPlaceholderText('Enter footer text')
        layout.addWidget(self.footer_text_edit)

        self.fields_container = QVBoxLayout()
        self.fields = []

        self.add_field_button = QPushButton('Add Field', self)
        self.add_field_button.clicked.connect(self.add_field)
        layout.addWidget(self.add_field_button)

        self.fields_widget = QWidget()
        self.fields_widget.setLayout(self.fields_container)
        self.fields_scroll = QScrollArea()
        self.fields_scroll.setWidgetResizable(True)
        self.fields_scroll.setWidget(self.fields_widget)
        layout.addWidget(self.fields_scroll)

        button_layout = QHBoxLayout()
        self.send_button = QPushButton('Send Embed', self)
        self.send_button.clicked.connect(self.send_embed)
        button_layout.addWidget(self.send_button)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle('Discord Embed Sender')
        self.show()

        self.load_config()

        # Add initial fields
        for _ in range(3):
            self.add_field()

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_edit.setText(color.name())

    def toggle_author_fields(self):
        author_name_filled = bool(self.author_name_edit.text().strip())
        self.author_link_edit.setEnabled(author_name_filled)
        self.author_icon_edit.setEnabled(author_name_filled)

    def add_field(self):
        if len(self.fields) < 25:
            field_layout = QHBoxLayout()
            field_title_edit = QLineEdit(self)
            field_title_edit.setPlaceholderText(f'Field {len(self.fields)+1} title')
            field_layout.addWidget(field_title_edit)

            field_value_edit = QTextEdit(self)
            field_value_edit.setPlaceholderText(f'Field {len(self.fields)+1} value')
            field_layout.addWidget(field_value_edit)

            field_inline_checkbox = QCheckBox("Inline", self)
            field_layout.addWidget(field_inline_checkbox)

            self.fields_container.addLayout(field_layout)
            self.fields.append((field_title_edit, field_value_edit, field_inline_checkbox))
        else:
            print("Maximum of 25 fields reached")

    def send_embed(self):
        webhook_url = self.webhook_url_edit.text()
        if not webhook_url:
            print("Webhook URL is required")
            return

        title = self.title_edit.text()
        url = self.url_edit.text()
        description = self.description_edit.toPlainText()
        color = self.color_edit.text().lstrip('#')
        image_url = self.image_url_edit.text()
        icon_url = self.icon_url_edit.text()
        footer_text = self.footer_text_edit.text()

        author_name = self.author_name_edit.text()
        author_link = self.author_link_edit.text()
        author_icon = self.author_icon_edit.text()

        fields = []
        for field_title_edit, field_value_edit, field_inline_checkbox in self.fields:
            field_title = field_title_edit.text()
            field_value = field_value_edit.toPlainText()
            if field_title and field_value:
                fields.append({
                    'name': field_title,
                    'value': field_value,
                    'inline': field_inline_checkbox.isChecked()
                })

        embed = {
            'embeds': [
                {
                    'title': title,
                    'url': url,
                    'description': description,
                    'color': int(color, 16) if color else 0xFFFFFF,
                    'author': {
                        'name': author_name,
                        'url': author_link if author_name else None,
                        'icon_url': author_icon if author_name else None
                    },
                    'image': {
                        'url': image_url
                    },
                    'thumbnail': {
                        'url': icon_url
                    },
                    'footer': {
                        'text': footer_text
                    },
                    'fields': fields
                }
            ]
        }

        # Remove None entries from author if author name is empty
        if not author_name:
            embed['embeds'][0].pop('author')

        response = requests.post(webhook_url, json=embed)
        if response.status_code == 204:
            print('Embed sent successfully!')
        else:
            print(f'Failed to send embed: {response.status_code}, {response.text}')

        self.save_config()

    def clear_fields(self):
        self.title_edit.clear()
        self.url_edit.clear()
        self.description_edit.clear()
        self.color_edit.clear()
        self.author_name_edit.clear()
        self.author_link_edit.clear()
        self.author_icon_edit.clear()
        self.image_url_edit.clear()
        self.icon_url_edit.clear()
        self.footer_text_edit.clear()
        for field_title_edit, field_value_edit, field_inline_checkbox in self.fields:
            field_title_edit.clear()
            field_value_edit.clear()
            field_inline_checkbox.setChecked(False)
        print("Fields cleared")

    def save_config(self):
        config = {
            'webhook_url': self.webhook_url_edit.text(),
            'title': self.title_edit.text(),
            'url': self.url_edit.text(),
            'description': self.description_edit.toPlainText(),
            'color': self.color_edit.text(),
            'author_name': self.author_name_edit.text(),
            'author_link': self.author_link_edit.text(),
            'author_icon': self.author_icon_edit.text(),
            'image_url': self.image_url_edit.text(),
            'icon_url': self.icon_url_edit.text(),
            'footer_text': self.footer_text_edit.text(),
            'fields': [
                {
                    'title': field_title_edit.text(),
                    'value': field_value_edit.toPlainText(),
                    'inline': field_inline_checkbox.isChecked()
                }
                for field_title_edit, field_value_edit, field_inline_checkbox in self.fields
            ]
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        print("Configuration saved")

    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.webhook_url_edit.setText(config.get('webhook_url', ''))
                self.title_edit.setText(config.get('title', ''))
                self.url_edit.setText(config.get('url', ''))
                self.description_edit.setPlainText(config.get('description', ''))
                self.color_edit.setText(config.get('color', ''))
                self.author_name_edit.setText(config.get('author_name', ''))
                self.author_link_edit.setText(config.get('author_link', ''))
                self.author_icon_edit.setText(config.get('author_icon', ''))
                self.image_url_edit.setText(config.get('image_url', ''))
                self.icon_url_edit.setText(config.get('icon_url', ''))
                self.footer_text_edit.setText(config.get('footer_text', ''))

                fields = config.get('fields', [])
                for i, field in enumerate(fields):
                    if i < len(self.fields):
                        self.fields[i][0].setText(field.get('title', ''))
                        self.fields[i][1].setPlainText(field.get('value', ''))
                        self.fields[i][2].setChecked(field.get('inline', False))
                    else:
                        self.add_field()
                        self.fields[-1][0].setText(field.get('title', ''))
                        self.fields[-1][1].setPlainText(field.get('value', ''))
                        self.fields[-1][2].setChecked(field.get('inline', False))

                print("Configuration loaded")
        except FileNotFoundError:
            print("No configuration file found")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmbedApp()
    sys.exit(app.exec_())
