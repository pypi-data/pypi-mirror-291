from ..constants import INTERACTION_TYPE, TYPE, Nullable


def _create_button(type, id, *, appearance=None, style=None, label=None, on_click=None):
    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "label": label,
                "hasOnClickHook": on_click is not None,
                **({"appearance": appearance} if appearance is not None else {}),
            },
        },
        "hooks": {"onClick": on_click},
        "type": type,
        "interactionType": INTERACTION_TYPE.BUTTON,
    }


def button_default(
    id: str,
    *,
    appearance: Nullable.Str = None,
    style: Nullable.Style = None,
    label: Nullable.Str = None,
    on_click: Nullable.Callable = None,
):
    return _create_button(
        TYPE.BUTTON_DEFAULT,
        id,
        style=style,
        label=label,
        on_click=on_click,
        appearance=appearance,
    )


def button_form_submit(
    id: str,
    *,
    appearance: Nullable.Str = None,
    style: Nullable.Style = None,
    label: Nullable.Str = None,
    on_click: Nullable.Callable = None,
):
    return _create_button(
        TYPE.BUTTON_FORM_SUBMIT,
        id,
        style=style,
        label=label,
        on_click=on_click,
        appearance=appearance,
    )
