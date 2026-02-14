import arcade
from arcade.gui import UIManager, UIFlatButton, UIInputText
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
import requests
from geocode_coords import geocode_coords
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Request"
MAP_FILE = 'map.png'


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('map.png')

    def update(self):
        self.texture = arcade.load_texture('map.png')


class MyGUIWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)
        self.Player = Player()
        self.Player.center_x = SCREEN_WIDTH // 2
        self.Player.center_y = SCREEN_HEIGHT // 2
        self.Player.width = 500
        self.Player.height = 300
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.Player)

        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout(y=SCREEN_HEIGHT // 3)  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=False, space_between=10)
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        # Здесь добавим ВСЕ виджеты — по порядку!
        self.input_text = UIInputText(x=0, y=0, width=200, height=50, text_color=arcade.color.WHITE,
                                      border_color=arcade.color.BLACK,
                                      fon_size=14, text='Enter background color')
        self.box_layout.add(self.input_text)
        flat_button = UIFlatButton(width=200, height=50, color=arcade.color.BLUE,
                                   text='Change color')
        flat_button.on_click = self.on_button_click
        self.box_layout.add(flat_button)

    def on_button_click(self, event):
        ll, span = geocode_coords(self.input_text.text)
        get_image(ll, span)
        self.Player.update()

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()
        self.manager.draw()


def setup_game(width=800, height=600, title="Background Color"):
    game = MyGUIWindow(width, height, title)
    return game


def get_image(ll, span):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    ll_spn = f'll={ll}&spn={span}'

    map_request = f"{server_address}{ll_spn}&apikey={api_key}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(MAP_FILE, "wb") as file:
        file.write(response.content)


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
