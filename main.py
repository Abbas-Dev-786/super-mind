import streamlit as st
from flow_runner import run_flow
import json

st.title("Social Media Analytics 🤖")
st.markdown(
    """
Made by [Abbas Bhanpura wala](https://abbas-bhanpura-wala.vercel.app/)

"""
)

endpoint = "2520f246-749c-468d-b715-747e436afdf2"

output_type = "chat"
input_type = "chat"

message = st.text_area("Enter your query", placeholder="Type your query here...")

if st.button("Get Analytics"):
    try:
        response = run_flow(
            message=message,
            endpoint=endpoint,
            output_type=output_type,
            input_type=input_type,

        )

        st.subheader("Response")
        if isinstance(response, dict):
            try:
                parsed_value = response["outputs"][0]["outputs"][0]["results"][
                    "message"
                ]["data"]["text"]
                st.write(parsed_value)

                if "visualization" in response["outputs"][0]["outputs"][0]["results"]:
                    visualization_data = response["outputs"][0]["outputs"][0][
                        "results"
                    ]["visualization"]
                    st.json(visualization_data)

            except KeyError:
                st.error("The expected key structure is missing in the response.")
        elif isinstance(response, str):
            st.write(response)
        else:
            st.error(
                "Unexpected response format. Check the API or tweaks configuration."
            )

    except json.JSONDecodeError:
        st.error("Invalid JSON in Tweaks")
    except Exception as e:
        st.error(f"Error: {e}")