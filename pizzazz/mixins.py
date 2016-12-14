from input import ButtonCallbacks, ButtonManager, PinnedCallbacks, ACTION_PRESSED, ACTION_RELEASED, ACTION_HELD
from utils import not_implemented


class AbstractButtonControllerMixin(object):

    def __init__(self):
        self._button_map = {}
        self._setup_buttons()

    def _handle_button_event(self, event):
        if self._button_map.has_key(event.name):
            btn = self._button_map[event.name]
            callbacks = btn.callbacks
            callback = None
            if event.action == ACTION_PRESSED:
                callback = callbacks.pressed
            elif event.action == ACTION_RELEASED:
                callback = callbacks.released
            elif event.action == ACTION_HELD:
                callback = callbacks.held
            if callback is not None:
                callback()

    def _setup_buttons(self):
        raise NotImplementedError(not_implemented(self, "_setup_buttons()"))

    def _setup_button(self, name, pin, pressed_callback=None, released_callback=None, held_callback=None):
        if self._button_map.has_key(name) and self._button_map[name] is not None:
            # TODO: Specialize the error here
            raise ValueError("Button {} has already been set up on pin {}.".format(name, self._button_map[name].pin))
        elif type(pin) is not int:
            raise AttributeError("Value for pin must be an integer.")
        else:
            # TODO: Add bounce time, hold time, and hold limit logic here
            ButtonManager().add_button(pin, name)
            button_callbacks = ButtonCallbacks(pressed_callback, released_callback, held_callback)
            pinned_callback = PinnedCallbacks(pin, button_callbacks)
            self._button_map[name] = pinned_callback


class MultiButtonControllerMixin(AbstractButtonControllerMixin):

    # TODO: Add logic for removing buttons when controllers are unregistered. Checks other controllers for final decision.

    def __init__(self):
        super(MultiButtonControllerMixin, self).__init__()
        self._button_controllers = []

    def register_controller(self, button_controller, front_of_queue=False):
        if front_of_queue is True:
            self._button_controllers.insert(0, button_controller)
        else:
            self._button_controllers.append(button_controller)

    def unregister_controller(self, button_controller):
        self._button_controllers.remove(button_controller)

    def _handle_button_event(self, event):
        for controller in self._button_controllers:
            controller._handle_button_event(event)

    def _setup_buttons(self):
        pass


class DPadButtonControllerMixin(AbstractButtonControllerMixin):

    # TODO: Put in a method for changing default pin numbers

    def _setup_buttons(self):
        self._setup_button("up", 27, self._up_pressed, self._up_released, self._up_held)
        self._setup_button("down", 5, self._down_pressed, self._down_released, self._down_held)
        self._setup_button("left", 17, self._left_pressed, self._left_released, self._left_held)
        self._setup_button("right", 22, self._right_pressed, self._right_released, self._right_held)

    def _up_pressed(self):
        """
        Override this method to perform an action upon pressing the up button.
        """
        pass

    def _up_released(self):
        """
        Override this method to perform an action upon releasing the up button.
        """
        pass

    def _up_held(self):
        """
        Override this method to perform an action upon holding the up button.
        """
        pass

    def _down_pressed(self):
        """
        Override this method to perform an action upon pressing the down button.
        """
        pass

    def _down_released(self):
        """
        Override this method to perform an action upon releasing the down button.
        """
        pass

    def _down_held(self):
        """
        Override this method to perform an action upon holding the down button.
        """
        pass

    def _left_pressed(self):
        """
        Override this method to perform an action upon pressing the left button.
        """
        pass

    def _left_released(self):
        """
        Override this method to perform an action upon releasing the left button.
        """
        pass

    def _left_held(self):
        """
        Override this method to perform an action upon holding the left button.
        """
        pass

    def _right_pressed(self):
        """
        Override this method to perform an action upon pressing the right button.
        """
        pass

    def _right_released(self):
        """
        Override this method to perform an action upon releasing the right button.
        """
        pass

    def _right_held(self):
        """
        Override this method to perform an action upon holding the right button.
        """
        pass


class OkCancelButtonControllerMixin(AbstractButtonControllerMixin):

    def _setup_buttons(self):
        self._setup_button("ok", 12, self._ok_pressed, self._ok_released, self._ok_held)
        self._setup_button("cancel", 6, self._cancel_pressed, self._cancel_released, self._cancel_held)

    def _ok_pressed(self):
        """
        Override this method to perform an action upon pressing the OK button.
        """
        pass

    def _ok_released(self):
        """
        Override this method to perform an action upon releasing the ok button.
        """
        pass

    def _ok_held(self):
        """
        Override this method to perform an action upon holding the ok button.
        """
        pass

    def _cancel_pressed(self):
        """
        Override this method to perform an action upon pressing the cancel button.
        """
        pass

    def _cancel_released(self):
        """
        Override this method to perform an action upon releasing the cancel button.
        """
        pass

    def _cancel_held(self):
        """
        Override this method to perform an action upon holding the cancel button.
        """
        pass

