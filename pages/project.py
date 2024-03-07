import streamlit as st 

st.title("Project")
for col_index, col in enumerate([col3, col4, col5, col6, col7], start=3):
    with col:
        if data is not None:
            binary_columns = []
            for col_name in data.columns:
                if data[col_name].isin([0, 1]).all():  
                    binary_columns.append(col_name)
            string_columns = data.select_dtypes(include=['object']).columns
            if not binary_columns and string_columns.empty:
                st.warning("No binary or string columns found in the uploaded data.")
            else:
                available_columns = []
                if binary_columns:
                    available_columns += list(binary_columns)
                if not string_columns.empty:
                    available_columns += list(string_columns)
                selected_column = st.selectbox("Select Column for Pie Chart", available_columns, key=f"pie_chart_{col_index}")
                if selected_column:
                    if selected_column in binary_columns:
                        pie_data = data[selected_column].value_counts()
                        fig_pie = px.pie(names=pie_data.index, values=pie_data.values, title=selected_column,
                                         color=pie_data.index, color_discrete_map={True: 'blue', False: 'green'})
                        fig_pie.update_layout(autosize=True, width=300, height=300) 
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label')  
                        st.plotly_chart(fig_pie)
                    elif selected_column in string_columns:
                        pie_data = data[selected_column].value_counts()
                        fig_pie = px.pie(names=pie_data.index, values=pie_data.values, title=selected_column)
                        fig_pie.update_layout(autosize=True, width=300, height=300)  
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label')  
                        st.plotly_chart(fig_pie)
                    else:
                        st.warning("No binary or string columns found in the uploaded data.")