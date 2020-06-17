import pandas as pd

from fds_profiling.report import templates, renderable
from fds_profiling.model.aggregators import groupby_aggregator, count_metric
from fds_profiling.visualisation.charts import bar_chart, histogram
from fds_profiling.model.describe import describe_series
from fds_profiling.model.associations import associations


def variables_html(dataframe, var_types, metrics, anchor_id):
    
    ## reading template
    nav_table_template = templates.template("navigation_table.html")
    
    ## associations df
    associations_df = associations(dataframe, var_types)
        
    html = ""
    
    for var_i, var_type in var_types.items():
        
        tabs = []
        
        if (var_type == "NUM"):
            
            ## 1st tab - statistics
            describe_df = describe_series(dataframe[var_i], var_type)
            tabs.append(
                renderable.Renderable(
                    content = {
                        "size": 3,
                        "headings": ["Descriptive", "Variability", "Moments", "Outliers"],
                        "contents": describe_df[0:4]
                    },
                    name = "Statistics",
                    anchor_id = anchor_id + var_i + "statistics",
                    type_id = "multiple_tables"))
            
            ## 2nd tab - associations
            num_associations = associations_df[(associations_df["col_a"] == var_i) & (associations_df["type_"] == "NUM-NUM")]
            pos_num_associations = num_associations[num_associations['association'] > 0].head(5)
            neg_num_associations = num_associations[num_associations['association'] < 0].sort_values('association').head(5)

            cat_associations = associations_df[(associations_df["col_a"] == var_i) & (associations_df["type_"] == "NUM-CAT")].head(5)

            table_pos_num_associations = convert_df_to_table(pos_num_associations, "col_b", "association")
            table_neg_num_associations = convert_df_to_table(neg_num_associations, "col_b", "association")
            table_cat_associations = convert_df_to_table(cat_associations, "col_b", "association")
            
            tabs.append(
                renderable.Renderable(
                    content = {
                        "size": 4,
                        "headings": ["Positive correlation", "Negative correlation", "Categorical"],
                        "contents": [table_pos_num_associations, table_neg_num_associations, table_cat_associations]
                    },
                    name = "Associations",
                    anchor_id = anchor_id + var_i + "associations",
                    type_id = "multiple_tables"))
            
            ## 3rd tab - Histogram
            
            ## a.Quantile ststistics
            quantile_df = describe_df[-1]
            
            ## b. Histogram
            histogram_encoding = histogram(dataframe[var_i])
            
            tabs.append(
                renderable.Renderable(
                    content = {"table_heading": "Quantile statistics", "table_content": quantile_df, "image_encoding": histogram_encoding},
                    name = "Histogram",
                    anchor_id = anchor_id + var_i + "histogram",
                    type_id = "table_chart"))
        
        
        
        elif ((var_type == "CAT") | (var_type == "BOOL")):
            ## 1st tab - statistics
            describe_df = describe_series(dataframe[var_i], var_type)
            tabs.append(
                renderable.Renderable(
                    content = {
                        "size": 3,
                        "headings": ["Descriptive", "Variability", "Moments", "Outliers"],
                        "contents": describe_df
                    },
                    name = "Statistics",
                    anchor_id = anchor_id + var_i + "statistics",
                    type_id = "multiple_tables"))
            
            ## 2nd tab - associations
            continuous_associations = associations_df[(associations_df["col_a"] == var_i) & (associations_df["type_"] == "CAT-NUM")].head(5)
            parent_associations = associations_df[(associations_df["col_a"] == var_i) & (associations_df["type_"] == "CAT-CAT")].head(5)
            child_associations = associations_df[(associations_df["col_b"] == var_i) & (associations_df["type_"] == "CAT-CAT")].head(5)

            table_continuous_associations = convert_df_to_table(continuous_associations, "col_b", "association")
            table_parent_associations = convert_df_to_table(parent_associations, "col_b", "association")
            table_child_associations = convert_df_to_table(child_associations, "col_a", "association")
            
            tabs.append(
                renderable.Renderable(
                    content = {
                        "size": 4,
                        "headings": ["Numerical", "Categorical(Parent)", "Categorical(Child)"],
                        "contents": [table_continuous_associations, table_parent_associations, table_child_associations]
                    },
                    name = "Associations",
                    anchor_id = anchor_id + var_i + "associations",
                    type_id = "multiple_tables"))    
            
            
            ## 3rd tab - count
            
            ## a. count dataframe
            count_df = count_metric(dataframe[var_i], var_i)
            
            ## b. bar chart
            bar_chart_encoding = bar_chart(count_df, "Percent", is_percent=True)
            
            tabs.append(
                renderable.Renderable(
                    content = {"dataframe": count_df, "image_encoding": bar_chart_encoding},
                    name = "Count",
                    anchor_id = anchor_id + var_i + "Count",
                    type_id = "dataframe_chart"))
            
            
            ## Remaining tabs - user metrics
            
            #### groupby data
            agg_df = groupby_aggregator(dataframe, var_i, metrics)
            
            for metric_i in metrics:
                
                ## a. table: sorting and re-ordering
                temp_df = agg_df.sort_values(metric_i[0], ascending=False).head(5)
                temp_df = temp_df[[metric_i[0]] + [col for col in temp_df if col != metric_i[0]]]
                
                ## b. bar chart:
                bar_chart_encoding = bar_chart(temp_df, metric_i[0])
                
                
                tabs.append(
                    renderable.Renderable(
                        content = {"dataframe": temp_df, "image_encoding": bar_chart_encoding},
                        name = metric_i[0],
                        anchor_id = anchor_id + var_i + metric_i[0],
                        type_id = "dataframe_chart"))
                
        
        else:
            ## 1st tab - statistics
            describe_df = describe_series(dataframe[var_i], var_type)
            tabs.append(
                renderable.Renderable(
                    content = {
                        "size": 3,
                        "headings": ["Descriptive", "Variability", "Moments", "Outliers"],
                        "contents": describe_df
                    },
                    name = "Statistics",
                    anchor_id = anchor_id + var_i + "statistics",
                    type_id = "multiple_tables"))
        
        
        html += nav_table_template.render(tabs = tabs, anchor_id = anchor_id, header=var_i, sub_heading=var_type)
        
        
        
    return html


def convert_df_to_table(dataframe, name, value):
    
    table = []
    for index, row in dataframe.iterrows():
        table.append(
            { "name": row[name], "value": row[value], "alert": False },
        )
    return table
        
            
