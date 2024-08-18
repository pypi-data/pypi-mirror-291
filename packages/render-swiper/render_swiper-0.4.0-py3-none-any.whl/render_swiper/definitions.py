# AUTO GENERATED FILE - DO NOT EDIT!

from render import Component, create_callback, InputComponent


class Swiper(InputComponent):
    Module = "swiper/react"
    JSXName = "Swiper"
    InputName = "value"
    NewValuePath = "activeIndex"
    ChangeEventName = "onSlideChange"
    CALLBACKS = ["onKeyPress", "onClick"]
    ATTRIBUTES = ["style", "className", "id", "navigation", "lazy"]

    def __init__(
        self,
        children=None,
        key=None,
        style=None,
        className=None,
        id=None,
        onKeyPress=None,
        onClick=None,
        navigation=None,
        lazy=None,
        controller=None,
        onSlideChange=None,
        value=None,
        defaultValue=None,
    ):
        super().__init__(key, controller, children, onSlideChange, value, defaultValue)
        self.style = style
        self.className = className
        self.id = id
        self.onKeyPress = create_callback(onKeyPress, "onKeyPress")
        self.onClick = create_callback(onClick, "onClick")
        self.navigation = navigation
        self.lazy = lazy


class SwiperSlide(Component):
    Module = "swiper/react"
    JSXName = "SwiperSlide"
    CALLBACKS = ["onKeyPress", "onClick"]
    ATTRIBUTES = ["style", "className", "id"]

    def __init__(
        self,
        children=None,
        key=None,
        style=None,
        className=None,
        id=None,
        onKeyPress=None,
        onClick=None,
        controller=None,
    ):
        super().__init__(key, controller, children)
        self.style = style
        self.className = className
        self.id = id
        self.onKeyPress = create_callback(onKeyPress, "onKeyPress")
        self.onClick = create_callback(onClick, "onClick")
