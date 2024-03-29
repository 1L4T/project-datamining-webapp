import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard",
                    page_icon=":bar_chart:",
                    layout='wide')

st.title(":chart_with_upwards_trend: CUSTOMER SEGMENTATION!!!")
st.markdown('<style>div.block-container{padding-top:1rem;}<style>', unsafe_allow_html=True)
st.markdown("👉👉👉 Welcome to our Customer Segmentation Dashboard! Upload your CSV file to explore insights and visualize customer segments. Let's uncover valuable insights together! 👈👈👈")

input_csv = st.sidebar.file_uploader("Upload your CSV File", type=['csv'])

data = None  

if input_csv is not None:
        data = pd.read_csv(input_csv)

col1, col2 = st.columns([1, 1])
with col1:
    if data is not None:
        st.info("CSV Uploaded successfully")
        st.dataframe(data)
        txt1 = st.text_area("Your DATA", "To generate plots, your CSV file must contain a column named 'Cluster'. Without this column, our system won't be able to generate visualizations.")

        st.subheader("Pie Charts Grouped by Cluster", divider='blue')
        if 'Cluster' in data.columns:
            binary_columns = []
            string_columns = []
            for col_name in data.columns:
                if data[col_name].isin([0, 1]).all():  
                    binary_columns.append(col_name)
                elif data[col_name].dtype == 'object':
                    string_columns.append(col_name)
            if not binary_columns and not string_columns:
                st.warning("No binary or string columns found in the uploaded data.")
            else:
                available_columns = binary_columns + string_columns
                available_columns.remove('Cluster')  # Remove 'Cluster' from available columns
                selected_column = st.selectbox("Select Column for Pie Charts Grouped by Cluster", available_columns, key=f"pie_chart_grouped")
                if selected_column:
                    if selected_column in binary_columns:
                        pie_data = data.groupby(['Cluster', selected_column]).size().unstack(fill_value=0)
                        for col in pie_data.columns:
                            fig_pie = px.pie(names=pie_data.index, values=pie_data[col], title=f'Pie Chart for {selected_column} Grouped by Cluster ({col})',
                                             color=pie_data.index, color_discrete_map={'C1': 'blue', 'C2': 'green', 'C3': 'red', 'C4': 'orange', 'C5': 'purple'})
                            fig_pie.update_layout(autosize=True)
                            fig_pie.update_traces(textposition='inside', textinfo='percent+label')  
                            st.plotly_chart(fig_pie)
                            st.write(f"Cluster {col} - {selected_column}")
                            st.dataframe(pie_data[[col]])
                    else:
                        cluster_grouped_data = data.groupby(['Cluster', selected_column]).size().unstack(fill_value=0)
                        for col in cluster_grouped_data.columns:
                            fig_cluster_pie = px.pie(names=cluster_grouped_data.index, values=cluster_grouped_data[col], title=f'Pie Chart for {selected_column} Grouped by Cluster ({col})',
                                                     color=cluster_grouped_data.index, color_discrete_map={True: 'blue', False: 'green'})
                            fig_cluster_pie.update_layout(autosize=True)
                            fig_cluster_pie.update_traces(textposition='inside', textinfo='percent+label')  
                            st.plotly_chart(fig_cluster_pie)
                            st.write(f"Cluster {col} - {selected_column}")
                            st.dataframe(cluster_grouped_data[[col]])
        else:
            st.warning("Cluster column not found in the uploaded CSV file.")

        if 'Cluster' in data.columns:
            agg_column = st.selectbox("Select Column to Aggregate", [col for col in data.columns if col != 'Cluster'])
            if data[agg_column].dtype == 'object':
                st.warning("Aggregation functions cannot be applied to non-numeric data.")
            else:
                agg_functions = ['mean', 'sum', 'std', 'min', 'max', 'count']
                selected_functions = st.multiselect("Select Aggregation Functions", agg_functions, default=['mean', 'sum', 'std', 'count'])
                
                aggregated_data = pd.DataFrame(index=data['Cluster'].unique())
                for func in selected_functions:
                    if func == 'count':
                        aggregated_data[func.capitalize()] = data.groupby('Cluster')[agg_column].size().values
                    else:
                        aggregated_data[func.capitalize()] = data.groupby('Cluster')[agg_column].agg(func).values
                with st.expander("View Data for Aggregated Column"):
                    st.dataframe(aggregated_data)
        else:
            st.warning("Cluster column not found in the uploaded CSV file.")

