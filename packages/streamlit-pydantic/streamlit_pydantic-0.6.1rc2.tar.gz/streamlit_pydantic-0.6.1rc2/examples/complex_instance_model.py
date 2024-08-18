import datetime
from enum import Enum
from typing import Annotated, Dict, List, Set

import streamlit as st
from annotated_types import Gt
from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color

import streamlit_pydantic as sp


class OtherData(BaseModel):
    text: str
    integer: int


class SelectionValue(str, Enum):
    FOO = "foo"
    BAR = "bar"


class ExampleModel(BaseModel):
    some_number: float = 10.0  # Optional
    some_text: str = Field(..., description="A text property")
    some_text_with_an_alias: str = Field(
        ..., description="A text property with an alias", alias="some_alias"
    )
    some_integer: int = Field(20, description="An integer property.")
    some_date: datetime.date = Field(..., description="A date.")
    some_time: datetime.time = Field(..., description="A time.")
    some_datetime: datetime.datetime = Field(..., description="A datetime.")
    some_boolean: bool = False  # Option
    long_text: str = Field(
        ..., format="multi-line", description="Unlimited text property"
    )
    integer_in_range: int = Field(
        20,
        ge=10,
        le=30,
        multiple_of=2,
        description="Number property with a limited range.",
    )
    some_colour: Color
    single_selection: SelectionValue = Field(
        ..., description="Only select a single item from a set."
    )
    multi_selection: Set[SelectionValue] = Field(
        ..., description="Allows multiple items from a set."
    )
    disabled_selection: SelectionValue = Field(
        ..., readOnly=True, description="A read only field that is shown as disabled"
    )
    read_only_text: str = Field(
        "Lorem ipsum dolor sit amet",
        description="This is a ready only text.",
        readOnly=True,
    )
    nested_object: OtherData = Field(
        ...,
        description="Another object embedded into this model.",
    )
    int_dict: Dict[str, Annotated[int, Gt(-4)]] = Field(
        ...,
        description="Dict property with int values",
    )
    date_dict: Dict[str, datetime.datetime] = Field(
        ...,
        description="Dict property with date values",
    )
    bool_dict: Dict[str, bool] = Field(
        ...,
        description="Dict property with bool values",
    )
    color_dict: Dict[str, Color] = Field(
        ...,
        description="A dict of colors embedded into this model.",
    )
    int_list: List[Annotated[int, Gt(2)]] = Field(
        ...,
        description="List of int values",
        max_items=4,
        min_items=2,
    )
    color_list: List[Color] = Field(
        ...,
        description="List of color values",
        min_items=2,
    )
    object_list: List[OtherData] = Field(
        ...,
        max_items=5,
        description="A list of objects embedded into this model.",
    )
    object_dict: Dict[str, OtherData] = Field(
        ...,
        description="Dict property with complex values",
    )


instance = ExampleModel(
    some_number=999.99,
    some_text="Some INSTANCE text",
    some_alias="Some INSTANCE alias text",
    some_integer=0,
    some_date=datetime.date(1999, 9, 9),
    some_time=datetime.time(9, 9, 16),
    some_datetime=datetime.datetime(1999, 9, 9),
    integer_in_range=28,
    some_boolean=True,
    long_text="This is some really long text from the INSTANCE",
    some_colour=Color("green"),
    single_selection=SelectionValue.FOO,
    disabled_selection=SelectionValue.BAR,
    multi_selection=[SelectionValue.FOO, SelectionValue.BAR],
    read_only_text="INSTANCE read only text",
    nested_object=OtherData(text="nested data INSTANCE text", integer=66),
    int_dict={"key 1": 33, "key 2": 33, "key 3": 333},
    date_dict={"date_key 1": datetime.datetime(1999, 9, 9)},
    bool_dict={"bool_key 1": True},
    color_dict={"Colour A": Color("#F3F3F3"), "Colour B": Color("#4E4E4E")},
    int_list=[9, 99, 999],
    color_list=[Color("#F300F3"), Color("#00F3F3")],
    object_list=[
        OtherData(text="object list INSTANCE item 1", integer=6),
        OtherData(text="object list INSTANCE item 2", integer=99),
    ],
    object_dict={
        "obj 1": OtherData(text="object list dict item 1", integer=6),
    },
)


from_model_tab, from_instance_tab = st.tabs(
    ["Form inputs from model", "Form inputs from instance"]
)

with from_model_tab:
    data = sp.pydantic_input(key="my_complex_input_model", model=ExampleModel)
    if data:
        with st.expander("Current Input State", expanded=False):
            st.json(data)


with from_instance_tab:
    instance_input_data = sp.pydantic_input(
        key="my_complex_input_instance", model=instance
    )
    if instance_input_data:
        with st.expander("Current Input State", expanded=False):
            st.json(instance_input_data)

st.markdown("---")

with st.expander("Session State", expanded=False):
    st.write(st.session_state)
