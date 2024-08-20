from typing import (
    TypedDict,
    NotRequired,
    Literal,
    Union,
    Dict,
    List,
    Any,
    Callable,
    get_type_hints,
)
from enum import Enum


class INTERACTION_TYPE(str, Enum):
    INPUT = "input"
    BUTTON = "button"
    DISPLAY = "display"
    LAYOUT = "layout"


class TYPE(str, Enum):
    # INPUT TYPES
    INPUT_TEXT = "input-text"
    INPUT_NUMBER = "input-number"
    INPUT_EMAIL = "input-email"
    INPUT_URL = "input-url"
    INPUT_PASSWORD = "input-password"
    INPUT_RADIO_GROUP = "input-radio-group"
    INPUT_SELECT_DROPDOWN_SINGLE = "input-select-dropdown-single"
    INPUT_SELECT_DROPDOWN_MULTI = "input-select-dropdown-multi"
    INPUT_TABLE = "input-table"
    INPUT_FILE_DROP = "input-file-drop"

    # BUTTON TYPES
    BUTTON_DEFAULT = "button-default"
    BUTTON_FORM_SUBMIT = "button-form-submit"

    # DISPLAY TYPES
    DISPLAY_TEXT = "display-text"
    DISPLAY_HEADER = "display-header"
    DISPLAY_JSON = "display-json"
    DISPLAY_SPINNER = "display-spinner"
    DISPLAY_CODE = "display-code"
    DISPLAY_IMAGE = "display-image"
    DISPLAY_MARKDOWN = "display-markdown"
    # A special type that's used to represent when a render returns None
    DISPLAY_NONE = "display-none"

    # LAYOUT TYPES
    LAYOUT_STACK = "layout-stack"
    LAYOUT_FORM = "layout-form"


def add_type_hints_as_class_attributes(cls):
    hints = get_type_hints(cls)
    for name, hint in hints.items():
        setattr(cls, name, hint)
    return cls


LAYOUT_DIRECTION = Literal[
    "vertical",
    "vertical-reverse",
    "horizontal",
    "horizontal-reverse",
]

LAYOUT_DIRECTION_DEFAULT: LAYOUT_DIRECTION = "vertical"

LAYOUT_JUSTIFY = Literal[
    "start",
    "end",
    "center",
    "between",
    "around",
    "evenly",
]

LAYOUT_JUSTIFY_DEFAULT: LAYOUT_JUSTIFY = "start"

LAYOUT_ALIGN = Literal[
    "start",
    "end",
    "center",
    "baseline",
    "stretch",
]

LAYOUT_ALIGN_DEFAULT: LAYOUT_ALIGN = "start"


@add_type_hints_as_class_attributes
class INPUT_UTILS:
    MULTI_SELECTION_MIN_DEFAULT = 0
    MULTI_SELECTION_MAX_DEFAULT = 1000000000

    class SelectOptionDict(TypedDict):
        value: Any
        label: str
        description: NotRequired[str]

    SelectOptionStr = str

    SelectOptions = Union[list[SelectOptionDict], list[SelectOptionStr]]

    TableDataRow = Dict[str, Union[str, int, float, None]]
    TableData = list[TableDataRow]

    class TableColumn(TypedDict):
        label: str
        key: str

    TableColumns = list[TableColumn]


@add_type_hints_as_class_attributes
class DISPLAY_UTILS:
    JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
    Json = Union[Dict[str, JsonValue], List[JsonValue]]