with col2:
    if data is not None:
        st.subheader("Boxplot Grouped by Cluster", divider='blue')
        if 'Cluster' in data.columns:
            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
            y_variables = [col for col in numeric_columns if col != 'Cluster']
            if len(y_variables) > 0:
                y_variable_box = st.selectbox("Select Y-axis variable for Boxplot", y_variables)
                fig_box = px.box(data, x='Cluster', y=y_variable_box, color='Cluster',
                                color_discrete_map={'C1': 'blue', 'C2': 'green', 'C3': 'red', 'C4': 'orange', 'C5': 'purple'})
                fig_box.update_layout(autosize=True)
                fig_box.update_layout(xaxis=dict(title='Cluster', titlefont=dict(size=14), tickfont=dict(size=12)), boxmode='group')  
                st.plotly_chart(fig_box)
                
                with st.expander("View Data for Boxplot"):
                    st.dataframe(data[[y_variable_box, 'Cluster']])
            else:
                st.warning("No numeric columns found in the uploaded data. Please upload a CSV file with numeric columns.")
        else:
            st.warning("Cluster column not found in the uploaded CSV file.")

        st.subheader("Bar Chart Grouped by Cluster", divider='blue')
        if 'Cluster' in data.columns:
            binary_columns = []
            string_columns = []
            for col_name in data.columns:
                if data[col_name].isin([0, 1]).all():  
                    binary_columns.append(col_name)
                elif data[col_name].dtype == 'object':
                    string_columns.append(col_name)
            if not binary_columns and not string_columns:
                st.warning("No binary or string columns found in the uploaded data.")
            else:
                available_columns = binary_columns + string_columns
                selected_column = st.selectbox("Select Column for Bar Chart", available_columns, key="bar_chart_column")
                if selected_column:
                    if selected_column in binary_columns:
                        bar_data = data.groupby('Cluster')[selected_column].value_counts().unstack(fill_value=0).reset_index()
                    else:
                        bar_data = data.groupby('Cluster')[selected_column].value_counts().unstack().fillna(0).reset_index()
                    fig_bar = px.bar(bar_data, x='Cluster', y=bar_data.columns[1:], barmode='group')
                    fig_bar.update_layout(autosize=True)
                    fig_bar.update_layout(xaxis=dict(title='Cluster', titlefont=dict(size=14), tickfont=dict(size=12)), barmode='group')  
                    st.plotly_chart(fig_bar)
                    
                    with st.expander("View Data for Bar Chart"):
                        st.dataframe(bar_data)
        else:
            st.warning("Cluster column not found in the uploaded CSV file.")

        

        st.subheader("Proportion", divider='blue')
        if 'Cluster' in data.columns:
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
                selected_column = st.selectbox("Select Column for Pie Chart", available_columns, key=f"pie_chart")
                if selected_column:
                    if selected_column in binary_columns:
                        pie_data = data[selected_column].value_counts()
                        fig_pie = px.pie(names=pie_data.index, values=pie_data.values, title=f'Pie Chart for {selected_column}',
                                         color=pie_data.index, color_discrete_map={True: 'blue', False: 'green'})
                        fig_pie.update_layout(autosize=True)
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label')  
                        st.plotly_chart(fig_pie)
                    else:
                        cluster_pie_data = data[selected_column].value_counts()
                        fig_cluster_pie = px.pie(names=cluster_pie_data.index, values=cluster_pie_data.values, title=f'Pie Chart for {selected_column}',
                                                 color=cluster_pie_data.index, color_discrete_map={'C1': 'blue', 'C2': 'green', 'C3': 'red', 'C4': 'orange', 'C5': 'purple'})
                        fig_cluster_pie.update_layout(autosize=True)
                        fig_cluster_pie.update_traces(textposition='inside', textinfo='percent+label')  
                        st.plotly_chart(fig_cluster_pie)
                        
                        with st.expander("View Data for Pie Chart"):
                            st.dataframe(cluster_pie_data.rename_axis('Cluster').reset_index(name='Count'))
        else:
            st.warning("Cluster column not found in the uploaded CSV file.")
        txt2 = st.text_area("Customer Behavior Analysis", "This dashboard provides insights into customer behavior based on segmentation. Explore various visualizations to understand customer clusters and their characteristics.")
        
if data is not None:
        try:
            if 'Cluster' not in data.columns:
                st.warning("Cluster column not found in the uploaded CSV file.")
            else:
                st.subheader("Scatter Plot", divider='blue')

                numeric_data = data.select_dtypes(include=['float64', 'int64'])

                if not numeric_data.empty:           
                    col1, col2 = st.columns(2)
                    with col1:
                        x_variable = st.selectbox("Select X-axis variable", numeric_data.columns, key="x_variable")
                    with col2:
                        y_variable = st.selectbox("Select Y-axis variable", numeric_data.columns, key="y_variable")

                    fig_scatter = px.scatter(data, x=x_variable, y=y_variable, color='Cluster')
                    fig_scatter.update_xaxes(title_text=x_variable)
                    fig_scatter.update_yaxes(title_text=y_variable)
                    st.plotly_chart(fig_scatter, use_container_width=True)    

                    with st.expander("View Data for Scatter Plot"):
                        st.dataframe(data[[x_variable, y_variable, 'Cluster']])

                else:
                    st.warning("No numeric columns found in the uploaded data. Please upload a CSV file with numeric columns.")
        except ValueError as e:
            if "Duplicate column names found" in str(e):
                st.warning("Duplicate column names found but ignored. Proceeding with the analysis.")
            else:
                raise e
            



            