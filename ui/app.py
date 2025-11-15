import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.title("📊 DataRefineX Dashboard")

file_url = st.text_input("Enter CSV URL or path:")

if st.button("Process CSV"):
    if not file_url.strip():
        st.warning("⚠️ Please enter a valid URL or path.")
    else:
        with st.spinner("Submitting job..."):
            res = requests.post(f"{API_URL}/process", json={"file_url": file_url})
            data = res.json()
            job_id = data.get("job_id")

        if not job_id:
            st.error(f"❌ Failed to queue job: {data}")
        else:
            st.success(f"✅ Job queued! ID: {job_id}")
            st.info("⏳ Waiting for completion...")

            progress = st.progress(0)
            poll_count = 0

            while True:
                poll_count += 1
                time.sleep(2)
                progress.progress(min(poll_count * 10, 100))

                status_res = requests.get(f"{API_URL}/status/{job_id}")
                status_data = status_res.json()

                # st.write("Debug:", status_data)

                if status_data["status"] == "SUCCESS":
                    result = status_data.get("result", {})
                    uploaded_link = result.get("uploaded")
                    local_file = result.get("file")

                    st.success("✅ Processing Complete!")
                    st.write("**Local File:**", local_file)
                    if uploaded_link:
                        st.markdown(
                            f"**Uploaded Link:** [View on Hugging Face]({uploaded_link})"
                        )
                    else:
                        st.info("ℹ️ Processed locally but not uploaded.")

                    progress.progress(100)
                    break

                elif status_data["status"] == "FAILURE":
                    st.error("❌ Job failed!")
                    st.json(status_data)
                    break
