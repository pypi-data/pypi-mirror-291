import streamlit as st
import streamlit_pydantic as sp
from pydantic import BaseModel


class ExampleModel(BaseModel):
    some_text: str
    some_number: int
    some_boolean: bool


from_model_tab, from_instance_tab = st.tabs(
    ["Form inputs from model", "Form inputs from instance"]
)

with from_model_tab:
    data = sp.pydantic_form(key="my_sample_form", model=ExampleModel)
    if data:
        st.json(data.model_dump())

with from_instance_tab:
    instance = ExampleModel(
        some_number=999, some_boolean=True, some_text="instance text"
    )

    instance_input_data = sp.pydantic_form(
        key="my_sample_form_instance", model=instance
    )
    if instance_input_data:
        st.json(instance_input_data.model_dump())
