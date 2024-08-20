"""Handle point-and-click element selection in a Reflex app"""

import functools
import importlib.util
import inspect
from pathlib import Path
from typing import Any

import reflex as rx

from . import paths

# These components will never be selectable.
ignored_components = [
    rx.accordion.root.__self__,
    rx.accordion.icon.__self__,
    rx.accordion.item.__self__,
    rx.accordion.trigger.__self__,
    rx.alert_dialog.trigger.__self__,
    rx.hover_card.root.__self__,
    rx.hover_card.trigger.__self__,
    rx.hover_card.content.__self__,
    rx.popover.root.__self__,
    rx.popover.trigger.__self__,
    rx.popover.content.__self__,
    rx.recharts.responsive_container.__self__,
    rx.select.content.__self__,
    rx.select.group.__self__,
    rx.select.item.__self__,
    rx.select.root.__self__,
    rx.theme.__self__,
    rx.Fragment,
]
# Radix triggers that fire on_pointer_down events need to be disabled so that on_click works.
neuter_pointer_down = [
    rx.select.trigger.__self__,
]
# For components that do not support on_click at all, wrap these in a box.
box_wrap_components = [
    rx.markdown.__self__,
]
# Preserve a reference to the original create method's function.
og_component_create = rx.Component.create.__func__


class ClickSelectionState(rx.State):
    """Track the currently selected component and the code that created it."""

    selected_element: str = ""
    _selected_code: list[str] = []
    filename: str = ""
    selected_function: str = ""
    start_lineno: int
    end_lineno: int
    selected_module: str = ""

    @rx.var
    def code(self) -> str:
        return "\n".join(self._selected_code)

    async def accept_change(self):
        """Accept the current diff."""

    async def handle_click(self, filename, function_name, lineno, end_lineno):
        print("clicking")
        self.selected_element = f"{filename}:{lineno}-{end_lineno}"
        self.filename = filename
        self.selected_function = function_name
        self.start_lineno = lineno
        self.end_lineno = end_lineno
        self._selected_code = (
            Path(filename).read_text().splitlines()[lineno - 1 : end_lineno]
        )

        if paths.tmp_root_path is not None:
            module_rel_path = Path(filename).relative_to(paths.tmp_root_path).with_suffix("")
            self.selected_module = ".".join(module_rel_path.parts)
            return

        spec = importlib.util.spec_from_file_location(
            Path(filename).stem,
            filename,
            submodule_search_locations=[paths.tmp_root_path],
        )
        module = importlib.util.module_from_spec(spec)

        self.selected_module = module.__name__


def _on_click_handler(
    props: dict[str, Any],
    filename: str,
    function_name: str,
    lineno: int,
    end_lineno: int,
):
    """Generate on_click handler and outline props for selectable components.

    Args:
        filename: The filename of the component.
        function_name: The function name of the component.
        lineno: The starting line number of the component.
        end_lineno: The ending line number of the component

    Returns:
        A dictionary of props that includes the on_click handler and outline props.
    """
    return {
        "on_click": ClickSelectionState.handle_click(
            filename,
            function_name,
            lineno,
            end_lineno,
        ).prevent_default.stop_propagation,
        "outline": rx.cond(
            ClickSelectionState.selected_element == f"{filename}:{lineno}-{end_lineno}",
            "2px dotted var(--ruby-7)",
            props.get("outline", "none"),
        ),
    }


def component_create_override(base_paths: list[Path]) -> classmethod:
    """Generate an override for Component.create that is active for the given paths.

    Args:
        base_paths: Components originating from modules prefixed by these paths will be clickable.

    Returns:
        A replacement Component.create function that adds an on_click handler where needed.
    """
    base_paths = base_paths + ["reflex_ai_tmp"]

    @classmethod
    def _component_create_override(cls, *children, **props):
        if cls not in ignored_components:
            # Walk up the stack to find the first frame that originates from a base path.
            for frame in inspect.stack()[1:]:
                if "site-packages" in frame.filename:
                    continue
                # Skip the module frame.
                if frame.function == "<module>":
                    continue
                if any(frame.filename.startswith(str(p)) for p in base_paths):
                    if cls in box_wrap_components:
                        return rx.box(
                            og_component_create(cls, *children, **props),
                            **_on_click_handler(
                                props,
                                frame.filename,
                                frame.function,
                                frame.lineno,
                                frame.positions.end_lineno,
                            ),
                        )
                    props.update(
                        _on_click_handler(
                            props,
                            frame.filename,
                            frame.function,
                            frame.lineno,
                            frame.positions.end_lineno,
                        )
                    )
                    if cls in neuter_pointer_down:
                        props.setdefault("special_props", set()).add(
                            rx.Var.create(
                                "onPointerDown={(e) => e.preventDefault()}",
                                _var_is_string=False,
                            ),
                        )
                    break
        return og_component_create(cls, *children, **props)

    return _component_create_override


def clickable(base_paths: list[Path] | None = None):
    """A decorator helper to make all components in a given page clickable to select.

    The active selection (filename and line range) is stored in
    ClickSelectionState.selected_element

    The code for the selection is cached in ClickSelectionState._selected_code

    Args:
        base_paths: Components originating from modules prefixed by these paths will be clickable.

    Returns:
        A decorator that adds an on_click handler to the component.
    """
    if base_paths is None:
        base_paths = [Path(".").resolve()]

    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            # Override the component create method.
            rx.Component.create = component_create_override(base_paths=base_paths)
            try:
                # Call the page wrapper
                return fn(*args, **kwargs)
            finally:
                # Restore the original component create method.
                rx.Component.create = classmethod(og_component_create)

        # Preserve the original function name to avoid having to specify route in add_page.
        inner.__name__ = fn.__name__
        return inner

    return outer
