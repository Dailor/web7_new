import pygame


def ApplySettings(funcSettings):
    def wrapper(self, *args, **kwargs):
        funcSettings(self, *args, **kwargs)
        self.apply_settings()

    return wrapper


def negativ_color(rgb):
    return tuple(map(lambda x: 255 - x, rgb))


class ButtonBase(pygame.sprite.Sprite):
    def __init__(self, group, pos, text, margin_top_bottom=10, margin_left_right=10, font_size=None,
                 background_color=None, text_color=None):
        super().__init__(group)

        self.pos = pos
        self.text = text

        if font_size is None:
            self.font_size = 20
        else:
            self.font_size = font_size

        if background_color is None:
            self.background_color = (0, 0, 0)
        else:
            self.background_color = background_color

        if text_color is None:
            self.text_color = (52, 217, 143)
        else:
            self.text_color = text_color

        self.margin_top_bottom = margin_top_bottom
        self.margin_left_right = margin_left_right

        self.border_width = self.font_size // 8

        self.apply_settings()

    def apply_settings(self):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.text_color)

        text_w = text.get_width()
        text_h = text.get_height()

        box_w = text_w + 2 * self.margin_left_right
        box_h = text_h + 2 * self.margin_top_bottom

        self.image = pygame.Surface((box_w, box_h), pygame.SRCALPHA, 32)
        self.image.fill(self.background_color)
        self.image.blit(text, (box_w - text_w - self.margin_left_right, box_h - text_h - self.margin_top_bottom))
        pygame.draw.rect(self.image, self.text_color, (0, 0, box_w, box_h), self.border_width)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def check_buttons_group(self, group, need):
        if isinstance(group, need) is False:
            raise Exception("Класс не соответсвует группе")

    def get_width(self):
        return self.rect.w

    def get_height(self):
        return self.rect.h

    @ApplySettings
    def set_border_width(self, width):
        self.border_width = width

    @ApplySettings
    def set_pos(self, pos):
        self.pos = pos

    @ApplySettings
    def set_text(self, text):
        self.text = text

    @ApplySettings
    def set_font_size(self, font_size):
        self.font_size = font_size

    @ApplySettings
    def set_background_color(self, color):
        self.background_color = color

    @ApplySettings
    def set_text_color(self, color):
        self.text_color = color

    @ApplySettings
    def set_margin_left_right(self, margin):
        self.margin_left_right = margin

    @ApplySettings
    def set_margin_top_bottom(self, margin):
        self.margin_top_bottom = margin

    def draw_border(self, color):
        pygame.draw.rect(self.image, color, (0, 0, self.rect.w, self.rect.h),
                         self.border_width)

    def make_active(self, pos):
        if self.check_on_press(pos):
            self.draw_border(negativ_color(self.text_color))
            return True
        return False

    def make_deactive(self):
        self.draw_border(self.text_color)

    def check_on_press(self, pos):
        x, y = pos
        if ((self.rect.x <= x <= self.rect.w + self.rect.x) and (self.rect.y <= y <= self.rect.h + self.rect.y)):
            return True
        return False


class DefaultButton(ButtonBase):
    def __init__(self, group, *args, **kwargs):
        self.check_buttons_group(group, ButtonsGroup)
        super().__init__(group, *args, **kwargs)
        self.pressed = False
        self.on_press_func = None
        self.on_press_func_args = None
        self.on_press_func_kwargs = None

    def set_on_press_func(self, func, *args, **kwargs):
        self.on_press_func = func
        self.on_press_func_args = args
        self.on_press_func_kwargs = kwargs

    def make_active(self, pos):
        self.pressed = super().make_active(pos)
        return self.pressed

    def make_deactive(self):
        if self.pressed:
            super().make_deactive()
            self.on_press()
            self.pressed = False

    def on_press(self):
        if self.on_press_func is None:
            raise Exception("Реализуй метод :)")
        return self.on_press_func(*self.on_press_func_args, **self.on_press_func_kwargs)


class RadioButton(ButtonBase):
    def __init__(self, group, *args, **kwargs):
        self.check_buttons_group(group, RadioButtonsGroup)
        super().__init__(group, *args, **kwargs)
        self.selected = False
        if len(group) == 1:
            self.make_active((self.rect.x, self.rect.y))

    def make_active(self, pos):
        if super().make_active(pos):
            self.selected = True
            return True
        return False

    def make_deactive(self):
        super().make_deactive()
        self.selected = False


class ButtonsGroup(pygame.sprite.Group):
    def __init__(self, *args: RadioButton):
        super().__init__(*args)

    def check_press(self, pos):
        for btn in self.sprites():
            if btn.make_active(pos):
                return btn

    def check_release(self):
        for btn in self.sprites():
            btn.make_deactive()


class RadioButtonsGroup(ButtonsGroup):
    def __init__(self, *args: RadioButton):
        super().__init__(*args)

    def check_press(self, pos):
        btn_selected = super().check_press(pos)
        if btn_selected is None:
            return
        for btn in self.sprites():
            if btn_selected is btn:
                continue
            if self in btn.groups():
                btn.make_deactive()

    def check_release(self):
        pass

    def get_selected(self):
        for btn in self.sprites():
            if btn.selected:
                return btn


class ButtonGroupOfGroups:
    def __init__(self, *groups):
        self.groups = set(groups)

    def add(self, group):
        self.groups.add(group)

    def draw(self, screen):
        for gr in self.groups:
            gr.draw(screen)

    def check_press(self, pos):
        for gr in self.groups:
            gr.check_press(pos)

    def check_release(self):
        for gr in self.groups:
            gr.check_release()


def test_how_work():
    def test_func():
        print(btn_group_1.get_selected().text)
        print(btn_group_2.get_selected().text)

    pygame.init()
    size = 1000, 500
    screen = pygame.display.set_mode(size)
    screen.fill((12, 121, 170))

    btn_group_1 = RadioButtonsGroup()
    btn_group_2 = RadioButtonsGroup()
    btn_group_def = ButtonsGroup()

    btn_def = DefaultButton(btn_group_def, (250, 50 * 5), "Print ", font_size=50)
    btn_def.set_on_press_func(test_func)

    btn1_1 = RadioButton(btn_group_1, (50, 50), "group_1_1", font_size=50)
    btn1_2 = RadioButton(btn_group_1, (50, 50 * 3), "group_1_2", font_size=50)

    btn2_1 = RadioButton(btn_group_2, (50 * 9, 50), "group_2_1", font_size=50)
    btn2_2 = RadioButton(btn_group_2, (50 * 9, 50 * 3), "group_2_2", font_size=50)

    all_btns_groups = ButtonGroupOfGroups(btn_group_def, btn_group_1, btn_group_2)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    all_btns_groups.check_press(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    all_btns_groups.check_release()

        all_btns_groups.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    test_how_work()