class ComponentStyle(TypedDict, total=False):
    # size
    width: str
    height: str
    minWidth: str
    maxWidth: str
    minHeight: str
    maxHeight: str

    # margin
    margin: str
    marginTop: str
    marginBottom: str
    marginLeft: str
    marginRight: str

    # padding
    padding: str
    paddingTop: str
    paddingBottom: str
    paddingLeft: str
    paddingRight: str

    # overflow
    overflowX: Literal["visible", "hidden", "scroll", "auto", "clip"]
    overflowY: Literal["visible", "hidden", "scroll", "auto", "clip"]

    # color
    color: str
    backgroundColor: str

    # border radius
    borderRadius: str
    borderTopLeftRadius: str
    borderTopRightRadius: str
    borderBottomLeftRadius: str
    borderBottomRightRadius: str

    # border
    border: str
    borderTop: str
    borderBottom: str
    borderLeft: str
    borderRight: str

    # text align
    textAlign: Literal["left", "right", "center", "justify", "start", "end"]

    # font
    fontSize: str
    fontWeight: str

    # gap
    gap: str

    # display
    display: str

    # position
    position: Literal["static", "relative", "absolute", "fixed", "sticky"]
    top: str
    right: str
    bottom: str
    left: str
    zIndex: int

    # flex
    flex: str
    flexGrow: float
    flexShrink: float
    flexBasis: str
    flexDirection: Literal["row", "row-reverse", "column", "column-reverse"]
    flexWrap: Literal["nowrap", "wrap", "wrap-reverse"]
    justifyContent: Literal[
        "flex-start",
        "flex-end",
        "center",
        "space-between",
        "space-around",
        "space-evenly",
    ]
    alignItems: Literal["stretch", "flex-start", "flex-end", "center", "baseline"]
    alignSelf: Literal[
        "auto", "flex-start", "flex-end", "center", "baseline", "stretch"
    ]
    alignContent: Literal[
        "flex-start", "flex-end", "center", "space-between", "space-around", "stretch"
    ]
    order: int

    # grid
    gridTemplateColumns: str
    gridTemplateRows: str
    gridTemplateAreas: str
    gridAutoColumns: str
    gridAutoRows: str
    gridAutoFlow: Literal["row", "column", "dense", "row dense", "column dense"]
    gridColumn: str
    gridRow: str
    gridArea: str
    columnGap: str
    rowGap: str

    # transform
    transform: str
    transformOrigin: str

    # transition
    transition: str

    # opacity
    opacity: float

    # cursor
    cursor: str

    # box-shadow
    boxShadow: str

    # outline
    outline: str
    outlineOffset: str

    # visibility
    visibility: Literal["visible", "hidden", "collapse"]

    # white-space
    whiteSpace: Literal[
        "normal", "nowrap", "pre", "pre-wrap", "pre-line", "break-spaces"
    ]

    # word-break
    wordBreak: Literal["normal", "break-all", "keep-all", "break-word"]

    # text-overflow
    textOverflow: Literal["clip", "ellipsis"]

    # line-height
    lineHeight: str

    # letter-spacing
    letterSpacing: str

    # text-decoration
    textDecoration: str

    # text-transform
    textTransform: Literal["none", "capitalize", "uppercase", "lowercase"]

    # vertical-align
    verticalAlign: str

    # list-style
    listStyle: str

    # background
    backgroundImage: str
    backgroundSize: str
    backgroundPosition: str
    backgroundRepeat: str
    backgroundAttachment: str

    # filter
    filter: str

    # backdrop-filter
    backdropFilter: str

    # resize
    resize: Literal["none", "both", "horizontal", "vertical"]

    # user-select
    userSelect: Literal["none", "auto", "text", "contain", "all"]

    # pointer-events
    pointerEvents: Literal["auto", "none"]

    # content
    content: str


@add_type_hints_as_class_attributes
class Nullable:
    NoArgumentsCallable = Union[Callable[[], Any], None]
    Callable = Union[Callable[..., Any], None]
    Str = Union[str, None]
    Bool = Union[bool, None]
    Int = Union[int, None]
    Float = Union[float, None]
    Style = Union[ComponentStyle, None]

    TableColumns = Union[INPUT_UTILS.TableColumns, None]

    class List:
        Str = Union[List[str], None]
        Int = Union[List[int], None]
        Float = Union[List[float], None]
        Bool = Union[List[bool], None]


class ComponentReturn(TypedDict):
    type: TYPE
    interactionType: INTERACTION_TYPE
    model: Dict[str, Any]
    hooks: Any
